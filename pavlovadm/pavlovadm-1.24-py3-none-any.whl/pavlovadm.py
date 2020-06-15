#!/usr/bin/env python3

from os import \
    makedirs, environ

from os.path import \
    join as pjoin, \
    expanduser, isdir, \
    basename, isfile, dirname

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

from time import sleep

try:
    import readline
except (ImportError, ModuleNotFoundError):
    pass

from discord import Client as DiscordClient

from requests import post, get

from inquirer import prompt, List as iList

from cmd import Cmd

from pavlovadm.colortext import tabd, error, bgre
from pavlovadm.__pkginfo__ import version

class PavlovADM(Cmd):
	servers = {}
	gameini = ''
	itemtbl = ''
	maptbl = '~/.cache/pavlovadm/maps.tbl'
	mapnames = None
	banlist = None
	maps = None
	hlp = None
	cnt = 0
	dbg = None
	pwd = None
	def __init__(self, *args, **kwargs):
		self.use_rawinput = False
		for (k, v) in kwargs.items():
			if hasattr(self, k):
				setattr(self, k, v)
		super().__init__()
		self.serverselect()

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

	def serverselect(self):
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
			cmd = self._cmdselects(srv)
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
				res = self._players(srv)
			else:
				res = self.rconexec(srv, cmd.strip('<>'))
			if isinstance(res, dict):
				res = tabd(res)
			print(res)
		self.serverselect()

	def _getmapname(self, mapid):
		if self.mapnames and mapid in self.mapnames:
			return self.mapnames[mapid]
		url = 'https://steamcommunity.com/sharedfiles/filedetails/?id='
		res = post('%s%s'%(url, mapid.strip('UGC')))
		for l in res.text.split('\n'):
			if 'workshopItemTitle' in l:
				return l.split('>')[1].split('<')[0]

	def _getmaps(self, srv, noask=None):
		if self.maps is None or self.mapnames is None:
			maplst = self.gameini
			if len(self.servers[srv]) > 1:
				maplst = self.servers[srv][1]
			if maplst.startswith('~'):
				maplst = expanduser(maplst)
			if not maplst.startswith('/'):
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
				self.mapnames = {}
			for l in lines:
				if not l or not l.startswith('MapRotation'):
					continue
				ugcid = l.split('MapId')[1].split(',')[0]
				ugcid = ugcid.strip(' =",')
				gmmod = l.split('GameMode')[1].split(')')[0]
				gmmod = gmmod.strip(' ="')
				name = self._getmapname(ugcid)
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
            choices=[m for m in self.maps.keys()] + ['<Return>'],
          ),
        ]
		mapp = list(prompt(ask).values())[0]
		if mapp == '<Return>':
			return
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
		with open(expanduser(self.itemtbl), 'r') as ifh:
			items = [l.split(',')[0] for l in list(ifh.readlines())[1:]]
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

	def _cmdselects(self, srv):
		noargs = ['Info', 'ResetSND', 'RefreshList', 'RotateMap', 'ServerInfo', 'Help', 'Disconnect']
		steams = ['Kick', 'Ban', 'Unban', 'InspectPlayer']
		others = ['SwitchMap', 'SwitchTeam', 'GiveItem', 'GiveCash', 'GiveTeamCash', 'SetPlayerSkin', 'SetLimitedAmmoType']
		order = ['Info', 'SwitchMap', 'Kick', 'ResetSND', 'InspectPlayer', 'GiveItem', 'GiveCash', 'GiveTeamCash', 'SetPlayerSkin', 'SetLimitedAmmoType', 'RefreshList', 'ServerInfo',  'RotateMap', 'Ban', 'Unban']
		if self.hlp is None:
			hlp = self.rconexec(srv, 'Help')
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
			sid = self._getsteamid(srv, cmd)
			if not sid:
				return
			return '%s %s'%(cmd, sid)
		elif cmd in others:
			if cmd == 'SwitchMap':
				mapmod = self._getmaps(srv)
				if not mapmod:
					return
				return 'SwitchMap %s'%mapmod
			elif cmd == 'SwitchTeam':
				sid = self._getsteamid(srv, cmd)
				if not sid:
					return
				return 'SwitchTeam %s %s'%(sid, self._getteam())
			elif cmd == 'GiveItem':
				sid = self._getsteamid(srv, cmd)
				if not sid:
					return
				return 'GiveItem %s %s'%(sid, self._getitem())
			elif cmd == 'GiveCash':
				sid = self._getsteamid(srv, cmd)
				if not sid:
					return
				return 'GiveCash %s %s'%(sid, self._getcash())
			elif cmd == 'GiveTeamCash':
				team = self._getteam()
				if not team:
					return
				return 'GiveTeamCash %s %s'%(team, self._getcash())
			elif cmd == 'SetPlayerSkin':
				sid = self._getsteamid(srv, cmd)
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
		c = 0
		for s in sids:
			s = s.strip()
			res, _ = Popen('curl -q https://steamdb.info/calculator/%s/'%s, stdout=PIPE, stderr=DEVNULL, shell=True).communicate()
			res = res.decode()
			for r in str(res).split('\n'):
				r = r.strip()
				if r.startswith('<title>'):
					n = r.split('>')[1].split(' · Steam Calculator')[0]
					namesids[n] = s
					break
			c = c+1
			if c >= 2:
				sleep(2)
		return namesids

	def _getbanlist(self, srv):
		if self.banlist is None:
			self.banlist = {}
			blacklist = ''
			if len(self.servers[srv]) == 3:
				blacklist = self.servers[srv][2]
			if blacklist and blacklist.startswith('~'):
				blacklist = expanduser(blacklist)
			if not blacklist.startswith('/'):
				error('cannot read blacklist if no absolute path is provided and', blacklist, 'is not!')
				return
			with open(blacklist, 'r') as bfh:
				banlist = bfh.readlines()
			self.banlist = self._sid2name([l for l in list(banlist) if l])
		return self.banlist

	def _getsteamid(self, srv, cmd):
		userids = self._players(srv)
		if cmd == 'Unban':
			if len(self.servers[srv]) != 3:
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


	def _players(self, srv):
		pout = dict(self.rconexec(srv, 'RefreshList'))
		if not isinstance(pout, dict) or not 'PlayerList' in pout.keys():
			return error('unexpected answer', pout)
		pout = pout['PlayerList']
		if self.dbg:
			print(bgre(pout))
		players = {}
		for p in pout:
			players[p['Username']] = p['UniqueId']
		return players

	def _getresponse(self, socket):
		res = []
		while True:
			ret = socket.recv(1024)
			res.append(ret.decode())
			if len(ret) <= 1023:
				break
		return ''.join(res)

	def _send(self, srv, data):
		passwd = self.servers[srv][0]
		server, port = srv.split(':')
		socket = sock(AF_INET, SOCK_STREAM)
		socket.settimeout(3)
		socket.connect((server, int(port)))
		#socket.sendall(''.encode())
		auth = self._getresponse(socket)
		socket.sendall(passwd.encode())
		auth = self._getresponse(socket)
		if str(auth).strip() != 'Authenticated=1':
			error('authentication failure')
		if self.dbg:
			print(bgre(auth))
		res = {}
		try:
			socket.sendall(data.encode())
			res = self._getresponse(socket)
			if res:
				res = jload(res)
		except JSONDecodeError as err:
			if res.strip() != 'Goodbye':
				error('while parsing', res, 'an exception', err, 'occured')
		except TimeOutError:
			self.cnt += 1
			if self.cnt <= 2:
				error('we ran into a timeout wile executing', data, '- retrying...')
				res = self._send(srv, data)
			error('we ran into a timeout wile executing', data, 'too often - aborting...')
		finally:
			socket.close()
		return res

	def rconexec(self, srv, cmd):
		if self.dbg:
			print(bgre('%s %s'%(srv, cmd)))
		if cmd == 'Info':
			res = self._send(srv, 'ServerInfo')
			res = res['ServerInfo']
			res['MapName'] = self._getmapname(res['MapLabel'])
			res['PlayerList'] = self._players(srv)
			res['MapList'] = self._getmaps(srv, True)
			res = {'Info': res}
		else:
			res = self._send(srv, cmd)
		if isinstance(res, dict):
			res = dict((k, v) for (k,v) in sorted(res.items()))
		return res


