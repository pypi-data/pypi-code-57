#!/usr/bin/env python3

import sys

from os import \
    makedirs, environ

from os.path import \
    join as pjoin, \
    expanduser, isdir, \
    basename, isfile, \
    abspath, dirname

from socket import \
    socket as sock, \
    timeout as TimeOutError, \
    SOCK_DGRAM, SHUT_WR, \
    AF_INET, SOCK_STREAM

from argparse import ArgumentParser

from yaml import \
    load as yload, \
    dump as ydump, \
    Loader, Dumper

from json import \
    loads as jload, \
    dumps as jdump
from json.decoder import \
    JSONDecodeError

from subprocess import \
    Popen, PIPE, DEVNULL

from asyncio import sleep as asysleep, get_event_loop


from time import sleep

try:
    import readline
except (ImportError, ModuleNotFoundError):
    pass

from discord import \
    utils as dscutil, \
    Client as DiscordClient, \
    Emoji as DiscordEmoji
from discord.ext import commands

from requests import post, get

from inquirer import prompt, List as iList

from cmd import Cmd

__dir = dirname(abspath(__file__))
if __dir not in sys.path:
	sys.path = [p for p in sys.path if p] + [__dir]

try:
	from pavlovadm.colortext import tabd, error, bgre
	from pavlovadm.__pkginfo__ import version
except ModuleNotFoundError:
	from colortext import tabd, error, bgre
	from __pkginfo__ import version

from logging import DEBUG, getLogger

