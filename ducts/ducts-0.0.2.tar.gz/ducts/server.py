#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from pathlib import Path
from datetime import datetime, timedelta
from io import StringIO
from io import BytesIO
from collections import namedtuple
from enum import Enum
import hashlib

import importlib
import inspect
import functools

import msgpack
import json

import asyncio
import aiohttp
from aiohttp import web
import aiohttp_remotes
import aiofiles
from http import HTTPStatus
import mimetypes

from ifconf import configure_module, config_callback

from ducts.context import ServerContext
from ducts.event import Event, EventSession, HandleType

import logging
        
@config_callback
def config(loader):
    loader.add_attr_boolean('behind_nginx', False, help='True if use ducts behind nginx')
    loader.add_attr('httpd_addr', '0.0.0.0', help='inet address to bind')
    loader.add_attr_int('httpd_port', 8080, help='inet port to bind')
    loader.add_attr_path('ducts_home', Path('.'), help='root directory of all local path')
    loader.add_attr_path('local_path_static', Path('./htdocs'), help='local path for static root')

    loader.add_attr_path('module_path_libs', Path('./libs'), help='module path for html/javascript files')
    loader.add_attr_list('web_lib_file_extensions', ['.js', '.html', '.css'], help='web library file extensions')
    loader.add_attr_path('module_path_jsonp_template', Path('./assets/jsonp_template.js'), help='')
    loader.add_attr_path('module_path_favicon', Path('./assets/favicon.ico'), help='')
    
    loader.add_attr('root_path_ducts', '/ducts/', help='URL path for all path')
    loader.add_attr('root_path_static', '/static/', help='URL path for static_root')
    loader.add_attr('root_path_favicon', '/favicon.ico', help='')
    loader.add_attr('relative_path_libs_dir', 'libs', help='URL path for html/javascript files')
    loader.add_attr('relative_path_web_service_discovery', 'wsd', help='where web service discovery is located')
    loader.add_attr('relative_path_web_service_main_jsonp', 'main', help='where main web service is located')
    loader.add_attr('relative_path_event_spec', 'events.json', help='where event descriptions json is located')
    loader.add_attr('relative_path_api', 'api/v1/', help='')
    loader.add_attr('relative_path_websocket', 'ws/v1/', help='')
    loader.add_attr('api_path_event', 'event', help='')
    loader.add_attr('api_path_event_id', 'event/{event_id}', help='')
    loader.add_attr('jsonp_callback_query', 'callback', help='')
    loader.add_attr('jsonp_callback_default', 'callback', help='')

    
@config_callback('web_service_discovery')
def wsd_config(loader):
    loader.add_attr('websocket_host', '{ws_host}', help='')
    loader.add_attr('websocket_url', '{ws_scheme}://{ws_host}{root_path_websocket}', help='')
    loader.add_attr('api_host', '{api_host}', help='')
    loader.add_attr('api_url_root', '{api_scheme}://{api_host}{root_path_api}', help='')
    loader.add_attr('api_url_event', '{api_scheme}://{api_host}{root_path_api}{api_path_event}', help='')

@config_callback('web_socket_server')
def wsserver_config(loader):
    loader.add_attr_int('ping_pong_interval', 3, help='interval to send ping msg after pong msg received')

    