class DiscordADM(DiscordClient, PavlovADM):
	dbg = False
	log = None
	botruns = None
	initmpl = ''
	sertmpl = ''
	servers = ''
	mapstbl = ''
	rconcfg = ''
	servdir = ''
	maxinstances = 20
	maxplayers = 60
	interval = 30
	bot = {}
	pvadmcfg = expanduser('~/.config/pavlovadm/pavlovadm.conf')
	cache = expanduser('~/.cache/pamama')
	_help = ''
	def __init__(self, *args, **kwargs):
		for (k, v) in kwargs.items():
			if hasattr(self, k):
				if str(v).startswith('~'):
					v = expanduser(v)
				setattr(self, k, v)
		super().__init__()
		if self.dbg:
			self.log.level = DEBUG
			print(bgre(MatchMaker.__mro__))
			print(bgre(tabd(MatchMaker.__dict__, 2)))
			print(' ', bgre(self.__init__))
			print(bgre(tabd(self.__dict__, 4)))


	#def default(self, line):
	#       if line == 'Disconnect':
	#               self.socket.close()
	#               self._login()
	#       else:
	#               out = self._send(line)




def config(cfg):
	with open(cfg, 'r') as cfh:
		return yload(cfh.read(), Loader=Loader)

def cli(cfgs):
	app = PavlovADM(**cfgs)
	app.cmdloop()

def discordbot(cfgs):
	bot = DiscordADM(**cfgs)
	bot.run(cfgs['bot']['token'])

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
		for f in ('%s/pavlovadm.conf'%src, '%s/Game.ini'%src, '%s/public.ini'%src, '%s/BalancingTable.csv'%src):
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
        dest='dsc', action='store_true', help='enable debugging')
	args = pars.parse_args()
	if args.dbg:
		cfgs['dbg'] = True
	if args.dsc:
		discordbot(cfgs)
		exit()
	cli(cfgs)


if __name__ == '__main__':
	main()