class PavlovADM(Cmd):
	config = pjoin(expanduser('~'), '.config', 'pavlovadm', 'pavlovadm.conf')
	cache = pjoin(expanduser('~'), '.cache', 'pavlovadm')
	cfgdir = dirname(config)
	servers = {}
	gameini = pjoin(cfgdir, 'Game.ini')
	itemtbl = pjoin(cfgdir, 'BalancingTable.csv')
	maptbl = pjoin(cache, 'maps.tbl')
	botcfg = {}
	rconroles = []
	mapnames = None
	banlist = None
	maps = None
	hlp = None
	cnt = 0
	dbg = None
	dsc = None
	def __init__(self, *args, **kwargs):
		self.use_rawinput = False
		for (k, v) in kwargs.items():
			if hasattr(self, k):
				setattr(self, k, v)
		
		super().__init__()
		if not self.dsc:
			loop = get_event_loop()
			loop.run_until_complete(self.serverselect())

	def getsrvnames(self):
		srvnames = {}
		for srv in self.servers.keys():
			gameini = self.gameini
			if len(self.servers[srv]) > 1:
				gameini = self.servers[srv][1]
			name = srv
			if gameini.startswith('~'):
				gameini = expanduser(gameini)
			with open(gameini, 'r') as gfh:
				gis = gfh.readlines()
			for l in gis:
				if l.startswith('ServerName'):
					name = '='.join(l.split('=')[1:])
			if name.startswith('~'):
				name = expanduser(name)
			name = name.strip()
			srvnames[name] = srv
		return srvnames

	async def serverselect(self):
		srvnames = self.getsrvnames()
		ask = [
            iList(
                'srv',
                carousel=True,
                message='select server',
                choices=list(srvnames.keys()) + ['<Exit>'],
            ),
        ]
		try:
			srv = list(prompt(ask).values())[0]
		except AttributeError:
			exit()
		if srv == '<Exit>':
			exit()
		srv = srvnames[srv]
		while True:
			cmd = await self._cmdselects(srv)
			if not cmd:
				continue
			cmd = cmd.strip('<>')
			if self.dbg:
				print(bgre(cmd))
			if cmd == 'Disconnect':
				self.maps = None
				self.banlist = None
				self.hlp = None
				break
			elif cmd == 'RefreshList':
				res = await self._players(srv)
			else:
				res = await self.rconexec(srv, self.servers[srv][0], cmd.strip('<>'))
			if isinstance(res, dict):
				res = tabd(res)
			print(res)
		await self.serverselect()

	async def _getmapname(self, mapid):
		if self.mapnames and mapid in self.mapnames:
			return self.mapnames[mapid]
		url = 'https://steamcommunity.com/sharedfiles/filedetails/?id='
		res = post('%s%s'%(url, mapid.strip('UGC')))
		for l in res.text.split('\n'):
			if 'workshopItemTitle' in l:
				return l.split('>')[1].split('<')[0]

	async def _getmaps(self, srv, noask=None):
		if self.maps is None or self.mapnames is None:
			maplst = self.gameini
			if len(self.servers[srv]) > 1:
				maplst = self.servers[srv][1]
			if maplst.startswith('~'):
				maplst = expanduser(maplst)
			if not maplst.startswith('/') and not maplst.startswith('C:\\'):
				error('cannot read maplist if no absolute path is provided and', maplst, 'is not!')
				return
			self.maps = {}
			with open(maplst, 'r') as mfh:
				lines = mfh.readlines()
			try:
				with open(expanduser(self.maptbl), 'r') as mfh:
					self.mapnames = yload(mfh.read(), Loader=Loader)
			except FileNotFoundError:
				with open(expanduser(self.maptbl), 'w+') as mfh:
					mfh.write(ydump({}, Dumper=Dumper))
			self.mapnames = self.mapnames if self.mapnames else {}
			for l in lines:
				if not l or not l.startswith('MapRotation'):
					continue
				ugcid = l.split('MapId')[1].split(',')[0]
				ugcid = ugcid.strip(' =",')
				gmmod = l.split('GameMode')[1].split(')')[0]
				gmmod = gmmod.strip(' ="')
				name = await self._getmapname(ugcid)
				#print('"%s"'%ugcid)
				#print('"%s"'%gmmod)
				#print('"%s"'%name)
				self.maps[name] = [ugcid, gmmod]
				self.mapnames[ugcid] = name
			with open(expanduser(self.maptbl), 'w+') as mfh:
				mfh.write(ydump(self.mapnames, Dumper=Dumper))
		if noask: return self.maps
		ask = [
          iList(
            'map',
            carousel=True,
            message='select map',
            choices=[m for m in self.maps.keys()] + ['<Enter Other>', '<Return>'],
          ),
        ]
		mapp = list(prompt(ask).values())[0]
		if mapp == '<Return>':
			return
		elif mapp == '<Enter Other>':
			mapp = input('Enter map name: ')
			mapp = self.map2ugc([mapp])
			if mapp:
				mapp = list(mapp.keys())[0]
				mode = input('Enter game mode: ').upper()
				return '%s %s'%(mapp, mode)
			return error('could not find map\'s UGC-ID...')
		mmod = self.maps[mapp][1]
		modes = [mmod] + [s for s in ['SND', 'TDM', 'DM', 'GUN'] if s != mmod]
		ask = [
            iList(
                'mod',
                carousel=True,
                message='select mode (irrelevant if set by map)',
                choices=[m for m in modes] + ['<Return>'],
            ),
        ]
		mode = list(prompt(ask).values())[0]
		if mode != '<Return>':
			return '%s %s'%(self.maps[mapp][0], mode)

	def _getitem(self):
		items = []
		try:
			with open(expanduser(self.itemtbl), 'r') as ifh:
				items = [l.split(',')[0] for l in list(ifh.readlines())[1:]]
		except FileNotFoundError:
			items = []
		if not items:
			print('no item table present - enter item manually: ', end='')
			return str(input()).strip()
		ask = [
            iList(
                'item',
                carousel=True,
                message='select item',
                choices=items  + ['<Return>'],
            ),
        ]
		item = list(prompt(ask).values())[0]
		if item != '<Return>':
			return item


	def _getskin(self):
		ask = [
            iList(
                'skin',
                carousel=True,
                message='select skin',
                choices=['clown', 'prisoner', 'naked', 'farmer', 'russian', 'nato', '<Return>'],
            ),
        ]
		skin = list(prompt(ask).values())[0]
		if skin != '<Return>':
			return skin

	def _getammotype(self):
		ask = [
            iList(
                'ammo',
                carousel=True,
                message='select ammo-limit',
                choices=[0, 1, 2, '<Return>'],
            ),
        ]
		ammo = list(prompt(ask).values())[0]
		if ammo != '<Return>':
			return ammo

	def _getteam(self):
		ask = [
            iList(
                'team',
                carousel=True,
                message='select team',
                choices=["Blue Team (Defenders)", "Red Team (Attackers)", '<Return>'],
            ),
        ]
		team = list(prompt(ask).values())[0]
		if team != '<Return>':
			return team

	def map2ugc(self, maps):
		with open(expanduser(self.maptbl), 'r') as mfh:
			mapnames = yload(mfh.read(), Loader=Loader)
		surl = 'https://steamcommunity.com/workshop/browse/?appid=555160&searchtext={searchpattern}&childpublishedfileid=0&browsesort=trend&section=readytouseitems'
		incosurl = 'https://steamcommunity.com/workshop/browse/?appid=555160&searchtext={searchpattern}&childpublishedfileid=0&browsesort=trend&section=readytouseitems&requiredflags%%5B%%5D=incompatible'
		ugcs = {}
		for m in maps:
			hit = False
			for (u, n) in mapnames.items():
				if n == m:
					ugcs[m] = u
					hit = True
			if hit:
				continue
			res = post(surl.format(searchpattern=m))
			mapinfo = {}
			for l in res.text.split('\n'):
				if 'SharedFileBindMouseHover' in l:
					mid = 'UGC%s'%l.split('"')[1].split('_')[1]
					mapinfo[mid] = {}
					#print(mid)
					l = str(l.split('{')[1]).split('}')[0]
					for kv in l.split(','):
						if ':' in kv:
							k, v = list(kv.split(':'))[0], list(kv.split(':'))[1]
							mapinfo[mid][k.strip('"')] = v.strip('"')
					if 'title' in mapinfo[mid].keys() and mapinfo[mid]['title'] == m:
						hit = True
						ugc = 'UGC%s'%mapinfo[mid]['id']
						mapnames[ugc] = m
						ugcs.append(ugc)
			if not hit:
				res = post(incosurl.format(searchpattern=m))
				mapinfo = {}
				for l in res.text.split('\n'):
					if 'SharedFileBindMouseHover' in l:
						mid = 'UGC%s'%l.split('"')[1].split('_')[1]
						mapinfo[mid] = {}
						#print(mid)
						l = str(l.split('{')[1]).split('}')[0]
						for kv in l.split(','):
							if ':' in kv:
								k, v = list(kv.split(':'))[0], list(kv.split(':'))[1]
								mapinfo[mid][k.strip('"')] = v.strip('"')
						if 'title' in mapinfo[mid].keys() and mapinfo[mid]['title'] == m:
							ugc = 'UGC%s'%mapinfo[mid]['id']
							mapnames[ugc] = m
							ugcs[m] = ugc
		with open(expanduser(self.maptbl), 'w+') as mfh:
			mfh.write(ydump(mapnames, Dumper=Dumper))
		return ugcs

	def _getcash(self):
		c = 0
		while True:
			print('enter amount of cash (as number): ', end='')
			cash = input()
			if cash.isdigit():
				return cash
			c+=1
			if c < 3:
				error('thats not a number - let\'s try that again!')
			else:
				error('too dumb for numbers? o.0 aborting...')

	async def _cmdselects(self, srv):
		noargs = ['Info', 'ResetSND', 'RefreshList', 'RotateMap', 'ServerInfo', 'Help', 'Disconnect']
		steams = ['Kick', 'Ban', 'Unban', 'InspectPlayer']
		others = ['SwitchMap', 'SwitchTeam', 'GiveItem', 'GiveCash', 'GiveTeamCash', 'SetPlayerSkin', 'SetLimitedAmmoType']
		order = ['Info', 'SwitchMap', 'Kick', 'ResetSND', 'InspectPlayer', 'GiveItem', 'GiveCash', 'GiveTeamCash', 'SetPlayerSkin', 'SetLimitedAmmoType', 'RefreshList', 'ServerInfo',  'RotateMap', 'Ban', 'Unban']
		if self.hlp is None:
			hlp = await self.rconexec(srv, self.servers[srv][0], 'Help')
			if not hlp or 'Help' not in hlp.keys():
				return error('no or malformed help received from the server')
			hlp = hlp['Help']
			self.hlp = [h.split(' ')[0] for h in hlp.split(', ') if h.split(' ')[0]]
		opts = ['Info'] + [o for o in order if o in self.hlp and not o == 'Disconnect']
		opts = opts + [h for h in self.hlp if h not in opts + ['Disconnect']] + ['<Disconnect>']
		ask = [
            iList(
                'cmd',
                carousel=True,
                message='select command',
                choices=opts,
            ),
        ]
		try:
			cmd = list(prompt(ask).values())[0].strip()
		except AttributeError:
			exit()
		if cmd.strip('<>') in noargs:
			return cmd
		elif cmd in steams:
			sid = await self._getsteamid(srv, cmd)
			if not sid:
				return
			return '%s %s'%(cmd, sid)
		elif cmd in others:
			if cmd == 'SwitchMap':
				mapmod = await self._getmaps(srv)
				if not mapmod:
					return
				return 'SwitchMap %s'%mapmod
			elif cmd == 'SwitchTeam':
				sid = await self._getsteamid(srv, cmd)
				if not sid:
					return
				return 'SwitchTeam %s %s'%(sid, self._getteam())
			elif cmd == 'GiveItem':
				sid = await self._getsteamid(srv, cmd)
				if not sid:
					return
				return 'GiveItem %s %s'%(sid, self._getitem())
			elif cmd == 'GiveCash':
				sid = await self._getsteamid(srv, cmd)
				if not sid:
					return
				return 'GiveCash %s %s'%(sid, self._getcash())
			elif cmd == 'GiveTeamCash':
				team = self._getteam()
				if not team:
					return
				return 'GiveTeamCash %s %s'%(team, self._getcash())
			elif cmd == 'SetPlayerSkin':
				sid = await self._getsteamid(srv, cmd)
				if not sid:
					return
				return 'SetPlayerSkin %s %s'%(sid, self._getskin())
			elif cmd == 'SetLimitedAmmoType':
				ammo = self._getammotype()
				if not ammo:
					return
				return 'SetLimitedAmmoType %s'%ammo

	def _sid2name(self, sids):
		namesids = {}
		for s in sids:
			if sids.index(s) >= 1:
				sleep(1)
			s = s.strip()
			res, _ = Popen('curl -q https://steamdb.info/calculator/%s/'%s, stdout=PIPE, stderr=DEVNULL, shell=True).communicate()
			res = res.decode()
			for r in str(res).split('\n'):
				r = r.strip()
				if r.startswith('<title>'):
					n = r.split('>')[1].split(' · Steam Calculator')[0]
					namesids[n] = s
					break
		return namesids

	def _getbanlist(self, srv):
		if self.banlist is None:
			self.banlist = {}
			blacklist = ''
			if len(self.servers[srv]) >= 3:
				blacklist = self.servers[srv][2]
			if blacklist and blacklist.startswith('~'):
				blacklist = expanduser(blacklist)
			if (not blacklist.startswith('/') and not blacklist.startswith('C:\\')):
				error('cannot read blacklist if no absolute path is provided and', blacklist, 'is not!')
				return
			with open(blacklist, 'r') as bfh:
				banlist = bfh.readlines()
			self.banlist = self._sid2name([l for l in list(banlist) if l])
		return self.banlist

	async def _getsteamid(self, srv, cmd):
		userids = await self._players(srv)
		if cmd == 'Unban':
			if len(self.servers[srv]) < 3:
				print('no blacklist present - manual input required, ', end='')
				sid = None
				while True:
					print('enter steamid: ', end='')
					sid = input()
					if not sid.isdigit():
						error('need numeric value', sid, 'is, not')
						continue
					if not sid: return
					name = self._sid2name([sid])
					if name:
						name = list(name.keys())[0]
					print('are you sure you want to unban the player "%s" with steam-id the "%s"? [Y/n]'%(name, sid))
					yesno = input()
					if str(yesno).lower() in ('', 'y'):
						self.banlist = {}
						return sid
			userids = self._getbanlist(srv)
		if not userids:
			error('no player available to', cmd)
			return
		ask = [
            iList(
                'user',
                carousel=True,
                message='select user to %s'%cmd,
                choices=list(userids) + ['<Return>'],
            ),
        ]
		usr = list(prompt(ask).values())[0]
		if usr == '<Return>':
			return
		return userids[usr]

	async def _players(self, srv):
		pout = dict(await self.rconexec(srv, self.servers[srv][0], 'RefreshList'))
		if not isinstance(pout, dict) or not 'PlayerList' in pout.keys():
			return error('unexpected answer', pout)
		pout = pout['PlayerList']
		if self.dbg:
			print(bgre(pout))
		players = {}
		for p in pout:
			players[p['Username']] = p['UniqueId']
		return players

	async def _receive(self, socket):
		res = []
		while True:
			ret = socket.recv(1024)
			res.append(ret.decode())
			if len(ret) <= 1023:
				break
		return ''.join(res)

	async def _send(self, srv, passwd, data):
		server, port = srv.split(':')
		socket = sock(AF_INET, SOCK_STREAM)
		socket.settimeout(3)
		socket.connect((server, int(port)))
		#socket.sendall(''.encode())
		auth = await self._receive(socket)
		socket.sendall(passwd.encode())
		auth = await self._receive(socket)
		if str(auth).strip() != 'Authenticated=1':
			error('authentication failure')
		if self.dbg:
			print(bgre(auth))
		res = {}
		try:
			socket.sendall(data.encode())
			res = await self._receive(socket)
			if res:
				res = jload(res)
		except JSONDecodeError as err:
			res = res
		except TimeOutError:
			self.cnt += 1
			if self.cnt >= 2:
				self.cnt = 0
				return error('we ran into a timeout wile executing', data, 'too often - aborting...')
			error('we ran into a timeout wile executing', data, '- retrying...')
			res = await self._send(srv, passwd, data)
		finally:
			socket.close()
		return res


	async def rconexec(self, srv, pwd, cmd):
		if self.dbg:
			print(bgre('%s %s'%(srv, cmd)))
		if cmd == 'Info':
			res = await self._send(srv, pwd, 'ServerInfo')
			res = res['ServerInfo']
			lbl = await self._getmapname(res['MapLabel'])
			res['MapName'] = lbl
			pls = await self._players(srv)
			res['PlayerList'] = pls
			maps = await self._getmaps(srv, True)
			res['MapList'] = maps
			res = {'Info': res}
		else:
			res = await self._send(srv, pwd, cmd)
		if isinstance(res, dict):
			res = dict((k, v) for (k,v) in sorted(res.items()))
		return res


