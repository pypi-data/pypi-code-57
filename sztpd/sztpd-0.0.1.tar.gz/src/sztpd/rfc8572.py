# Copyright (c) 2020 Watsen Networks.  All Rights Reserved.

from __future__ import annotations
_o='ietf-sztp-bootstrap-server'
_n='urn:ietf:params:xml:ns:yang:ietf-sztp-bootstrap-server'
_m='Unable to parse "input" JSON document: '
_l='application/*'
_k='*/*'
_j='ssl_object'
_i='Resource does not exist.'
_h='Requested resource does not exist.'
_g=':log-entry'
_f='/devices/device='
_e=':devices/device='
_d='webhooks'
_c='ietf-sztp-bootstrap-server:input'
_b='Parent node does not exist.'
_a='Resource can not be modified.'
_Z='callback'
_Y='RPC "input" node fails YANG validation here: '
_X=True
_W='name'
_V='passed-input'
_U=':device'
_T='1'
_S=':tenants/tenant='
_R='x'
_Q='reference'
_P='dynamic-callout'
_O='Accept'
_N='return-code'
_M='error-message'
_L='path'
_K='method'
_J='source-ip'
_I='timestamp'
_H='application/yang-data+xml'
_G='Content-Type'
_F='application/yang-data+json'
_E='0'
_D=':dynamic-callout'
_C='/'
_B='event-details'
_A=None
import json,base64,pprint,aiohttp,yangson,datetime,basicauth,pkg_resources
from .  import yl
from .  import dal
from .  import utils
from aiohttp import web
from pyasn1.type import univ
from .dal import DataAccessLayer
from .rcsvr import RestconfServer
from .handler import RouteHandler
from pyasn1_modules import rfc5652
from passlib.hash import sha256_crypt
from pyasn1.codec.der.encoder import encode as encode_der
from pyasn1.codec.der.decoder import decode as der_decoder
from certvalidator import CertificateValidator,ValidationContext,PathBuildingError
class RFC8572ViewHandler(RouteHandler):
	len_prefix_running=len(RestconfServer.root+'/ds/ietf-datastores:running');len_prefix_operational=len(RestconfServer.root+'/ds/ietf-datastores:operational');len_prefix_operations=len(RestconfServer.root+'/operations');id_ct_sztpConveyedInfoXML=rfc5652._buildOid(1,2,840,113549,1,9,16,1,42);id_ct_sztpConveyedInfoJSON=rfc5652._buildOid(1,2,840,113549,1,9,16,1,43)
	def __init__(A,dal,mode,yl,nvh):A.dal=dal;A.mode=mode;A.nvh=nvh;B=pkg_resources.resource_filename('sztpd','yang/');A.dm=yangson.DataModel(json.dumps(yl),[B])
	async def _insert_bootstrapping_log_entry(A,device_id,bootstrapping_log_entry):
		E='/bootstrapping-log';B=device_id
		if A.mode==_E:C=_C+A.dal.app_ns+':device/bootstrapping-log'
		elif A.mode==_T:C=_C+A.dal.app_ns+_e+B[0]+E
		elif A.mode==_R:C=_C+A.dal.app_ns+_S+B[1]+_f+B[0]+E
		D={};D[A.dal.app_ns+_g]=bootstrapping_log_entry;await A.dal.handle_post_opstate_request(C,D)
	async def _insert_audit_log_entry(A,tenant_name,audit_log_entry):
		B=tenant_name
		if A.mode==_E or A.mode==_T or B==_A:C=_C+A.dal.app_ns+':audit-log'
		elif A.mode==_R:C=_C+A.dal.app_ns+_S+B+'/audit-log'
		D={};D[A.dal.app_ns+_g]=audit_log_entry;await A.dal.handle_post_opstate_request(C,D)
	async def handle_get_opstate_request(E,request):
		C=request;D=C.path[E.len_prefix_operational:];F=await E._check_auth(C,D)
		if F is _A:return web.Response(status=401)
		A={};A[_I]=datetime.datetime.utcnow();A[_J]=C.remote;A[_K]=C.method;A[_L]=C.path
		if D=='/ietf-yang-library:yang-library'or D==_C or D=='':B=web.Response(status=200);B.content_type=_F;B.text=getattr(yl,'sbi_rfc8572')()
		else:B=web.Response(status=400);B.text=_h;A[_M]=B.text
		A[_N]=B.status;await E._insert_bootstrapping_log_entry(F,A);return B
	async def handle_get_config_request(D,request):
		B=request;E=B.path[D.len_prefix_running:];F=await D._check_auth(B,E)
		if F is _A:return web.Response(status=401)
		A={};A[_I]=datetime.datetime.utcnow();A[_J]=B.remote;A[_K]=B.method;A[_L]=B.path
		if E==_C or E=='':C=web.Response(status=204)
		else:C=web.Response(status=400);C.text=_h;A[_M]=C.text
		A[_N]=C.status;await D._insert_bootstrapping_log_entry(F,A);return C
	async def handle_post_config_request(D,request):
		C=request;E=C.path[D.len_prefix_running:];F=await D._check_auth(C,E)
		if F is _A:return web.Response(status=401)
		A={};A[_I]=datetime.datetime.utcnow();A[_J]=C.remote;A[_K]=C.method;A[_L]=C.path
		if E==_C or E=='':B=web.Response(status=400);B.text=_a
		else:B=web.Response(status=404);B.text=_b
		A[_N]=B.status;A[_M]=B.text;await D._insert_bootstrapping_log_entry(F,A);return B
	async def handle_put_config_request(D,request):
		C=request;E=C.path[D.len_prefix_running:];F=await D._check_auth(C,E)
		if F is _A:return web.Response(status=401)
		A={};A[_I]=datetime.datetime.utcnow();A[_J]=C.remote;A[_K]=C.method;A[_L]=C.path
		if E==_C or E=='':B=web.Response(status=400);B.text=_a
		else:B=web.Response(status=404);B.text=_b
		A[_N]=B.status;A[_M]=B.text;await D._insert_bootstrapping_log_entry(F,A);return B
	async def handle_delete_config_request(D,request):
		C=request;E=C.path[D.len_prefix_running:];F=await D._check_auth(C,E)
		if F is _A:return web.Response(status=401)
		A={};A[_I]=datetime.datetime.utcnow();A[_J]=C.remote;A[_K]=C.method;A[_L]=C.path
		if E==_C or E=='':B=web.Response(status=400);B.text=_a
		else:B=web.Response(status=404);B.text=_b
		A[_N]=B.status;A[_M]=B.text;await D._insert_bootstrapping_log_entry(F,A);return B
	async def handle_action_request(D,request):
		C=request;E=C.path[D.len_prefix_operational:];F=await D._check_auth(C,E)
		if F is _A:return web.Response(status=401)
		A={};A[_I]=datetime.datetime.utcnow();A[_J]=C.remote;A[_K]=C.method;A[_L]=C.path
		if E==_C or E=='':B=web.Response(status=400);B.text="Resource doesn't support action."
		else:B=web.Response(status=404);B.text=_i
		A[_N]=B.status;A[_M]=B.text;await D._insert_bootstrapping_log_entry(F,A);return B
	async def handle_rpc_request(D,request):
		C=request;E=C.path[D.len_prefix_operations:];F=await D._check_auth(C,E)
		if F is _A:return web.Response(status=401)
		B={};B[_I]=datetime.datetime.utcnow();B[_J]=C.remote;B[_K]=C.method;B[_L]=C.path
		if E=='/ietf-sztp-bootstrap-server:get-bootstrapping-data':
			try:A=await D._handle_get_bootstrapping_data_rpc(F,C,B)
			except NotImplementedError as G:A=web.Response(status=501);A.text=str(G)
		elif E=='/ietf-sztp-bootstrap-server:report-progress':
			try:A=await D._handle_report_progress_rpc(F,C,B)
			except NotImplementedError as G:A=web.Response(status=501);A.text=str(G)
		elif E==_C or E=='':A=web.Response(status=400);A.text=_i
		else:A=web.Response(status=404);A.text='Unrecognized RPC.'
		B[_N]=A.status
		if not(A.status>=200 and A.status<=299):B[_M]=A.text
		await D._insert_bootstrapping_log_entry(F,B);return A
	async def _check_auth(B,request,data_path):
		o='local-truststore-reference';n=':device-type';m='identity-certificates';l='activation-code';k='" not found for any tenant.';j='Device "';X='verification';W='device-type';I='comment';H='failure';G='outcome';E=request;A={};A[_I]=datetime.datetime.utcnow();A[_J]=E.remote;A['source-proxies']=list(E.forwarded);A['host']=E.host;A[_K]=E.method;A[_L]=E.path;J=set();L=E.transport.get_extra_info('peercert')
		if L is not _A:P=L['subject'][-1][0][1];J.add(P)
		M=_A;Q=_A;N=E.headers.get('AUTHORIZATION')
		if N!=_A:M,Q=basicauth.decode(N);J.add(M)
		if len(J)==0:A[G]=H;A[I]='Device provided no identification credentials.';await B._insert_audit_log_entry(_A,A);return _A
		if len(J)!=1:A[G]=H;A[I]='Device provided mismatched authentication credentials ('+P+' != '+M+').';await B._insert_audit_log_entry(_A,A);return _A
		D=J.pop();C=_A
		if B.mode==_E:K=_C+B.dal.app_ns+_U
		elif B.mode==_T:K=_C+B.dal.app_ns+_e+D
		if B.mode!=_R:
			try:C=await B.dal.handle_get_config_request(K)
			except dal.NodeNotFound as R:A[G]=H;A[I]=j+D+k;await B._insert_audit_log_entry(_A,A);return _A
			F=_A
		else:
			try:F=await B.dal.get_tenant_name_for_global_key(_C+B.dal.app_ns+':tenants/tenant/devices/device',D)
			except dal.NodeNotFound as R:A[G]=H;A[I]=j+D+k;await B._insert_audit_log_entry(_A,A);return _A
			K=_C+B.dal.app_ns+_S+F+_f+D;C=await B.dal.handle_get_config_request(K)
		assert C!=_A;assert B.dal.app_ns+_U in C;C=C[B.dal.app_ns+_U]
		if B.mode!=_E:C=C[0]
		if l in C:
			if N==_A:A[G]=H;A[I]='Activation code required but none passed for serial number '+D;await B._insert_audit_log_entry(F,A);return _A
			S=C[l];assert S.startswith('$5$')
			if not sha256_crypt.verify(Q,S):A[G]=H;A[I]='Activation code mismatch for serial number '+D;await B._insert_audit_log_entry(F,A);return _A
		else:0
		assert W in C;Y=_C+B.dal.app_ns+':device-types/device-type='+C[W];T=await B.dal.handle_get_config_request(Y)
		if m in T[B.dal.app_ns+n][0]:
			if L is _A:A[G]=H;A[I]='Client cert required but none passed for serial number '+D;await B._insert_audit_log_entry(F,A);return _A
			U=E.transport.get_extra_info(_j);assert U is not _A;Z=U.getpeercert(_X);O=T[B.dal.app_ns+n][0][m];assert X in O;assert o in O[X];V=O[X][o];a=_C+B.dal.app_ns+':truststore/certificate-bags/certificate-bag='+V['certificate-bag']+'/certificate='+V['certificate'];b=await B.dal.handle_get_config_request(a);c=b[B.dal.app_ns+':certificate'][0]['cert'];d=base64.b64decode(c);e,f=der_decoder(d,asn1Spec=rfc5652.ContentInfo());assert not f;g=utils.degenerate_cms_obj_to_ders(e);h=ValidationContext(trust_roots=g);i=CertificateValidator(Z,validation_context=h)
			try:i._validate_path()
			except PathBuildingError as R:A[G]=H;A[I]="Client cert for serial number '"+D+"' doesn't validate using trust anchors specified by device-type '"+C[W]+"'";await B._insert_audit_log_entry(F,A);return _A
		A[G]='success';await B._insert_audit_log_entry(F,A);return[D,F]
	async def _handle_get_bootstrapping_data_rpc(A,device_id,request,bootstrapping_log_entry):
		Ae='ietf-sztp-bootstrap-server:output';Ad='ASCII';Ac='contentType';Ab=':configuration';Aa='configuration-handling';AZ='script';AY='hash-value';AX='hash-algorithm';AW='address';AV='referenced-definition';AU='serial-number';AT='rpc-supported';AS='not';AR='match-criteria';AQ='no-match-found';AP='response-manager';AO='input';A5='post-configuration-script';A4='configuration';A3='pre-configuration-script';A2='os-version';A1='os-name';A0='trust-anchor';z='port';y='bootstrap-server';x='ietf-sztp-conveyed-info:redirect-information';w='selected-response';p='image-verification';o='download-uri';n='boot-image';m='value';g=device_id;f='onboarding-information';b='key';Z='ietf-sztp-conveyed-info:onboarding-information';Y='redirect-information';Q='managed-response-supplied';P='response-details';H='response';G='get-bootstrapping-data-event';F=request;D=bootstrapping_log_entry;C='conveyed-information'
		if F.body_exists:
			if not _G in F.headers:B=web.Response(status=400);B.text='Content-Type must be specified when request bodies are passed (auto-sensing not supported).';return B
			if not any((F.headers[_G]==A for A in(_F,_H))):B=web.Response(status=415);B.text='Content-Type, when specified, must be either "application/yang-data+json" or "application/yang-data+xml".';return B
		if _O in F.headers:
			if not any((F.headers[_O]==A for A in(_k,_l,_F,_H))):B=web.Response(status=406);B.text='"Accept, when specified, must be "*/*", "application/*", "application/yang-data+json", or "application/yang-data+xml".';return B
		U=_A
		if F.body_exists:
			if F.headers[_G]==_F:
				try:U=await F.json()
				except json.decoder.JSONDecodeError as V:B=web.Response(status=400);B.text=_m+str(V);return B
			else:assert F.headers[_G]==_H;A6=await F.text();A7={_n:_o};U=xmltodict.parse(A6,process_namespaces=_X,namespaces=A7)
		J=_A
		if U:
			try:J=U[_c]
			except KeyError:B=web.Response(status=400);B.text=_Y+str(V);return B
			A8=A.dm.get_schema_node('/ietf-sztp-bootstrap-server:get-bootstrapping-data/input')
			try:A8.from_raw(J)
			except yangson.exceptions.RawMemberError as V:B=web.Response(status=400);B.text=_Y+str(V);return B
		if A.mode!=_R:K=_C+A.dal.app_ns+':'
		else:K=_C+A.dal.app_ns+_S+g[1]+_C
		if A.mode==_E:q=K+'device'
		else:q=K+'devices/device='+g[0]
		try:M=await A.dal.handle_get_config_request(q)
		except Exception as V:B=web.Response(status=501);B.text='Unhandled exception: '+str(V);return B
		assert M!=_A;assert A.dal.app_ns+_U in M;M=M[A.dal.app_ns+_U]
		if A.mode!=_E:M=M[0]
		D[_B]={};D[_B][G]={};D[_B][G][_V]={}
		if U is _A:D[_B][G][_V]['no-input-passed']=[_A]
		else:
			D[_B][G][_V][AO]=[]
			for r in J.keys():input={};input[b]=r;input[m]=J[r];D[_B][G][_V][AO].append(input)
		E=_A
		if AP not in M:D[_B][G][w]=AQ;B=web.Response(status=404);B.text='No responses configured.';return B
		for c in M[AP]['matched-response']:
			if not AR in c:E=c;break
			if U is _A:continue
			for L in c[AR]['match']:
				if L[b]not in J:break
				if'present'in L:
					if AS in L:
						if L[b]in J:break
					elif L[b]not in J:break
				elif m in L:
					if AS in L:
						if L[m]==J[L[b]]:break
					elif L[m]!=J[L[b]]:break
				else:raise NotImplementedError("Unrecognized 'match' expression.")
			else:E=c;break
		if E is _A or'none'in E[H]:D[_B][G][w]=AQ;B=web.Response(status=404);B.text='No matching responses configured.';return B
		D[_B][G][w]=E[_W];D[_B][G][P]={Q:{}}
		if C in E[H]:
			D[_B][G][P][Q]={C:{}};I={}
			if _P in E[H][C]:
				D[_B][G][P][Q][C]={_P:{}};assert _Q in E[H][C][_P];h=E[H][C][_P][_Q];D[_B][G][P][Q][C][_P]['referenced-callout']=h;R=await A.dal.handle_get_config_request(K+'dynamic-callouts/dynamic-callout='+h);assert h==R[A.dal.app_ns+_D][0][_W];D[_B][G][P][Q][C][_P][AT]=R[A.dal.app_ns+_D][0][AT];W={}
				if A.mode!=_E:W[AU]=g[0]
				else:W[AU]='mode-0 == no-sn'
				W['source-ip-address']=F.remote
				if J:W['from-device']=J
				s=F.transport.get_extra_info(_j)
				if s:
					t=s.getpeercert(_X)
					if t:W['identity-certificate']=t
				if _Z in R[A.dal.app_ns+_D][0]:A9=R[A.dal.app_ns+_D][0][_Z]['plugin'];AA=R[A.dal.app_ns+_D][0][_Z]['function'];AB=A.nvh.plugins[A9]['functions'][AA](W)
				elif _d in R[A.dal.app_ns+_D][0]:raise NotImplementedError('webhooks callout support pending!')
				else:raise NotImplementedError('unhandled dynamic callout type: '+str(R[A.dal.app_ns+_D][0]))
				I=AB
			elif Y in E[H][C]:
				D[_B][G][P][Q][C]={Y:{}};I[x]={};I[x][y]=[]
				if _Q in E[H][C][Y]:
					a=E[H][C][Y][_Q];D[_B][G][P][Q][C][Y]={AV:a};i=await A.dal.handle_get_config_request(K+'conveyed-information-responses/redirect-information-response='+a)
					for AC in i[A.dal.app_ns+':redirect-information-response'][0][Y][y]:
						S=await A.dal.handle_get_config_request(K+'bootstrap-servers/bootstrap-server='+AC);S=S[A.dal.app_ns+':bootstrap-server'][0];d={};d[AW]=S[AW]
						if z in S:d[z]=S[z]
						if A0 in S:d[A0]=S[A0]
						I[x][y].append(d)
				else:raise NotImplementedError('unhandled redirect-information config type: '+str(E[H][C][Y]))
			elif f in E[H][C]:
				D[_B][G][P][Q][C]={};I[Z]={}
				if _Q in E[H][C][f]:
					a=E[H][C][f][_Q];D[_B][G][P][Q][C][f]={AV:a};i=await A.dal.handle_get_config_request(K+'conveyed-information-responses/onboarding-information-response='+a);N=i[A.dal.app_ns+':onboarding-information-response'][0][f]
					if n in N:
						AD=N[n];AE=await A.dal.handle_get_config_request(K+'boot-images/boot-image='+AD);O=AE[A.dal.app_ns+':boot-image'][0];I[Z][n]={};X=I[Z][n]
						if A1 in O:X[A1]=O[A1]
						if A2 in O:X[A2]=O[A2]
						if o in O:
							X[o]=list()
							for AF in O[o]:X[o].append(AF)
						if p in O:
							X[p]=list()
							for u in O[p]:j={};j[AX]=u[AX];j[AY]=u[AY];X[p].append(j)
					if A3 in N:AG=N[A3];AH=await A.dal.handle_get_config_request(K+'scripts/pre-configuration-script='+AG);I[Z][A3]=AH[A.dal.app_ns+':pre-configuration-script'][0][AZ]
					if A4 in N:AI=N[A4];v=await A.dal.handle_get_config_request(K+'configurations/configuration='+AI);I[Z][Aa]=v[A.dal.app_ns+Ab][0][Aa];I[Z][A4]=v[A.dal.app_ns+Ab][0]['config']
					if A5 in N:AJ=N[A5];AK=await A.dal.handle_get_config_request(K+'scripts/post-configuration-script='+AJ);I[Z][A5]=AK[A.dal.app_ns+':post-configuration-script'][0][AZ]
			else:raise NotImplementedError('unhandled conveyed-information type: '+str(E[H][C]))
		else:raise NotImplementedError('unhandled response type: '+str(E[H]))
		T=_A
		if _O in F.headers:
			if any((F.headers[_O]==A for A in(_F,_H))):T=F.headers[_O]
		if T is _A:T=F.headers[_G]
		if T==_H:raise NotImplementedError('XML-based response not implemented yet...')
		e=rfc5652.ContentInfo()
		if T==_F:e[Ac]=A.id_ct_sztpConveyedInfoJSON;e['content']=encode_der(json.dumps(I,indent=4),asn1Spec=univ.OctetString())
		else:assert T==_H;e[Ac]=A.id_ct_sztpConveyedInfoXML;raise NotImplementedError('XML based responses not supported.')
		AL=encode_der(e,rfc5652.ContentInfo());k=base64.b64encode(AL).decode(Ad);AM=base64.b64decode(k);AN=base64.b64encode(AM).decode(Ad);assert k==AN;l={};l[Ae]={};l[Ae][C]=k;B=web.Response(status=200);B.content_type=T;B.text=json.dumps(l,indent=4);return B
	async def _handle_report_progress_rpc(B,device_id,request,bootstrapping_log_entry):
		f='remote-port';e='wn-sztpd-rpcs:input';d='webhook-results';U='tcp-client-parameters';T='encoding';S='webhook';Q=device_id;P='http';M='dynamic-callout-result';H='report-progress-event';E=bootstrapping_log_entry;C=request
		if _G not in C.headers:A=web.Response(status=400);A.text='Request missing the "Content-Type" header (RFC 8040, 5.2).';return A
		if not any((C.headers[_G]==A for A in(_F,_H))):A=web.Response(status=415);A.text='Content-Type must be "application/yang-data+json" or "application/yang-data+xml".';return A
		if _O in C.headers:
			if not any((C.headers[_O]==A for A in(_k,_l,_F,_H))):A=web.Response(status=406);A.text='The "Accept" type, when set, must be "*/*", "application/*", "application/yang-data+json", or "application/yang-data+xml".';return A
		G=_A
		if not C.body_exists:A=web.Response(status=400);A.text='Missing "input" document';return A
		if C.headers[_G]==_F:
			try:G=await C.json()
			except json.decoder.JSONDecodeError as F:A=web.Response(status=400);A.text=_m+str(F);return A
		else:assert C.headers[_G]==_H;V=await C.text();W={_n:_o};G=xmltodict.parse(V,process_namespaces=_X,namespaces=W)
		assert not G is _A
		try:X=G[_c]
		except KeyError:A=web.Response(status=400);A.text=_Y+str(F);return A
		Y=B.dm.get_schema_node('/ietf-sztp-bootstrap-server:report-progress/input')
		try:Y.from_raw(X)
		except (yangson.exceptions.RawMemberError,yangson.exceptions.RawTypeError)as F:A=web.Response(status=400);A.text=_Y+str(F);return A
		E[_B]={};E[_B][H]={};E[_B][H][_V]=G[_c];E[_B][H][M]={}
		if B.mode==_E or B.mode==_T:I=_C+B.dal.app_ns+':preferences/notification-delivery'
		elif B.mode==_R:I=_C+B.dal.app_ns+_S+Q[1]+'/preferences/notification-delivery'
		try:Z=await B.dal.handle_get_config_request(I)
		except Exception as F:E[_B][H][M]['no-webhooks-configured']=[_A]
		else:
			N=Z[B.dal.app_ns+':notification-delivery'][_P][_Q];E[_B][H][M][_W]=N
			if B.mode==_E or B.mode==_T:I=_C+B.dal.app_ns+':dynamic-callouts/dynamic-callout='+N
			elif B.mode==_R:I=_C+B.dal.app_ns+_S+Q[1]+'/dynamic-callouts/dynamic-callout='+N
			K=await B.dal.handle_get_config_request(I);E[_B][H][M][d]={S:[]};O={};O[e]={};O[e]['notification']=G;a=json.dumps(O);b='FIXME: xml output'
			if _Z in K[B.dal.app_ns+_D][0]:raise NotImplementedError('callback support not implemented yet')
			elif _d in K[B.dal.app_ns+_D][0]:
				for D in K[B.dal.app_ns+_D][0][_d][S]:
					J={};J[_W]=D[_W]
					if T not in D or D[T]=='json':R=a
					elif D[T]=='xml':R=b
					if P in D:
						L='http://'+D[P][U]['remote-address']
						if f in D[P][U]:L+=':'+str(D[P][U][f])
						L+='/send-notification';J['uri']=L
						try:
							async with aiohttp.ClientSession()as c:A=await c.post(L,data=R)
						except aiohttp.client_exceptions.ClientConnectorError as F:J['connection-error']=str(F)
						else:
							J['http-status-code']=A.status
							if A.status==200:break
					else:assert'https'in D;raise NotImplementedError("https-based webhook isn't supported yet.")
					E[_B][H][M][d][S].append(J)
			else:raise NotImplementedError('unrecognized callout type '+str(K[B.dal.app_ns+_D][0]))
		A=web.Response(status=204);return A