class HttpdServer(object):

    def __init__(self, loop):
        self.logger = logging.getLogger(__name__).getChild('httpd')
        self.conf = configure_module(config)
        self.context = ServerContext(loop, self.conf.ducts_home)
        self.root_path_ducts = Path(self.conf.root_path_ducts)
        self.wsd = configure_module(wsd_config)
        self.wsd_dict = self.wsd._asdict()
        with open(self._module_path(self.conf.module_path_jsonp_template), 'r') as f:
            self.jsonp_template = f.read()
        with open(self._module_path(self.conf.module_path_favicon), 'rb') as f:
            self.favicon = f.read()
        self.wss = WebSocketServer(self.context)
        self.app = web.Application(loop=self.context.loop)
        self.md5 = hashlib.md5()
        self.setup_route()

    def _module_path(self, path):
        return path.resolve() if path.is_absolute() else Path(__file__).parent.joinpath(path).resolve()

    def _root_path_for(self, path, is_dir = False):
        return str(self.root_path_ducts.joinpath(path)) + ('/' if is_dir else '')

    def _root_path_for_websocket(self):
        return self._root_path_for(self.conf.relative_path_websocket, True)
        
    def _root_path_for_api(self):
        return self._root_path_for(self.conf.relative_path_api, True)
        
    def _root_path_for_libs(self):
        return self._root_path_for(self.conf.relative_path_libs_dir, True)
        
    def setup_route(self):
        self.app.router.add_static(self.conf.root_path_static, path=str(self.context.resolve_local_path(self.conf.local_path_static)), name='static', show_index=True)
        self.app.router.add_get(self.conf.root_path_favicon, lambda request: web.Response(body=self.favicon, content_type='image/x-icon'))
        for lib_file in [p for p in self._module_path(self.conf.module_path_libs).glob('**/*') if re.match('.*({})'.format('|'.join(self.conf.web_lib_file_extensions)),str(p))]:
            with open(lib_file, 'rb') as f:
                buf = f.read()
                self.md5.update(buf)
                checksum = self.md5.hexdigest()
                f = functools.partial((lambda src, mt, request : web.Response(body=src, content_type=mt, headers={'ETag':checksum})), buf, mimetypes.guess_type(str(lib_file))[0])
            self.app.router.add_get(self._root_path_for_libs() + lib_file.name, f)
        self.app.router.add_get(self._root_path_for_libs() + self.conf.relative_path_event_spec
                                , lambda request: web.json_response([s._asdict() for s in self.context.event_handler_manager.specs]))
        self.app.router.add_get(self._root_path_for(self.conf.relative_path_web_service_discovery), self.get_web_service_discovery)
        self.app.router.add_get(self._root_path_for(self.conf.relative_path_web_service_main_jsonp), self.get_web_service_main_jsonp)
        self.app.router.add_get(self._root_path_for_websocket(), self.wss.websocket_handler)
        self.app.router.add_get(self._root_path_for_api()+self.conf.api_path_event, self.handle_event)
        self.app.router.add_get(self._root_path_for_api()+self.conf.api_path_event_id, self.handle_event_id)

    async def run(self):
        if self.conf.behind_nginx:
            await aiohttp_remotes.setup(self.app, aiohttp_remotes.XForwardedRelaxed())
        self.handler = self.app.make_handler()
        self.srv = await self.context.loop.create_server(self.handler, self.conf.httpd_addr, self.conf.httpd_port)
        self.logger.notice('START|SOCKET=%s', self.srv.sockets[0].getsockname())
        await self.context.redis.connect()

    def close(self):
        self.context.close()
        self.srv.close()
        self.context.run_until_complete(self.srv.wait_closed())
        self.context.run_until_complete(self.app.shutdown())
        self.context.run_until_complete(self.handler.shutdown(60.0))
        self.context.run_until_complete(self.app.cleanup())
        self.logger.notice('CLOSED')

    async def get_web_service_discovery(self, request):
        return web.json_response(self._create_wsd_dict(request), status=HTTPStatus.OK.value)

    async def get_web_service_main_jsonp(self, request):
        params = request.rel_url.query
        callback = params.get(self.conf.jsonp_callback_query, self.conf.jsonp_callback_default)
        libs = self._root_path_for_libs()
        script = self.jsonp_template.replace('__TEMPLATE_DUCTS_LIBS__', libs).replace('__TEMPLATE_CALLBACK__', callback).replace('__TEMPLATE_WSD__', json.dumps(self._create_wsd_dict(request)))
        res = web.Response(body=script, content_type='application/javascript')
        res.last_modified = datetime.now()
        return res
        
    async def handle_event(self, request):
        return web.json_response(self.context.event_handler_manager.key_ids)

    async def handle_event_id(self, request):
        operation = request.match_info['event_id']
        params = request.rel_url.query['args'].strip().split()
        return web.json_response({'result' : await self.redis.execute(operation, params)})

    def _create_wsd_dict(self, request):
        params = self.conf._asdict()
        params['root_path_websocket'] = self._root_path_for_websocket()
        params['ws_host'] = request.host
        params['ws_scheme'] = 'wss' if request.secure else 'ws'
        params['root_path_api'] = self._root_path_for_api()
        params['api_host'] = request.host
        params['api_scheme'] = request.scheme
        your_wsd = namedtuple('wsd', ' '.join(self.wsd_dict.keys()))(*[v.format(**params) if type(v) is str else v for v in self.wsd_dict.values()])
        your_wsd_dict = your_wsd._asdict()
        your_wsd_dict['EVENT'] = self.context.event_handler_manager.key_ids
        return your_wsd_dict

    
