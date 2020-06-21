# Copyright (c) 2020 Watsen Networks.  All Rights Reserved.

from __future__ import annotations
_Q='wn-sztpd-x:'
_P='Unable to parse "input" JSON document: '
_O='wn-sztpd-x'
_N='/wn-sztpd-x:tenants/tenant=[^ ]*'
_M='/wn-sztpd-x:tenants/tenant=[^/]*/'
_L='Top node names must begin with the "wn-sztpd-1" prefix.'
_K='wn-sztpd-1'
_J='name'
_I='wn-sztpd-1:'
_H='/wn-sztpd-x:tenants/tenant/0/'
_G='Non-root data_paths must begin with "/wn-sztpd-1:".'
_F='wn-sztpd-x:tenant'
_E='/wn-sztpd-x:tenants/tenant='
_D=':'
_C='/wn-sztpd-1:'
_B=None
_A='/'
import re,json,datetime,basicauth
from .  import yl
from .  import dal
from aiohttp import web
from .rcsvr import RestconfServer
from .handler import RouteHandler
from passlib.hash import sha256_crypt
class TenantViewHandler(RouteHandler):
	def __init__(A,native):A.native=native
	async def _check_auth(B,request):
		H='comment';G='failure';F='outcome';C=request;A={};A['timestamp']=datetime.datetime.utcnow();A['source-ip']=C.remote;A['source-proxies']=list(C.forwarded);A['host']=C.host;A['method']=C.method;A['path']=C.path;I=C.headers.get('AUTHORIZATION')
		if I is _B:A[F]=G;A[H]='No authorization specified in the HTTP header.';await B.native._insert_audit_log_entry(_B,A);return web.Response(status=401)
		D,L=basicauth.decode(I);O=_B
		try:E=await B.native.dal.get_tenant_name_for_admin(D)
		except dal.NodeNotFound as P:A[F]=G;A[H]='Unknown admin: '+D;await B.native._insert_audit_log_entry(_B,A);return web.Response(status=401)
		if E==_B:A[F]=G;A[H]='Host-level admins cannot use tenant interface ('+D+').';await B.native._insert_audit_log_entry(_B,A);return web.Response(status=401)
		M=_A+B.native.dal.app_ns+':tenants/tenant='+E+'/admin-accounts/admin-account='+D+'/password';N=await B.native.dal.handle_get_config_request(M);J=N[B.native.dal.app_ns+':password'];assert J.startswith('$5$')
		if not sha256_crypt.verify(L,J):A[F]=G;A[H]='Password mismatch for admin '+D;await B.native._insert_audit_log_entry(E,A);return web.Response(status=401)
		A[F]='success';await B.native._insert_audit_log_entry(E,A);K=web.Response(status=200);K.text=E;return K
	async def handle_get_opstate_request(F,request):
		E=request;M=E.path;A=M[RestconfServer.len_prefix_operational:]
		if A=='':A=_A
		elif A!=_A and A[-1]==_A:A=A[:-1]
		B=await F._check_auth(E)
		if B.status==401:return B
		J=B.text;B=await F.native.check_headers(E)
		if B!=_B:return B
		if A=='/ietf-yang-library:yang-library':D=web.Response(status=200);D.content_type='application/yang-data+json';D.text=getattr(yl,'nbi_x_tenant')();return D
		assert A==_A or A.startswith(_C)
		if A==_A:K=_E+J
		else:
			if not A.startswith(_C):D=web.Response(status=400);D.text=_G;return D
			P,L=A.split(_D,1);assert L!=_B;K=_E+J+_A+L
		B,C=await F.native.handle_get_opstate_request_lower_half(K,E.query_string)
		if C!=_B:
			assert B.status==200;G={}
			if A==_A:
				for H in C[_F][0].keys():
					if H==_J:continue
					G[_I+H]=C[_F][0][H]
			else:I=next(iter(C));assert I.count(_D)==1;N,O=I.split(_D);assert N==_O;assert type(C)==dict;assert len(C)==1;G[_I+O]=C[I]
			B.text=json.dumps(G,indent=2)
		return B
	async def handle_get_config_request(E,request):
		D=request;M=D.path;A=M[RestconfServer.len_prefix_running:]
		if A=='':A=_A
		elif A!=_A and A[-1]==_A:A=A[:-1]
		B=await E._check_auth(D)
		if B.status==401:return B
		I=B.text;B=await E.native.check_headers(D)
		if B!=_B:return B
		assert A==_A or A.startswith(_C)
		if A==_A:J=_E+I
		else:
			if not A.startswith(_C):K=web.Response(status=400);K.text=_G;return K
			P,L=A.split(_D,1);assert L!=_B;J=_E+I+_A+L
		B,C=await E.native.handle_get_config_request_lower_half(J,D.query_string)
		if C!=_B:
			assert B.status==200;F={}
			if A==_A:
				for G in C[_F][0].keys():
					if G==_J:continue
					F[_I+G]=C[_F][0][G]
			else:H=next(iter(C));assert H.count(_D)==1;N,O=H.split(_D);assert N==_O;assert type(C)==dict;assert len(C)==1;F[_I+O]=C[H]
			B.text=json.dumps(F,indent=2)
		return B
	async def handle_post_config_request(F,request):
		D=request;K=D.path;B=K[RestconfServer.len_prefix_running:]
		if B=='':B=_A
		elif B!=_A and B[-1]==_A:B=B[:-1]
		C=await F._check_auth(D)
		if C.status==401:return C
		H=C.text;C=await F.native.check_headers(D)
		if C!=_B:return C
		if B==_A:I=_E+H
		else:
			if not B.startswith(_C):A=web.Response(status=400);A.text=_G;return A
			P,J=B.split(_D,1);assert J!=_B;I=_E+H+_A+J
		try:E=await D.json()
		except json.decoder.JSONDecodeError as L:A=web.Response(status=400);A.text=_P+str(L);return A
		assert type(E)==dict;assert len(E)==1;G=next(iter(E));assert G.count(_D)==1;M,N=G.split(_D)
		if M!=_K:A=web.Response(status=400);A.text=_L;return A
		O={_Q+N:E[G]};A=await F.native.handle_post_config_request_lower_half(I,D.query_string,O)
		if A.status!=201:
			if'/wn-sztpdex:tenants/tenant/0/'in A.text:A.text=A.text.replace(_H,_C)
			elif _E in A.text:A.text=re.sub(_M,_C,A.text);A.text=re.sub(_N,_C,A.text)
		return A
	async def handle_put_config_request(F,request):
		E=request;M=E.path;B=M[RestconfServer.len_prefix_running:]
		if B=='':B=_A
		elif B!=_A and B[-1]==_A:B=B[:-1]
		C=await F._check_auth(E)
		if C.status==401:return C
		G=C.text;C=await F.native.check_headers(E)
		if C!=_B:return C
		if B==_A:K=_E+G
		else:
			if not B.startswith(_C):A=web.Response(status=400);A.text=_G;return A
			S,L=B.split(_D,1);assert L!=_B;K=_E+G+_A+L
		try:D=await E.json()
		except json.decoder.JSONDecodeError as N:A=web.Response(status=400);A.text=_P+str(N);return A
		if B==_A:
			H={_F:[{_J:G}]}
			for I in D.keys():
				assert I.count(_D)==1;O,P=I.split(_D)
				if O!=_K:A=web.Response(status=400);A.text=_L;return A
				H[_F][0][P]=D[I]
		else:
			assert type(D)==dict;assert len(D)==1;J=next(iter(D));assert J.count(_D)==1;Q,R=J.split(_D)
			if Q!=_K:A=web.Response(status=400);A.text=_L;return A
			H={_Q+R:D[J]}
		A=await F.native.handle_put_config_request_lower_half(K,E.query_string,H)
		if A.status!=204:
			if _H in A.text:A.text=A.text.replace(_H,_C)
			elif _E in A.text:A.text=re.sub(_M,_C,A.text);A.text=re.sub(_N,_C,A.text)
		return A
	async def handle_delete_config_request(D,request):
		E=request;I=E.path;B=I[RestconfServer.len_prefix_running:]
		if B=='':B=_A
		elif B!=_A and B[-1]==_A:B=B[:-1]
		C=await D._check_auth(E)
		if C.status==401:return C
		F=C.text;C=await D.native.check_headers(E)
		if C!=_B:return C
		if B==_A:G=_E+F
		else:
			if not B.startswith(_C):A=web.Response(status=400);A.text=_G;return A
			J,H=B.split(_D,1);assert H!=_B;G=_E+F+_A+H
		A=await D.native.handle_delete_config_request_lower_half(G)
		if A.status!=204:
			if _H in A.text:A.text=A.text.replace(_H,_C)
			elif _E in A.text:A.text=re.sub(_M,_C,A.text);A.text=re.sub(_N,_C,A.text)
		return A
	async def handle_action_request(A,request):0
	async def handle_rpc_request(A,request):0