class DiscordADM(DiscordClient, commands.Cog, PavlovADM):
	"""
	Provides aliases for RCON-Commands executed via discord messages.\n
	RCONCommand | Alias | Description'
	"""
	dsc = True
	dbg = False
	srv = None
	log = getLogger()
	log.level = DEBUG
	emoji = ''
	channel = ''
	botruns = None
	initmpl = ''
	sertmpl = ''
	servers = {}
	ugcmaps = {}
	mapstbl = ''
	rconcfg = ''
	servdir = ''
	rconroles = []
	botcfg = {}
	config = pjoin(expanduser('~'), '.config', 'pavlovadm', 'pavlovadm.conf')
	cache = pjoin(expanduser('~'), '.cache', 'pavlovadm')
	cfgdir = dirname(config)
	servers = {}
	gameini = pjoin(cfgdir, 'Game.ini')
	itemtbl = pjoin(cfgdir, 'BalancingTable.csv')
	maptbl = pjoin(cache, 'maps.tbl')
	def __init__(self, bot, **kwargs):
		for (k, v) in kwargs.items():
			if hasattr(self, k):
				if str(v).startswith('~'):
					v = expanduser(v)
				if k == 'config':
					self.cfgdir = dirname(v)
				setattr(self, k, v)
		self.botcfg['blacklistchannel'] = '' if 'blacklistachnnel' not in self.botcfg.keys() else self.botcfg['blacklistchannel']
		self.bot = bot
		super().__init__()
		if self.dbg:
			self.log.level = DEBUG
			print(bgre(DiscordADM.__mro__))
			print(bgre(tabd(DiscordADM.__dict__, 2)))
			print(' ', bgre(self.__init__))
			print(bgre(tabd(self.__dict__, 4)))

	def servlist(self):
		srvs = {}
		try:
			with open(self.config, 'r') as sfh:
				srvs = yload(sfh.read(), Loader=Loader)
		except FileNotFoundError:
			with open(self.config, 'w+') as sfh:
				sfh.write(ydump({}, Dumper=Dumper))
		return srvs

	def _srvsearch(self, key, val):
		for (name, srvinfo) in self.servlist().items():
			if name == 'state': continue
			if key in srvinfo.keys() and srvinfo[key] == val:
				return {name: srvinfo}

	async def checkperms(self, chat):
		for perm in self.botcfg['rconroles']:
			if perm in [str(r) for r in chat.author.roles]:
				return True

	async def prechecks(self, chat):
		if str(chat.channel) != self.channel:
			self.srv = None
			self.maps = None
			self.banlist = None
			self.hlp = None
			self.channel = chat.channel
		if (chat.author == self.user) or \
              (chat.guild and chat.guild.name != self.botcfg['server']):
			return False
		grant = self.checkperms()
		self.log.info('#%s(%s|%s): %s'%(str(chat.channel), str(chat.author), grant, str(chat)))
		if not grant:
			await chat.author.send('du kommst nisch in #RCON rein brudi - brauchst du krass rolle un so - schwierr ab!')
			return False

	async def slicsend(self, chat, msg):
		if len(msg) > 1999:
			frag = []
			count = 0
			for line in msg.split('\n'):
				count = count+1+len(line)
				if count <= 1999:
					frag.append(line)
				elif len(line) > 1999:
					lfrag = []
					lcount = 0
					for word in line.split(' '):
						lcount = lcount+1+len(word)
						if lcount <= 1999:
							lfrag.append(word)
						else:
							await chat.channel.send(' '.join(lfrag))
							lfrag = [word]
							lcount = len(word)+1
					if lfrag:
						await chat.channel.send('\n'.join(lfrag))
				else:
					await chat.channel.send('\n'.join(frag))
					frag = [line]
					count = len(line)+1
			if frag:
				await chat.channel.send('\n'.join(frag))
			return
		if isinstance(msg, dict):
			msg = tabd(msg)
		await chat.channel.send(msg)

	def _banmessage(self, chat, msg):
		if chat.author == self.user: return
		for l in str(msg).split():
			l = l.strip()
			if l.startswith('http'):
				sid = l.rstrip('/').split('/')[-1]
				if sid.isdigit():
					return sid

	@commands.Cog.listener()
	async def on_message(self, chat):
		if str(chat.channel) == self.botcfg['blacklistchannel']:
			sids = []
			async for msg in chat.channel.history(limit=None, oldest_first=True):
				sid = self._banmessage(chat, str(msg.content))
				if not sid:
					continue
				reac = await msg.add_reaction('✅')
				sids.append(sid)
			for (k, v) in dict((k,v) for (k, v) in self.servers.items() if len(v) == 4).items():
				blst = expanduser(v[2])
				with open(blst, 'r') as bfh:
					bsids = [l.strip() for l in bfh.readlines()]
				for sid in sids:
					if sid not in bsids:
						bsids.append(sid)
					res = await self.rconexec(k, v[0], 'Ban %s'%sid)
				for sid in bsids:
					if sid not in sids:
						bsids = [s for s in bsids if s != sid]
				with open(blst, 'w+') as bfh:
					bfh.write('\n'.join(bsids))

	@commands.command()
	async def switch(self, chat, sth, mapid, *mode):
		"""|| SwitchMap => /switch $UGCID $MODE"""
		granted = await self.prechecks(chat)
		if granted:
			print(chat)
		srv = [k for (k, v) in self.servers.items() if len(v) == 4 and str(chat.channel) == v[3]]
		inf = srv if not srv else self.servers[srv[0]]
		res = await self.rconexec(srv[0], inf[0], 'SwitchMap %s %s'%(sth, mapid))
		if res:
			await self.slicsend(chat, tabd(res))

	@commands.command()
	async def reset(self, chat, *_):
		"""|| ResetSND => /reset"""
		granted = await self.prechecks(chat)
		if not granted: return
		srv = [k for (k, v) in self.servers.items() if len(v) == 4 and str(chat.channel) == v[3]]
		inf = srv if not srv else self.servers[srv[0]]
		res = await self.rconexec(srv[0], inf[0], 'ResetSND')
		if res:
			await self.slicsend(chat, tabd(res))

	@commands.command()
	async def rotate(self, chat, *_):
		"""|| RotateMap => /rotate"""
		granted = await self.prechecks(chat)
		if not granted: return
		srv = [k for (k, v) in self.servers.items() if len(v) == 4 and str(chat.channel) == v[3]]
		inf = srv if not srv else self.servers[srv[0]]
		res = await self.rconexec(srv[0], inf[0], 'RotateMap')
		if res:
			await self.slicsend(chat, tabd(res))

	@commands.command()
	async def players(self, chat, *args):
		"""|| RefreshList => /players"""
		granted = await self.prechecks(chat)
		if not granted:
			return
		srv = [k for (k, v) in self.servers.items() if len(v) == 4 and str(chat.channel) == v[3]]
		inf = srv if not srv else self.servers[srv[0]]
		res = await self.rconexec(srv[0], inf[0], 'RefreshList')
		if res:
			await self.slicsend(chat, tabd(res))

	@commands.command()
	async def info(self, chat, *_):
		"""|| ServerInfo => /info"""
		_chat = await self.prechecks(chat)
		if not _chat:
			return
		srv = [k for (k, v) in self.servers.items() if len(v) == 4 and str(chat.channel) == v[3]]
		inf = srv if not srv else self.servers[srv[0]]
		res = await self.rconexec(srv[0], inf[0], 'Info')
		if res:
			await self.slicsend(chat, tabd(res))