class WebSocketSession():

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.peername = request.transport.get_extra_info('peername')
        self.peername = "{}:{}".format(self.peername[0], self.peername[1])
        self.logger = logging.getLogger(__name__).getChild('ws').getChild(self.peername)

    async def prepare(self):
        self.socket = web.WebSocketResponse()
        await self.socket.prepare(self.request)
        asyncio.ensure_future(self.ping())

    async def ping(self):
        await self.socket.ping()

class WebSocketEventSession(EventSession):

    def __init__(self, session, msg, request_id, event_id, data):
        super().__init__(session.context.event_handler_manager)
        self.logger = logging.getLogger(__name__).getChild('event').getChild(str(event_id)).getChild(session.peername).getChild(str(id(msg)))
        self.context = session.context
        self.request = session.request
        self.peername = session.peername
        self.socket = session.socket
        self._msg_id = id(msg)
        self._request_id = request_id
        self._event_id = event_id
        self._event_data = data
        
    async def is_closed(self):
        self.logger.debug('IS_CLOSED=%s', self.socket.closed)
        return self.socket.closed

    def request_id(self):
        return self._request_id

    def session_id(self):
        return self.peername

    #need to await
    def log_message(self, request_id, event_id, data):
        return 


    async def send_bytes(self, request_id, event_id, data, loop = False):
        if data is None:
            self.logger.debug("SEND_BYTES_IGNORE|SOCKET=%s", not self.socket.closed)
            return not self.socket.closed
        try:
            self.logger.debug("SEND_BYTES_AWAIT|DATA=%s", type(data))
            await self.socket.send_bytes(msgpack.packb([request_id, event_id, data]))
            self.logger.debug("SEND_BYTES_DONE|NEXT=%s", loop)
        except Exception as e:
            self.logger.exception("SEND_BYTES_ERROR=%s", e)
            try:
                await self.socket.close()
            except Exception as e:
                self.logger.exception("SOCKET_CLOSE_ERROR=%s", e)
            return False
        else:
            return True

    async def send_str(self, data):
        await session.socket.send_str(data)
        
    
