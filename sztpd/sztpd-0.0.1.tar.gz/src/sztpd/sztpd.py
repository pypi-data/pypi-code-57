# Copyright (c) 2020 Watsen Networks.  All Rights Reserved.

_G='tested?'
_F='$0$'
_E='device'
_D='wn-sztpd-0:device'
_C='/'
_B='activation-code'
_A=None
import gc,tracemalloc,os,re,json,signal,asyncio,datetime,functools,pkg_resources
from .  import yl
from .dal import DataAccessLayer
from .rcsvr import RestconfServer
from passlib.hash import sha256_crypt
from .tenant import TenantViewHandler
from .rfc8572 import RFC8572ViewHandler
from .native import NativeViewHandler,Period,TimeUnit
loop=_A
sig=_A
def signal_handler(name):global loop;global sig;sig=name;loop.stop()
def run(debug,db_url,cacert_path):
	d=':transport';c='SIGHUP';b='0';a=True;U='use-for';T='x';S='1';O=cacert_path;N=db_url;E='';global loop;global sig;A=_A;B=_A;P=False
	try:A=DataAccessLayer(N,O)
	except (SyntaxError,AssertionError)as K:return 1
	except NotImplementedError as K:P=a
	else:B=A.opaque()
	if P==a:
		I=os.environ.get('SZTPD_MODE')
		if I!=_A:
			assert type(I)==str
			if I not in[b,S,T]:print('Unknown SZTPD_MODE value.  Must be 0, 1, or x.');return 1
			B=I
		else:
			print(E);V=pkg_resources.resource_filename('sztpd','LICENSE.txt');Q=open(V,'r');print(Q.read());Q.close();print('First time initialization.  Please accept the license terms.');print(E);print('By entering "Yes" below, you agree to be bound to the terms and conditions contained on this screen with Watsen Networks.');print(E);W=input('Please enter "Yes" or "No": ')
			if W!='Yes':print(E);print('Thank you for your consideration.');print(E);return 1
			print(E);print('Modes:');print('  1 - single-tenant');print('  x - multi-tenant');print(E);B=input('Please select mode: ')
			if B not in[S,T]:print('Unknown mode selection.  Please try again.');return 1
			print(E);print("Running SZTPD in mode '"+B+"'. (No more output expected)");print(E)
		try:A=DataAccessLayer(N,O,json.loads(getattr(yl,'nbi_'+B)()),'wn-sztpd-'+B,B)
		except Exception as K:raise K;return 1
	assert B!=_A;assert A!=_A;tracemalloc.start(25);loop=asyncio.get_event_loop();loop.add_signal_handler(signal.SIGHUP,functools.partial(signal_handler,name=c));loop.add_signal_handler(signal.SIGTERM,functools.partial(signal_handler,name='SIGTERM'));loop.add_signal_handler(signal.SIGINT,functools.partial(signal_handler,name='SIGINT'));loop.add_signal_handler(signal.SIGQUIT,functools.partial(signal_handler,name='SIGQUIT'))
	while sig is _A:
		J=[];F=A.handle_get_config_request(_C+A.app_ns+d);L=loop.run_until_complete(F)
		for D in L[A.app_ns+d]['listen']['endpoint']:
			if D[U][0]=='native-interface':
				C=NativeViewHandler(A,B,loop)
				if B==b:G=_C+A.app_ns+':device'
				elif B==S:G=_C+A.app_ns+':devices/device'
				elif B==T:G=_C+A.app_ns+':tenants/tenant/devices/device'
				C.register_create_callback(G,_handle_device_created);X=G+'/activation-code';C.register_change_callback(X,_handle_device_act_code_changed);C.register_subtree_change_callback(G,_handle_device_subtree_changed);C.register_somehow_change_callback(G,_handle_device_somehow_changed);C.register_delete_callback(G,_handle_device_deleted);C.register_periodic_callback(Period(24,TimeUnit.Hours),datetime.datetime(2000,1,1,0),_check_expirations);M=RestconfServer(loop,A,D,C)
			elif D[U][0]=='tenant-interface':Y=TenantViewHandler(C);M=RestconfServer(loop,A,D,Y)
			else:assert D[U][0]=='rfc8572-interface';R=json.loads(getattr(yl,'sbi_rfc8572')());Z=RFC8572ViewHandler(A,B,R,C);M=RestconfServer(loop,A,D,Z,R)
			J.append(M);del D;D=_A
		del L;L=_A;loop.run_forever()
		for H in J:F=H.app.shutdown();loop.run_until_complete(F);F=H.runner.cleanup();loop.run_until_complete(F);F=H.app.cleanup();loop.run_until_complete(F);del H;H=_A
		del J;J=_A
		if sig==c:sig=_A
	loop.close();del A;return 0
async def _handle_device_created(watched_node_path,jsob,jsob_data_path,nvh):
	B=jsob;assert type(B)==dict
	if jsob_data_path==_C:assert _D in B;A=B[_D]
	else:assert _E in B;A=B[_E]
	A['lifecycle-statistics']={'nbi-access-stats':{'created':datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),'num-times-modified':0},'sbi-access-stats':{'num-times-accessed':0}};A['bootstrapping-log']={}
	if _B in A and A[_B].startswith(_F):A[_B]=sha256_crypt.using(rounds=1000).hash(A[_B][3:])
async def _handle_device_act_code_changed(watched_node_path,jsob,jsob_data_path,nvh):
	A=jsob;assert type(A)==dict
	if jsob_data_path==_C:assert _D in A;B=A[_D]
	else:assert _E in A;B=A[_E]
	if _B in B and B[_B].startswith(_F):B[_B]=sha256_crypt.using(rounds=1000).hash(B[_B][3:])
async def _handle_device_subtree_changed(watched_node_path,jsob,jsob_data_path,nvh):raise NotImplementedError(_G)
async def _handle_device_somehow_changed(watched_node_path,jsob,jsob_data_path,nvh):raise NotImplementedError(_G)
async def _handle_device_deleted(data_path,nvh):0
def _check_expirations(nvh):0