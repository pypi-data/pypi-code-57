# Copyright (c) 2020 Watsen Networks.  All Rights Reserved.

_E='application/yang-data+json'
_D='/ds/ietf-datastores:operational'
_C='/ds/ietf-datastores:running'
_B=None
_A='/'
import os,ssl,json,base64,pyasn1,asyncio,yangson,datetime,tempfile,basicauth
from .  import utils
from aiohttp import web
from .handler import RouteHandler
from pyasn1_modules import rfc5652
from pyasn1_modules import rfc5915
from pyasn1.codec.der.decoder import decode as der_decoder
from pyasn1.codec.der.encoder import encode as der_encoder
async def set_server_header(request,response):response.headers['Server']='<redacted>'
class RestconfServer:
	root='/restconf';prefix_running=root+_C;prefix_operational=root+_D;prefix_operations=root+'/operations';len_prefix_running=len(prefix_running);len_prefix_operational=len(prefix_operational);len_prefix_operations=len(prefix_operations)
	def __init__(A,loop,dal,endpoint_config,view_handler,facade_yl=_B):
		A3='client-certs';A2='local-truststore-reference';A1='ca-certs';A0='client-authentication';z='w';y='cert';x='ASCII';w=':keystore/asymmetric-keys/asymmetric-key=';v='reference';u='server-identity';t='local-port';s='http';X='tcp-server-parameters';N='certificate';M='tls-server-parameters';L='/ds/ietf-datastores:running{tail:.*}';G=dal;E='https';C=view_handler;B=endpoint_config;A.len_prefix_running=len(A.root+_C);A.len_prefix_operational=len(A.root+_D);A.loop=loop;A.dal=G;A.name=B['name'];A.view_handler=C;A.app=web.Application();A.app.on_response_prepare.append(set_server_header);A.app.router.add_get('/.well-known/host-meta',A.handle_get_host_meta);A.app.router.add_get(A.root,A.handle_get_tippy_top);A.app.router.add_get(A.root+_A,A.handle_get_tippy_top);A.app.router.add_get(A.root+'/yang-library-version',A.handle_get_yang_library_version);A.app.router.add_get(A.root+'/ds/ietf-datastores:operational{tail:.*}',C.handle_get_opstate_request);A.app.router.add_get(A.root+L,C.handle_get_config_request);A.app.router.add_put(A.root+L,C.handle_put_config_request);A.app.router.add_post(A.root+L,C.handle_post_config_request);A.app.router.add_delete(A.root+L,C.handle_delete_config_request);A.app.router.add_post(A.root+'/ds/ietf-datastores:operational/{tail:.*}',C.handle_action_request);A.app.router.add_post(A.root+'/operations/{tail:.*}',C.handle_rpc_request)
		if s in B:F=s
		else:assert E in B;F=E
		A.local_address=B[F][X]['local-address'];A.local_port=os.environ.get('SZTPD_DEFAULT_PORT',8080)
		if t in B[F][X]:A.local_port=B[F][X][t]
		D=_B
		if F==E:
			O=B[E][M][u][N][v]['asymmetric-key'];I=A.dal.handle_get_config_request(_A+A.dal.app_ns+w+O);Y=A.loop.run_until_complete(I);P=Y[A.dal.app_ns+':asymmetric-key'][0]['private-key'];Z=base64.b64decode(P);a,A4=der_decoder(Z,asn1Spec=rfc5915.ECPrivateKey());b=der_encoder(a);Q=base64.b64encode(b).decode(x);assert P==Q;c='-----BEGIN EC PRIVATE KEY-----\n'+Q+'\n-----END EC PRIVATE KEY-----\n';d=B[E][M][u][N][v][N];I=A.dal.handle_get_config_request(_A+A.dal.app_ns+w+O+'/certificates/certificate='+d);e=A.loop.run_until_complete(I);f=e[A.dal.app_ns+':certificate'][0][y];g=base64.b64decode(f);h,i=der_decoder(g,asn1Spec=rfc5652.ContentInfo());j=h.getComponentByName('content');k,i=der_decoder(j,asn1Spec=rfc5652.SignedData());R=k.getComponentByName('certificates');S=''
			for l in range(len(R)):m=R[l][0];n=der_encoder(m);o=base64.b64encode(n).decode(x);S+='-----BEGIN CERTIFICATE-----\n'+o+'\n-----END CERTIFICATE-----\n'
			D=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH);D.verify_mode=ssl.CERT_OPTIONAL
			with tempfile.TemporaryDirectory()as T:
				U=T+'key.pem';V=T+'certs.pem'
				with open(U,z)as p:p.write(c)
				with open(V,z)as q:q.write(S)
				D.load_cert_chain(V,U)
			if A0 in B[E][M]:
				H=B[E][M][A0]
				def W(truststore_ref):
					C=G.handle_get_config_request(_A+G.app_ns+':truststore/certificate-bags/certificate-bag='+truststore_ref);D=A.loop.run_until_complete(C);B=[]
					for E in D[G.app_ns+':certificate-bag'][0][N]:F=base64.b64decode(E[y]);H,I=der_decoder(F,asn1Spec=rfc5652.ContentInfo());assert not I;B+=utils.degenerate_cms_obj_to_ders(H)
					return B
				J=[]
				if A1 in H:K=H[A1][A2];J+=W(K)
				if A3 in H:K=H[A3][A2];J+=W(K)
				r=utils.der_dict_to_multipart_pem({'CERTIFICATE':J});D.load_verify_locations(cadata=r)
		if F==E:assert not D is _B
		else:assert D is _B
		A.runner=web.AppRunner(A.app);A.loop.run_until_complete(A.runner.setup());A.site=web.TCPSite(A.runner,host=A.local_address,port=A.local_port,ssl_context=D,reuse_port=True);A.loop.run_until_complete(A.site.start())
	async def handle_get_host_meta(B,request):A=web.Response();A.content_type='application/xrd+xml';A.text='<XRD xmlns="http://docs.oasis-open.org/ns/xri/xrd-1.0">\n  <Link rel="restconf" href="/restconf"/>\n</XRD>';return A
	async def handle_get_tippy_top(C,request):
		A=request.path[C.len_prefix_running:]
		if A=='':A=_A
		elif A!=_A and A[-1]==_A:A=A[:-1]
		B=web.Response();B.content_type=_E;B.text='{\n  "ietf-restconf:restconf" : {\n    "data" : {},\n    "operations" : {},\n    "yang-library-version" : "2019-01-04"\n  }\n}';return B
	async def handle_get_yang_library_version(C,request):
		D=request;A=D.path[C.len_prefix_running:]
		if A=='':A=_A
		elif A!=_A and A[-1]==_A:A=A[:-1]
		B=await C._check_auth(D,A)
		if B.status==401:return B
		B=await C.check_headers(D)
		if B!=_B:return B
		E=web.Response();E.content_type=_E;E.text='{\n  "ietf-restconf:yang-library-version" : "2019-01-04"\n}';return E