class WebSocketServer(object):
    
    def __init__(self, context):
        self.conf = configure_module(wsserver_config)
        self.context = context
        self.wsmsg_handler = {msg_type : lambda : self._default_wsmsg_handler
                              for msg_type in [getattr(aiohttp.WSMsgType, attr) for attr in dir(aiohttp.WSMsgType)]
                              if type(msg_type) is aiohttp.WSMsgType}
        self.wsmsg_handler[aiohttp.WSMsgType.BINARY] = lambda : self._msgpack_msg_handler
        #self.wsmsg_handler[aiohttp.WSMsgType.CONTINUATION] = lambda : self._msgpack_msg_handler
        self.wsmsg_handler[aiohttp.WSMsgType.TEXT] = lambda : self._default_textmsg_handler
        self.wsmsg_handler[aiohttp.WSMsgType.PING] = lambda : self._pingmsg_handler
        self.wsmsg_handler[aiohttp.WSMsgType.PONG] = lambda : self._pongmsg_handler
        self.wsmsg_handler[aiohttp.WSMsgType.CLOSE] = lambda : self._closemsg_handler

        self.event_handler = [None for v in HandleType]
        self.event_handler[HandleType.ALIVE_MONITORING.value] = self._event_handler_alive_monitoring
        self.event_handler[HandleType.ASYNC_FOR.value] = self._event_handler_async_for
        self.event_handler[HandleType.FOR.value] = self._event_handler_for
        self.event_handler[HandleType.ASYNC.value] = self._event_handler_async
        self.event_handler[HandleType.SYNC.value] = self._event_handler_sync

    async def websocket_handler(self, request):
        session = WebSocketSession(self.context, request)
        session.logger.debug("REQUEST")
        await session.prepare()
        session.logger.info('START')
        async for msg in session.socket:
            session.logger.debug('MSG=%s|START|TYPE=%s', id(msg), str(msg.type))
            handle = self.wsmsg_handler[msg.type]()
            try:
                assert inspect.iscoroutinefunction(handle), 'handle must be async function'
                asyncio.ensure_future(handle(session, msg))
            except Exception as e:
                session.logger.exception('MSG=%s|HANDLE=%s|ERROR=%s', id(msg), handle, e)
            session.logger.debug('MSG=%s|NEXT', id(msg))
        session.logger.info('MSG=%s|END|TYPE=%s', id(msg), str(msg.type))
        return session.socket

    async def _default_pingmsg_handler(self, session, msg):
        session.logger.debug("MSG=%s|PING", id(msg))
        await session.socket.pong()

    async def _default_pongmsg_handler(self, session, msg):
        session.logger.debug("MSG=%s|PONG", id(msg))
        await asyncio.sleep(self.conf.ping_pong_interval)
        await session.socket.ping()

    async def _default_closemsg_handler(self, session, msg):
        session.logger.debug("MSG=%s|CLOSE", id(msg))

    async def _default_wsmsg_handler(self, session, msg):
        session.logger.debug("MSG=%s|UNHNADLED", id(msg))
        await session.socket.send_str('N/A')
        
    async def _msgpack_msg_handler(self, socket_session, msg):
        request_id, event_id, data = msgpack.unpackb(msg.data)
        event_id = int(event_id)
        session = WebSocketEventSession(socket_session, msg, request_id, event_id, data)
        session.logger.info("REQUEST=%s|TYPE=%s|LEN=%s", request_id, type(data), len(data) if hasattr(data, '__len__') else 0)
        try:
            handle_type, handler = self.context.event_handler_manager.get_handler_for(event_id)
            await self.event_handler[handle_type.value](session, msg, request_id, event_id, data, handler.handle, Event(event_id, session, data))
            session.logger.info("END".format(session.peername, id(msg), event_id))
        except Exception as e:
            session.logger.exception("END|ERROR=%s".format(e))
            if not await session.is_closed():
                event_id = -1 * event_id
                ret = '{}:{}'.format(e.__class__.__name__, e.args)
                await session.send_bytes(request_id, event_id, ret)
                

    async def _event_handler_alive_monitoring(self, session, msg, request_id, event_id, data, handle, event):
        session.logger.debug("START|ALIVE_MONITORING")
        async for ret in handle(event):
            try:
                await session.socket.send_bytes(msgpack.packb([request_id, event_id, ret]))
                if session.request.transport:
                    is_closing = session.request.transport.is_closing()
                    session.logger.debug("ALIVE_MONITORING|TRANSPORT=%s|IS_CLOGING=%s", session.request.transport, is_closing)
                    if is_closing:
                        break
                else:
                    session.logger.debug("ALIVE_MONITORING|TRANSPORT=None")
                    break
            except Exception as e:
                session.logger.debug("ALIVE_MONITORING|ERROR=%s", e)
        session.logger.debug("START_CLOSE_HANDLERS")
        closed = await asyncio.gather(*[f for f in [h[1].handle_closed(session) for h in session.manager.handlers()] if inspect.isawaitable(f)])
        session.logger.info("HANDLER_CLOSED=%s", closed)
            
    async def _event_handler_async_for(self, session, msg, request_id, event_id, data, handle, event):
        session.logger.debug("START|AWAIT_ASYNC_LOOP")
        async for ret in handle(event):
            await session.send_bytes(request_id, event_id, ret, True)

    async def _event_handler_async_for(self, session, msg, request_id, event_id, data, handle, event):
        session.logger.debug("START|AWAIT_ASYNC_LOOP")
        async for ret in handle(event):
            await session.send_bytes(request_id, event_id, ret, True)

    async def _event_handler_for(self, session, msg, request_id, event_id, data, handle, event):
        session.logger.debug("START|SYNC_LOOP")
        for ret in handle(event):
            await session.send_bytes(request_id, event_id, ret, True)

    async def _event_handler_async(self, session, msg, request_id, event_id, data, handle, event):
        session.logger.debug("START|AWAIT_ASYNC_HANDLE")
        ret = await handle(event)
        await session.send_bytes(request_id, event_id, ret)

    async def _event_handler_sync(self, session, msg, request_id, event_id, data, handle, event):
        session.logger.debug("START|SYNC_HANDLE")
        ret = handle(event)
        await session.send_bytes(request_id, event_id, ret)

        