def config(cfg):
	with open(cfg, 'r') as cfh:
		return yload(cfh.read(), Loader=Loader)

def cli(cfgs):
	app = PavlovADM(**cfgs)
	app.cmdloop()

def discordbot(cfgs):
	bot = commands.Bot(command_prefix='/', description='Discord bot feature of PavlovADM')
	#print(cfgs['botcfg'])
	bot.add_cog(DiscordADM(bot, **cfgs))
	bot.run(cfgs['botcfg']['token'])

def main():
	__me = 'pavlovadm'
	__dsc = '%s <by d0n@janeiskla.de> manages pavlov servers commands via it\'s rcon like admin interface'%__me
	cfgdir = expanduser('~/.config/%s'%__me)
	cacdir = expanduser('~/.cache/%s'%__me)
	try:
		makedirs(cfgdir)
	except FileExistsError:
		pass
	try:
		makedirs(cacdir)
	except FileExistsError:
		pass
	src = expanduser('~/.local/share/pavlovadm')
	lsrc = '/usr/local/share/pavlovadm'
	if not isdir(src):
		src = lsrc
	if isdir(src):
		for f in ('pavlovadm.conf', 'Game.ini', 'public.ini', 'BalancingTable.csv'):
			f = pjoin(src, f)
			if not isfile(f):
				f = '%s/%s'%(lsrc, basename(f))
				if not isfile(f):
					continue
			if not isfile('%s/%s'%(cfgdir, basename(f))):
				with open(expanduser(f), 'r') as lfh, open('%s/%s'%(cfgdir, basename(f)), 'w+') as gfh:
					gfh.write(lfh.read())
	cfgs = config('%s/%s.conf'%(cfgdir, __me))
	pars = ArgumentParser(description=__dsc)
	pars.add_argument(
        '--version',
        action='version', version='%s v%s'%(__me, version))
	pars.add_argument(
        '-D', '--debug',
        dest='dbg', action='store_true', help='enable debugging')
	pars.add_argument(
        '-d', '--discord',
        dest='dsc', action='store_true', help='run discord bot')
	args = pars.parse_args()
	if args.dbg:
		cfgs['dbg'] = True
	if args.dsc:
		cfgs['dsc'] = True
		discordbot(cfgs)
		exit()
	cli(cfgs)


if __name__ == '__main__':
	main()
