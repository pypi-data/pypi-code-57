# Copyright (c) 2020 Watsen Networks.  All Rights Reserved.

_k='config-false-prefixes'
_j='table-name-map'
_i='table-keys'
_h='app_ns'
_g='sztpd_meta'
_f='SELECT schema_name FROM information_schema.schemata;'
_e='postgresql'
_d='Cannot delete: '
_c='[^/]*=[^/]*'
_b='[^:]*:'
_a='yang-library'
_Z='" does not exist.'
_Y=':tenants/tenant'
_X='opaque'
_W='global-root'
_V='db_ver'
_U='sqlite'
_T=':memory:'
_S='mysql'
_R='" already exists.'
_Q='Node "'
_P='Parent node ('
_O='.singletons'
_N='name'
_M='row_id'
_L='.*/'
_K=') does not exist.'
_J=':'
_I='jsob'
_H='pid'
_G='='
_F='=[^/]*'
_E='singletons'
_D=True
_C=False
_B=None
_A='/'
import os,re,sys,json,base64,pickle,yangson,binascii,pkg_resources,sqlalchemy_utils,sqlalchemy as sa
from sqlalchemy.schema import CreateTable
from sqlalchemy.sql import and_
from dataclasses import dataclass
from enum import IntFlag
known_text=b'a secret message'
jsob_type=sa.JSON
class ContentType(IntFlag):CONFIG_TRUE=1;CONFIG_FALSE=2;CONFIG_ANY=3
@dataclass
class DatabasePath:data_path:str=_B;schema_path:str=_B;jsob_data_path:str=_B;table_name:str=_B;row_id:int=_B;inside_path:str=_B;path_segments:list=_B;jsob:dict=_B;node_ptr:dict=_B;prev_ptr:dict=_B
class NodeAlreadyExists(Exception):0
class NodeNotFound(Exception):0
class ParentNodeNotFound(Exception):0
class DataAccessLayer:
	def __init__(A,db_url,cert_path,yl_obj=_B,app_ns=_B,opaque=_B):
		D=yl_obj;C=cert_path;B=db_url;A.app_ns=_B;A.engine=_B;A.metadata=_B;A.leafrefs=_B;A.referers=_B;A.ref_stat_collectors=_B;A.global_root_id=_B;A.table_keys=_B;A.schema_path_to_real_table_name=_B;A.config_false_prefixes=_B
		if D is _B:A._init(B,C)
		else:A.app_ns=app_ns;A._create(B,C,D,opaque)
		assert A.app_ns!=_B;assert A.engine!=_B;assert A.metadata!=_B;assert A.leafrefs!=_B;assert A.referers!=_B;assert A.ref_stat_collectors!=_B;assert A.global_root_id!=_B;assert A.table_keys!=_B;assert A.schema_path_to_real_table_name!=_B;assert A.config_false_prefixes!=_B
	def opaque(A):
		B=A.metadata.tables[A.schema_path_to_real_table_name[_E]]
		with A.engine.connect()as C:D=C.execute(sa.select([B.c.jsob]).where(B.c.name==_X));return D.first()[0]
	async def num_elements_in_list(A,data_path):
		B=data_path;C=re.sub(_F,'',B)
		if C!=B:assert NotImplementedError("Nested listed arren't supported yet.")
		D=A.schema_path_to_real_table_name[C];E=A.metadata.tables[D]
		with A.engine.connect()as F:G=F.execute(sa.select([sa.func.count()]).select_from(E));H=G.first()[0];return H
	async def get_tenant_name_for_admin(A,email_address):
		K='email-address';G=email_address
		if A.app_ns.endswith('x'):
			B=A.schema_path_to_real_table_name[_A+A.app_ns+':tenants/tenant/admin-accounts/admin-account'];C=A.metadata.tables[B]
			with A.engine.connect()as E:
				D=E.execute(sa.select([C.c.pid]).where(C.c[K]==G));F=D.first()
				if F!=_B:I=F[0];B=A.schema_path_to_real_table_name[_A+A.app_ns+_Y];H=A.metadata.tables[B];D=E.execute(sa.select([H.c.name]).where(H.c.row_id==I));J=D.first()[0];return J
		B=A.schema_path_to_real_table_name[_A+A.app_ns+':admin-accounts/admin-account'];C=A.metadata.tables[B]
		with A.engine.connect()as E:
			D=E.execute(sa.select([C.c.pid]).where(C.c[K]==G));F=D.first()
			if F!=_B:return _B
		raise NodeNotFound('Admin "'+G+_Z)
	async def get_tenant_name_for_global_key(A,table_name,k):
		B=table_name;C=A.schema_path_to_real_table_name[B];E=A.metadata.tables[C]
		with A.engine.connect()as F:
			D=F.execute(sa.select([E.c.pid]).where(getattr(E.c,A.table_keys[B])==k));G=D.first()
			if G==_B:raise NodeNotFound('key "'+k+'" in table "'+B+_Z)
			I=G[0];C=A.schema_path_to_real_table_name[_A+A.app_ns+_Y];H=A.metadata.tables[C];D=F.execute(sa.select([H.c.name]).where(H.c.row_id==I));J=D.first()[0];return J
	async def handle_get_opstate_request(B,data_path):
		A=data_path;assert A!='';assert not(A!=_A and A[-1]==_A)
		if A=='/ietf-yang-library:yang-library':
			E=B.schema_path_to_real_table_name[_E];C=B.metadata.tables[E]
			with B.engine.connect()as F:G=F.execute(sa.select([C.c.jsob]).where(C.c.name==_a));return G.first()[0]
		D=re.sub(_F,'',A)
		if 0:return await B.handle_get_data_request(A,D,ContentType.CONFIG_FALSE)
		else:return await B.handle_get_data_request(A,D,ContentType.CONFIG_ANY)
	async def handle_get_config_request(C,data_path):
		A=data_path;assert A!='';assert not(A!=_A and A[-1]==_A);B=re.sub(_F,'',A);F=await C.handle_get_data_request(A,B,ContentType.CONFIG_TRUE);D=re.sub(_L,'',B)
		if not D.startswith(C.app_ns+_J):D=C.app_ns+_J+D
		for E in C.config_false_prefixes:
			if E.startswith(B):
				if B==_A:G=E[1:]
				else:G=E.replace(B,D,1)
				I=_B;J=F
				def H(prev_ptr,curr_ptr,remainder_path):
					D=prev_ptr;B=remainder_path;A=curr_ptr;E=B.split(_A)
					for C in E:
						if type(A)==list:
							for F in A:H(A,F,B)
							return
						elif C in A:D=A;A=A[C];B=B.replace(C+_A,'',1)
						else:return
					D.pop(C)
				H(I,J,G)
			else:0
		return F
	async def handle_get_data_request(C,data_path,schema_path,content_type):
		L='Node (';G=content_type;F=data_path;E=schema_path
		if G is ContentType.CONFIG_TRUE and any((E.startswith(A)for A in C.config_false_prefixes)):raise NodeNotFound(L+F+_K)
		with C.engine.connect()as H:
			A=C._get_dbpath_for_data_path(F,G,H)
			if A==_B:raise NodeNotFound(L+F+_K)
			B=re.sub(_L,'',E);I=B
			if B=='':D=A.node_ptr
			else:
				if not B.startswith(C.app_ns+_J):B=C.app_ns+_J+B
				D={}
				if A.table_name!=_E and I==A.inside_path:D[B]=[];D[B].append(A.node_ptr);A.node_ptr=D[B][0]
				else:D[B]=A.node_ptr
			J=C._get_list_of_direct_subtables_for_schema_path(E)
			for K in J:await C._recursively_attempt_to_get_data_from_subtable(K,A.row_id,E,A.node_ptr,G,H)
		return D
	async def _recursively_attempt_to_get_data_from_subtable(E,subtable_name,pid,jsob_schema_path,jsob_iter,content_type,conn):
		J=content_type;I=jsob_schema_path;C=subtable_name
		if not ContentType.CONFIG_FALSE in J:
			if any((C.startswith(A)for A in E.config_false_prefixes)):return
			else:0
		else:0
		Q=E._find_rows_in_table_having_pid(C,pid,conn);K=Q.fetchall()
		if len(K)==0:return
		B=jsob_iter
		if I==_A:M=C[1:]
		else:assert I.startswith(_A+E.app_ns);M=C.replace(I+_A,'')
		D=re.sub(_L,'',C);G=re.sub(D+'$','',M)
		if G!='':
			G=G[:-1];R=G.split(_A)
			for L in R:
				try:B=B[L]
				except KeyError as W:assert ContentType.CONFIG_FALSE in J;B[L]={};B=B[L]
		if any((C.startswith(A)for A in E.config_false_prefixes)):
			B[D]=[];S=E.schema_path_to_real_table_name[C];T=E.metadata.tables[S]
			for F in K:
				H={}
				for A in T.c:
					if A.name!=_M and A.name!=_H:
						if type(A.type)is sa.sql.sqltypes.DateTime:H[A.name]=F[A.name].strftime('%Y-%m-%dT%H:%M:%SZ')
						elif type(A.type)is sa.sql.sqltypes.JSON or type(A.type)is sa.sql.sqltypes.PickleType:
							if F[A.name]is not _B and not(type(F[A.name])is list and len(F[A.name])==0):H[A.name]=F[A.name]
						elif F[A.name]is not _B:H[A.name]=F[A.name]
				B[D].append(H)
		else:
			N=0
			for O in K:
				P=O[_I];D=next(iter(P))
				if D not in B:B[D]=[]
				B[D].append(P.pop(D));U=E._get_list_of_direct_subtables_for_schema_path(C)
				for V in U:await E._recursively_attempt_to_get_data_from_subtable(V,O[0],C,B[D][N],J,conn)
				N+=1
	async def handle_post_config_request(B,data_path,request_body,create_callbacks,change_callbacks,opaque):
		C=request_body;A=data_path;assert A!='';assert not(A!=_A and A[-1]==_A);assert type(C)==dict
		with B.engine.begin()as D:
			E=B._get_dbpath_for_data_path(A,ContentType.CONFIG_TRUE,D)
			if E==_B:raise ParentNodeNotFound(_P+A+_K)
			await B._handle_post_config_request(E,C,create_callbacks,change_callbacks,opaque,D)
	async def _handle_post_config_request(C,parent_dbpath,request_body,create_callbacks,change_callbacks,opaque,conn):
		P=change_callbacks;O=create_callbacks;M=opaque;H=request_body;D=conn;A=parent_dbpath;I=A.data_path;S=re.sub(_F,'',I);E=next(iter(H))
		if I==_A:B=E;F=_A+B
		else:B=re.sub(_b,'',E);F=I+_A+B
		T=re.sub(_F,'',F);G=C._get_table_name_for_schema_path(T);assert G!=_B
		if G==A.table_name:
			if B in A.node_ptr:raise NodeAlreadyExists(_Q+B+_R)
			A.node_ptr[B]=H.pop(E);U=await C._recursively_post_subtable_data(A.row_id,F,A.node_ptr[B],A.jsob,A.jsob_data_path,O,M,D);C._update_jsob_for_row_id_in_table(A.table_name,A.row_id,A.jsob,D)
		else:
			if B not in A.node_ptr:A.node_ptr[B]=[];C._update_jsob_for_row_id_in_table(A.table_name,A.row_id,A.jsob,D)
			J={};assert len(H[E])==1;J[B]=H[E][0];Q=H[E][0][C.table_keys[G]];K={};K[_H]=A.row_id;K[C.table_keys[G]]=Q;K[_I]={};N=C.schema_path_to_real_table_name[G];L=C.metadata.tables[N]
			try:R=D.execute(L.insert().values(**K))
			except sa.exc.IntegrityError:raise NodeAlreadyExists(_Q+B+_R)
			F+=_G+str(Q);U=await C._recursively_post_subtable_data(R.inserted_primary_key[0],F,J[B],J,F,O,M,D);N=C.schema_path_to_real_table_name[G];L=C.metadata.tables[N];D.execute(L.update().where(L.c.row_id==R.inserted_primary_key[0]).values(jsob=J))
		V=re.sub(_F,'',I)
		if V in P:
			for W in P[S]:await W(I,A.jsob,A.jsob_data_path,M)
	async def _recursively_post_subtable_data(B,pid,data_path,req_body_iter,jsob,jsob_data_path,create_callbacks,opaque,conn):
		N=jsob_data_path;M=jsob;J=conn;I=opaque;E=data_path;D=create_callbacks;C=req_body_iter;A=re.sub(_F,'',E)
		if type(C)==dict:
			if A in D:
				for O in D[A]:await O(E,M,N,I)
			for P in C.copy():K=E+_A+P;R=await B._recursively_post_subtable_data(pid,K,C[P],M,N,D,I,J)
		elif type(C)==list and A in B.table_keys:
			if A in B.table_keys:
				while C:
					F=C.pop(0);assert type(F)==dict;S=re.sub(_L,'',A);L={};L[S]=F;G=B.table_keys[A];H={};H[_H]=pid;H[G]=F[G];H[_I]=L;T=B.schema_path_to_real_table_name[A];U=B.metadata.tables[T]
					try:Q=J.execute(U.insert().values(**H))
					except sa.exc.IntegrityError as V:raise NodeAlreadyExists(_Q+G+'" with value "'+H[G]+_R)
					K=E+_G+str(F[G]);R=await B._recursively_post_subtable_data(Q.inserted_primary_key[0],K,F,L,K,D,I,J);B._update_jsob_for_row_id_in_table(A,Q.inserted_primary_key[0],L,J)
				assert type(C)==list;assert len(C)==0
		elif A in D:
			for O in D[A]:await O(E,M,N,I)
		if A in B.table_keys:return _D
		return _C
	async def handle_post_opstate_request(A,data_path,request_body):
		P='Unrecognized resource schema path: ';I=request_body;B=data_path;assert B!='';assert not(B!=_A and B[-1]==_A);C=re.sub(_F,'',B);F=next(iter(I))
		if C==_A:G=F;D=_A+G
		else:G=re.sub(_b,'',F);D=C+_A+G
		J=A._get_table_name_for_schema_path(D)
		if J!=D:raise NodeNotFound(P+D)
		E=I[F];K=re.findall(_c,B)
		if len(K)==0:E[_H]=A.global_root_id
		else:
			L=A._get_table_name_for_schema_path(C)
			if L==_B:raise ParentNodeNotFound(P+C)
			M=K[-1].split(_G)
			with A.engine.connect()as H:E[_H]=A._get_row_id_for_key_in_table(L,M[1],H)
			if E[_H]==_B:raise ParentNodeNotFound('Nonexistent parent resource: '+B)
		N=A.schema_path_to_real_table_name[J];O=A.metadata.tables[N]
		with A.engine.connect()as H:Q=H.execute(O.insert().values(**E))
	async def handle_put_config_request(B,data_path,request_body,create_callbacks,change_callbacks,delete_callbacks,opaque):
		A=data_path;assert A!='';assert not(A!=_A and A[-1]==_A)
		with B.engine.begin()as C:await B._handle_put_config_request(A,request_body,create_callbacks,change_callbacks,delete_callbacks,opaque,C)
	async def _handle_put_config_request(C,data_path,request_body,create_callbacks,change_callbacks,delete_callbacks,opaque,conn):
		L=delete_callbacks;I=opaque;H=change_callbacks;G=create_callbacks;E=data_path;D=conn;B=request_body;J=re.sub(_F,'',E)
		if E==_A:A=C._get_dbpath_for_data_path(_A,ContentType.CONFIG_ANY,D);assert A!=_B;await C.recursive_compare_and_put(A.row_id,_A,B,A.node_ptr,_B,A,G,H,L,I,D);N=C.schema_path_to_real_table_name[A.table_name];K=C.metadata.tables[N];D.execute(K.update().where(K.c.row_id==A.row_id).values(jsob=A.jsob));return
		if J.count(_A)>1:assert type(B)==dict;assert len(B)==1;F=next(iter(B));assert J.endswith(F.replace(C.app_ns+_J,'',1));O=B;B=B[F]
		if type(B)==list:assert len(B)==1;B=B[0]
		A=C._get_dbpath_for_data_path(E,ContentType.CONFIG_ANY,D)
		if A==_B:
			assert E!=_A;M,P=E.rsplit(_A,1)
			if M=='':M=_A
			A=C._get_dbpath_for_data_path(M,ContentType.CONFIG_ANY,D)
			if A==_B:raise ParentNodeNotFound(_P+M+_K)
			if J.count(_A)>1:await C._handle_post_config_request(A,O,G,H,I,D)
			else:await C._handle_post_config_request(A,B,G,H,I,D)
			C._update_jsob_for_row_id_in_table(A.table_name,A.row_id,A.jsob,D);return
		if J.count(_A)==1 and J!=_A:
			if J in C.table_keys:F=next(iter(B));assert type(B[F])==list;assert len(B[F])==1;B=B[F][0];await C.recursive_compare_and_put(A.row_id,E,B,A.node_ptr,A.prev_ptr,A,G,H,L,I,D)
			else:F=next(iter(B));B=B[F];await C.recursive_compare_and_put(A.row_id,E,B,A.node_ptr,A.prev_ptr,A,G,H,L,I,D)
		else:await C.recursive_compare_and_put(A.row_id,E,B,A.node_ptr,A.prev_ptr,A,G,H,L,I,D)
		N=C.schema_path_to_real_table_name[A.table_name];K=C.metadata.tables[N];D.execute(K.update().where(K.c.row_id==A.row_id).values(jsob=A.jsob))
	async def recursive_compare_and_put(D,pid,data_path,req_body_iter,dbpath_curr_ptr,dbpath_prev_ptr,dbpath,create_callbacks,change_callbacks,delete_callbacks,opaque,conn):
		W=dbpath_prev_ptr;O=delete_callbacks;N=create_callbacks;M=pid;K=change_callbacks;J=opaque;I=conn;H=dbpath;F=dbpath_curr_ptr;C=req_body_iter;B=data_path;assert type(C)==type(F);E=re.sub(_F,'',B)
		if B==_A:0
		if type(C)==dict:
			P=set(list(C.keys()));Q=set(list(F.keys()))
			for A in [A for A in P if A not in Q]:
				if type(C[A])==list:U=_A+A if B==_A else B+_A+A;await D.recursive_compare_and_put(M,U,C[A],[],_B,H,N,K,O,J,I);F[A]=[]
				else:
					E=re.sub(_F,'',B);R=_A+A if E==_A else E+_A+A;assert type(C)!=list;G=_A+A if B==_A else B+_A+A;F[A]=C[A];a=await D._recursively_post_subtable_data(M,G,C[A],H.jsob,H.jsob_data_path,N,J,I)
					if a==1:assert type(C)==dict;assert type(C[A])==list;assert len(C[A])==0;C.pop(A);F.pop(A)
			for A in Q-P:
				if _C:U=_A+A if B==_A else B+_A+A;await D.recursive_compare_and_put(M,U,[],F[A],F,H,N,K,O,J,I);del F[A]
				else:
					R=_A+A if E==_A else E+_A+A
					if R in D.config_false_prefixes:0
					else:G=_A+A if B==_A else B+_A+A;await D._recursively_delete_subtable_data(H.row_id,G,F[A],O,J,I);del F[A]
			X=_C
			for A in Q&P:
				G=_A+A if B==_A else B+_A+A;R=re.sub(_F,'',G)
				if R in D.schema_path_to_real_table_name:0
				b=await D.recursive_compare_and_put(M,G,C[A],F[A],F,H,N,K,O,J,I)
				if b==_D:X=_D
				if R in D.schema_path_to_real_table_name:0
			if Q-P or(P-Q or X==_D):
				if E in K:
					for V in K[E]:await V(B,H.jsob,H.jsob_data_path,J)
			return _C
		elif type(C)==list and E in D.table_keys:
			Y=[A[D.table_keys[E]]for A in C];T=set(Y);S=set([A[0]for A in D._get_keys_in_table_having_pid(E,M,I)])
			for A in [A for A in Y if A not in S]:assert B!=_A;G=B+_G+A;c=[B for B in C if B[D.table_keys[E]]==A][0];d=[c];g=await D._recursively_post_subtable_data(M,B,d,_B,_B,N,J,I)
			for A in S-T:G=B+_G+A;h,Z=B.rsplit(_A,1);assert Z!='';await D._recursively_delete_subtable_data(H.row_id,G,W[Z],O,J,I)
			for A in S&T:G=B+_G+A;L=D._get_dbpath_for_data_path(G,ContentType.CONFIG_TRUE,I);assert L!=_B;e=[B for B in C if B[D.table_keys[E]]==A][0];await D.recursive_compare_and_put(L.row_id,G,e,L.node_ptr,L.prev_ptr,L,N,K,O,J,I);D._update_jsob_for_row_id_in_table(L.table_name,L.row_id,L.jsob,I)
			if T-S or S-T:return _D
			return _C
		else:
			if F!=C:
				f=re.sub('^.*/','',B);W[f]=C
				if E in K:
					for V in K[E]:await V(B,H.jsob,H.jsob_data_path,J)
			else:0
			return _C
		raise NotImplementedError('logic never reaches this point')
	async def handle_put_opstate_request(E,data_path,request_body):
		C=data_path;B=request_body;assert C!='';assert not(C!=_A and C[-1]==_A)
		with E.engine.begin()as G:
			D,F=C.rsplit(_A,1);assert F!=''
			if D=='':D=_A
			A=E._get_dbpath_for_data_path(D,ContentType.CONFIG_ANY,G)
			if A==_B:raise ParentNodeNotFound(_P+D+_K)
			if type(B)==str:assert type(A.node_ptr)==dict;A.node_ptr[F]=B
			else:assert type(A.node_ptr)==dict and type(B)==dict;A.node_ptr[F]=B[next(iter(B))]
			E._update_jsob_for_row_id_in_table(A.table_name,A.row_id,A.jsob,G)
	async def handle_delete_config_request(B,data_path,delete_callbacks,change_callbacks,opaque):
		A=data_path;assert A!='';assert A!=_A;assert A[-1]!=_A
		with B.engine.begin()as C:await B._handle_delete_config_request(A,delete_callbacks,change_callbacks,opaque,C)
	async def _handle_delete_config_request(E,data_path,delete_callbacks,change_callbacks,opaque,conn):
		I=opaque;H=change_callbacks;F=conn;C=data_path;D,G=C.rsplit(_A,1)
		if D=='':D=_A
		A=E._get_dbpath_for_data_path(D,ContentType.CONFIG_TRUE,F)
		if A==_B:raise NodeNotFound(_d+C)
		if _G in G:B,O=G.rsplit(_G,1)
		else:B=G
		assert type(A.node_ptr)==dict
		if B not in A.node_ptr:raise NodeNotFound('Cannot delete '+C+'.')
		await E._recursively_delete_subtable_data(A.row_id,C,A.node_ptr[B],delete_callbacks,I,F)
		if type(A.node_ptr[B])==list:
			K=re.sub(_F,'',C);L=E._find_rowids_in_table_having_pid(K,A.row_id,F);M=L.fetchall()
			if len(M)==0:assert type(A.node_ptr[B])==list;assert len(A.node_ptr[B])==0;A.node_ptr.pop(B)
		else:A.node_ptr.pop(B)
		E._update_jsob_for_row_id_in_table(A.table_name,A.row_id,A.jsob,F);J=re.sub(_F,'',D)
		if J in H:
			for N in H[J]:await N(D,A.jsob,A.jsob_data_path,I)
	async def _recursively_delete_subtable_data(A,pid,data_path,curr_data_iter,delete_callbacks,opaque,conn):
		H=conn;G=opaque;F=pid;D=delete_callbacks;C=curr_data_iter;B=data_path;E=re.sub(_F,'',B)
		if type(C)==list and E in A.table_keys:
			assert C==[];P,L=B.rsplit(_A,1)
			async def J(pid,data_path,delete_callbacks,opaque,conn):
				D=conn;C=data_path;F=re.sub(_F,'',C);B=A._get_dbpath_for_data_path(C,ContentType.CONFIG_TRUE,D)
				if B==_B:raise NodeNotFound(_d+C)
				G=next(iter(B.jsob));H=B.jsob[G];await A._recursively_delete_subtable_data(B.row_id,C,H,delete_callbacks,opaque,D);I=A.schema_path_to_real_table_name[F];E=A.metadata.tables[I];J=D.execute(sa.delete(E).where(E.c.row_id==B.row_id));assert J.rowcount==1
			if _G in L:await J(F,B,D,G,H)
			else:
				M=[B[0]for B in A._get_keys_in_table_having_pid(E,F,H)]
				for N in M:I=B+_G+N;await J(F,I,D,G,H)
		elif type(C)==dict:
			for K in C.keys():assert B!=_A;I=B+_A+K;await A._recursively_delete_subtable_data(F,I,C[K],D,G,H)
		else:0
		if not(type(C)==list and E in A.table_keys):
			if E in D:
				for O in D[E]:await O(B,G)
	def _find_rows_in_table_having_pid(B,table_name,pid,conn):C=B.schema_path_to_real_table_name[table_name];A=B.metadata.tables[C];D=conn.execute(sa.select([A]).where(A.c.pid==pid).order_by(A.c.row_id));return D
	def _find_rowids_in_table_having_pid(B,table_name,pid,conn):C=B.schema_path_to_real_table_name[table_name];A=B.metadata.tables[C];D=conn.execute(sa.select([A.c.row_id]).where(A.c.pid==pid).order_by(A.c.row_id));return D
	def _get_keys_in_table_having_pid(A,table_name,pid,conn):B=table_name;D=A.schema_path_to_real_table_name[B];C=A.metadata.tables[D];E=conn.execute(sa.select([getattr(C.c,A.table_keys[B])]).where(C.c.pid==pid));return E
	def _get_list_of_direct_subtables_for_schema_path(D,schema_path):
		A=schema_path
		if A!=_A:assert A[-1]!=_A;A+=_A
		C=[]
		for B in sorted(D.schema_path_to_real_table_name.keys()):
			if str(B).startswith(A):
				if not any((A for A in C if str(B).startswith(A+_A))):
					if str(B)!=_A:C.append(str(B))
					else:0
				else:0
		return C
	def _get_row_id_for_key_in_table(A,table_name,key,conn):
		B=table_name;E=A.schema_path_to_real_table_name[B];C=A.metadata.tables[E];F=conn.execute(sa.select([C.c.row_id]).where(getattr(C.c,A.table_keys[B])==key));D=F.first()
		if D==_B:return _B
		return D[0]
	def _get_jsob_iter_for_path_in_jsob(D,jsob,path):
		B=path;assert jsob!=_B;assert B[0]!=_A;A=jsob
		if B!='':
			for C in B.split(_A):
				if C!=''and C not in A:return _B
				A=A[C]
				if type(A)==list:assert len(A)==1;A=A[0]
		return A
	def _get_jsob_for_row_id_in_table(A,table_name,row_id,conn):D=A.schema_path_to_real_table_name[table_name];B=A.metadata.tables[D];E=conn.execute(sa.select([B.c.jsob]).where(B.c.row_id==row_id));C=E.first();assert C!=_B;return C[0]
	def _insert_jsob_into_table(A,pid,table_name,new_jsob,conn):D=new_jsob;C=table_name;E=A.schema_path_to_real_table_name[C];F=A.metadata.tables[E];G=next(iter(D));B={};B[_H]=pid;B[A.table_keys[C]]=D[G][A.table_keys[C]];B[_I]=D;H=conn.execute(F.insert().values(**B));return H.inserted_primary_key[0]
	def _update_jsob_for_row_id_in_table(A,table_name,row_id,new_jsob,conn):C=A.schema_path_to_real_table_name[table_name];B=A.metadata.tables[C];D=conn.execute(sa.update(B).where(B.c.row_id==row_id).values(jsob=new_jsob))
	def _get_table_name_for_schema_path(D,schema_path):
		B=len(_A);C=_E
		for A in D.schema_path_to_real_table_name.keys():
			if schema_path.startswith(A)and len(A)>B:B=len(A);C=A
		return C
	def _get_row_data_for_list_path(A,data_path,conn):
		B=data_path;assert B[0]==_A;assert B!=_A;assert B[-1]!=_A;G=B[1:].split(_A);assert _G in G[-1];D='';H=A.global_root_id
		for E in G:
			if _G in E:
				K,L=E.split(_G);D+=_A+K;I=A._get_table_name_for_schema_path(D);M=A.schema_path_to_real_table_name[I];C=A.metadata.tables[M];J=conn.execute(sa.select([C.c.row_id,C.c.pid]).where(and_(C.c.pid==H,getattr(C.c,A.table_keys[I])==L)));F=J.fetchone()
				if F==_B:return _B
				assert J.fetchone()==_B;H=F[_M]
			else:D+=_A+E
		return F
	def _get_dbpath_for_data_path(B,data_path,content_type,conn):
		C=data_path;A=DatabasePath();A.data_path=C;A.schema_path=re.sub(_F,'',C)
		if _G not in C:A.jsob_data_path=_A
		else:A.jsob_data_path=re.sub('(.*=[^/]*).*','\\g<1>',C)
		A.table_name=B._get_table_name_for_schema_path(A.schema_path)
		if A.table_name==_B:return _B
		if ContentType.CONFIG_FALSE in content_type and A.table_name in B.config_false_prefixes:
			raise NotImplementedError('Does this ever get called?')
			if A.table_name!=A.schema_path:return _B
			return _B
		D=re.findall(_c,C)
		if len(D)==0:A.row_id=B.global_root_id
		else:
			F=D[-1].split(_G);A.row_id=B._get_row_id_for_key_in_table(A.table_name,F[1],conn)
			if A.row_id==_B:return _B
		if A.table_name.endswith(_E):assert A.table_name==_E;assert len(D)==0;A.inside_path=A.schema_path[1:]
		else:
			assert len(D)!=0;A.inside_path=F[0];G=re.sub('^'+A.table_name,'',A.schema_path)
			if G!='':A.inside_path+=G
		if A.inside_path!=''and A.inside_path[0]==_A:raise NotImplementedError('can this be removed now?');A.inside_path=A.inside_path[1:]
		A.jsob=B._get_jsob_for_row_id_in_table(A.table_name,A.row_id,conn);A.node_ptr=A.jsob;A.prev_ptr=_B
		if A.inside_path=='':A.path_segments=[''];return A
		A.path_segments=A.inside_path.split(_A);H=''
		for E in A.path_segments:
			H+=_A+E
			if type(A.node_ptr)==list:A.prev_ptr=A.node_ptr;A.node_ptr=A.node_ptr[0]
			if E not in A.node_ptr:return _B
			else:A.prev_ptr=A.node_ptr;A.node_ptr=A.node_ptr[E]
		return A
	def _init(A,url,cert):
		F=url
		if not(F.startswith('sqlite:///')or F.startswith(_S)or F.startswith(_e)):raise SyntaxError('The database url contains an unrecognized dialect.')
		A.engine=sa.create_engine(F);A.db_schema=_B;A.table_keys={_E:_N};A.config_false_prefixes={};A.schema_path_to_real_table_name={};A.leafrefs={};A.referers={};A.ref_stat_collectors={}
		if A.engine.url.database==_T or not sqlalchemy_utils.database_exists(A.engine.url):A.engine=_B;raise NotImplementedError
		if A.engine.dialect.name==_U:A.schema_path_to_real_table_name[_A]=_E;A.schema_path_to_real_table_name[_E]=_E
		else:
			A.db_schema=A.engine.url.database;A.schema_path_to_real_table_name[_A]=A.db_schema.join(_O);A.schema_path_to_real_table_name[_E]=A.db_schema+_O;I=A.engine.execute(_f);G=I.fetchall();J=[G[A][0]for A in range(len(G))]
			if A.db_schema not in J:A.engine.execute(sa.schema.CreateSchema(A.db_schema));raise NotImplementedError
		A.metadata=sa.MetaData(bind=A.engine,schema=A.db_schema);A.metadata.reflect()
		for K in A.metadata.tables.values():
			for D in K.c:
				if type(D.type)is sa.sql.sqltypes.BLOB or type(D.type)is sa.sql.sqltypes.PickleType:D.type=sa.PickleType()
				if A.engine.dialect.name==_S and type(D.type)is sa.dialects.mysql.types.LONGTEXT:D.type=sa.JSON()
				elif type(D.type)is sa.sql.sqltypes.JSON:D.type=sa.JSON()
		B=A.metadata.tables[A.schema_path_to_real_table_name[_E]]
		with A.engine.connect()as E:
			C=E.execute(sa.select([B.c.jsob]).where(B.c.name==_g));H=C.first()[0]
			if H[_V]!=1:raise AssertionError('The database version ('+H[_V]+') is unexpected.')
			C=E.execute(sa.select([B.c.jsob]).where(B.c.name==_h));A.app_ns=C.first()[0];C=E.execute(sa.select([B.c.row_id]).where(B.c.name==_W));A.global_root_id=C.first()[0];C=E.execute(sa.select([B.c.jsob]).where(B.c.name==_i));A.table_keys=C.first()[0];C=E.execute(sa.select([B.c.jsob]).where(B.c.name==_j));A.schema_path_to_real_table_name=C.first()[0];C=E.execute(sa.select([B.c.jsob]).where(B.c.name==_k));A.config_false_prefixes=C.first()[0]
	def _create(A,url,cert,yl_obj,opaque):
		Q='default startup endpoint';P='endpoint';O='SZTPD_TEST_PATH';N='_sztp_ref_stats_stmt';M='_sztp_globally_unique_stmt';E=yl_obj;A.engine=sa.create_engine(url)
		if A.engine.url.database!=_T and sqlalchemy_utils.database_exists(A.engine.url):raise AssertionError('Database already exists (call init() first).')
		if A.engine.url.database!=_T:sqlalchemy_utils.create_database(A.engine.url)
		A.db_schema=_B
		if A.engine.dialect.name in(_S,_e):
			A.db_schema=str(A.engine.url.database);D=A.engine.execute(_f);F=D.fetchall();H=[F[A][0]for A in range(len(F))]
			if A.db_schema not in H:A.engine.execute('CREATE SCHEMA IF NOT EXISTS %s;'%A.db_schema)
		A.metadata=sa.MetaData(bind=A.engine,schema=A.db_schema);C=sa.Table(_E,A.metadata,sa.Column(_M,sa.Integer,primary_key=_D),sa.Column(_H,sa.Integer,unique=_D),sa.Column(_N,sa.String(250),unique=_D),sa.Column(_I,jsob_type));A.metadata.create_all()
		with A.engine.connect()as B:B.execute(C.insert(),name=_g,jsob={_V:1});B.execute(C.insert(),name=_h,jsob=A.app_ns);B.execute(C.insert(),name=_a,jsob=E);B.execute(C.insert(),name=_X,jsob=opaque)
		A.table_keys={_E:_N};A.config_false_prefixes={};A.schema_path_to_real_table_name={};A.leafrefs={};A.referers={};A.ref_stat_collectors={}
		if A.engine.dialect.name==_U:A.schema_path_to_real_table_name[_A]=_E;A.schema_path_to_real_table_name[_E]=_E
		else:A.schema_path_to_real_table_name[_A]=A.db_schema+_O;A.schema_path_to_real_table_name[_E]=A.db_schema+_O
		def I(self,stmt,sctx):self.globally_unique=stmt.argument
		setattr(yangson.schemanode.SchemaNode,M,I);yangson.schemanode.SchemaNode._stmt_callback['wn-app:globally-unique']=M
		def J(self,stmt,sctx):self.ref_stats=stmt.argument
		setattr(yangson.schemanode.SchemaNode,N,J);yangson.schemanode.SchemaNode._stmt_callback['wn-app:ref-stats']=N;G=pkg_resources.resource_filename('sztpd','yang/')
		if os.environ.get(O):A.dm=yangson.DataModel(json.dumps(E),[os.environ.get(O),G])
		else:A.dm=yangson.DataModel(json.dumps(E),[G])
		A._gen_tables(A.dm.schema,_E)
		with A.engine.connect()as B:D=B.execute(C.insert(),name=_j,jsob=A.schema_path_to_real_table_name);D=B.execute(C.insert(),name=_i,jsob=A.table_keys);D=B.execute(C.insert(),name=_k,jsob=A.config_false_prefixes)
		if os.environ.get('SZTPD_TEST_DAL'):
			with A.engine.connect()as B:D=B.execute(C.insert().values(name=_W,jsob={}))
			A.global_root_id=D.inserted_primary_key[0]
		else:
			with A.engine.connect()as B:D=B.execute(C.insert().values(name=_W,jsob={A.app_ns+':transport':{'listen':{P:[]}},A.app_ns+':audit-log':{}}))
			A.global_root_id=D.inserted_primary_key[0];K=A.schema_path_to_real_table_name[_A+A.app_ns+':transport/listen/endpoint'];L=A.metadata.tables[K]
			with A.engine.connect()as B:R=B.execute(L.insert().values(pid=A.global_root_id,name=Q,jsob={P:{_N:Q,'use-for':['native-interface'],'http':{'tcp-server-parameters':{'local-address':'127.0.0.1'}}}}))
	def _gen_tables(D,node,parent_table_name):
		R='ref_stats';G=parent_table_name;C=node
		if issubclass(type(C),yangson.schemanode.ListNode):
			B=[];B.append(sa.Column(_M,sa.Integer,primary_key=_D));N=D.schema_path_to_real_table_name[G];B.append(sa.Column(_H,sa.Integer,sa.ForeignKey(N+'.row_id'),index=_D,nullable=_C))
			if C.config==_D:
				if len(C.keys)>1:raise NotImplementedError('Only supports lists with at most one key.')
				E=C.get_child(*C.keys[0]);D.table_keys[C.data_path()]=E.name
				if type(E.type)==yangson.datatype.StringType:B.append(sa.Column(E.name,sa.String(250),nullable=_C))
				elif type(E.type)==yangson.datatype.Uint32Type:B.append(sa.Column(E.name,sa.Integer,nullable=_C))
				elif type(E.type)==yangson.datatype.IdentityrefType:B.append(sa.Column(E.name,sa.String(250),nullable=_C))
				elif type(E.type)==yangson.datatype.UnionType:B.append(sa.Column(E.name,sa.String(250),nullable=_C))
				else:raise Exception('Unsupported key node type: '+str(type(E.type)))
				if hasattr(E,'globally_unique'):B.append(sa.UniqueConstraint(E.name))
				else:B.append(sa.UniqueConstraint(E.name,_H))
				B.append(sa.Column(_I,jsob_type,nullable=_C))
			if C.config==_C:
				assert hasattr(C,R)==_C
				for A in C.children:
					if issubclass(type(A),yangson.schemanode.LeafNode):
						if type(A.type)==yangson.datatype.StringType:
							if str(A.type)=='date-and-time(string)':B.append(sa.Column(A.name,sa.DateTime,index=_D,nullable=A.mandatory==_C or A.when!=_B))
							else:B.append(sa.Column(A.name,sa.String(250),index=_D,nullable=A.mandatory==_C or A.when!=_B))
						elif type(A.type)==yangson.datatype.Uint16Type:B.append(sa.Column(A.name,sa.SmallInteger,index=_D,nullable=A.mandatory==_C or A.when!=_B))
						elif type(A.type)==yangson.datatype.InstanceIdentifierType:B.append(sa.Column(A.name,sa.String(250),nullable=A.mandatory==_C or A.when!=_B))
						elif type(A.type)==yangson.datatype.LeafrefType:B.append(sa.Column(A.name,sa.String(250),nullable=A.mandatory==_C or A.when!=_B))
						elif type(A.type)==yangson.datatype.IdentityrefType:B.append(sa.Column(A.name,sa.String(250),nullable=A.mandatory==_C or A.when!=_B))
						elif type(A.type)==yangson.datatype.EnumerationType:B.append(sa.Column(A.name,sa.String(250),index=_D,nullable=A.mandatory==_C or A.when!=_B))
						elif type(A.type)==yangson.datatype.UnionType:
							J=0;S=_D
							for K in A.type.types:
								if issubclass(type(K),yangson.datatype.StringType):J+=1
								else:raise Exception('Unhandled union type: '+str(type(K)))
							if J==len(A.type.types):B.append(sa.Column(A.name,sa.String(250),index=_D,nullable=A.mandatory==_C or A.when!=_B))
							else:raise Exception('FIXME: not all union subtypes are stringafiable')
						else:raise Exception('Unhandled leaf type: '+str(type(A.type)))
					elif issubclass(type(A),yangson.schemanode.ChoiceNode):
						H=_D
						for I in A.children:
							assert type(I)==yangson.schemanode.CaseNode
							if len(I.children)>1:H=_C;break
							else:
								for O in I.children:
									if type(O)!=yangson.schemanode.LeafNode:H=_C;break
						if H==_D:B.append(sa.Column(A.name,sa.String(250),index=_D,nullable=A.mandatory==_C or A.when!=_B))
						else:B.append(sa.Column(A.name,jsob_type,nullable=A.mandatory==_C or A.when!=_B))
					elif issubclass(type(A),yangson.schemanode.AnydataNode):B.append(sa.Column(A.name,jsob_type,nullable=A.mandatory==_C or A.when!=_B))
					elif issubclass(type(A),yangson.schemanode.LeafListNode):B.append(sa.Column(A.name,jsob_type,nullable=A.mandatory==_C or A.when!=_B))
					elif issubclass(type(A),yangson.schemanode.ListNode):B.append(sa.Column(A.name,jsob_type,nullable=A.mandatory==_C or A.when!=_B))
					elif issubclass(type(A),yangson.schemanode.ContainerNode):B.append(sa.Column(A.name,jsob_type,nullable=A.mandatory==_C or A.when!=_B))
					elif issubclass(type(A),yangson.schemanode.NotificationNode):0
					else:raise Exception('Unhandled list child type: '+str(type(A)))
			P=re.sub('^/.*:','',C.data_path()).split(_A)
			if D.engine.dialect.name==_U:F=''
			else:F=D.db_schema+'.'
			for Q in P:F+=Q[0]
			while F in D.schema_path_to_real_table_name.values():F+='2'
			D.schema_path_to_real_table_name[C.data_path()]=F
			if D.db_schema is _B:L=sa.Table(F,D.metadata,*B)
			else:L=sa.Table(re.sub('^'+D.db_schema+'.','',F),D.metadata,*B)
			L.create();G=C.data_path()
		if C.config==_C and issubclass(type(C),yangson.schemanode.DataNode):
			M=C.data_path()
			if not any((M.startswith(A)for A in D.config_false_prefixes)):D.config_false_prefixes[M]=_D
		if hasattr(C,R):D.ref_stat_collectors[C.data_path()]=_B
		if issubclass(type(C),yangson.schemanode.InternalNode):
			if not(type(C)==yangson.schemanode.ListNode and C.config==_C)and not type(C)==yangson.schemanode.RpcActionNode and not type(C)==yangson.schemanode.NotificationNode:
				for A in C.children:D._gen_tables(A,G)