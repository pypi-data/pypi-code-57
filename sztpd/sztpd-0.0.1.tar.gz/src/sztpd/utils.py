# Copyright (c) 2020 Watsen Networks.  All Rights Reserved.

_D='content'
_C='certificates'
_B='certificate'
_A='contentType'
import re,pem,base64,textwrap
from pyasn1.type import tag,univ
from pyasn1_modules import rfc5652
from pyasn1_modules import rfc5280
from pyasn1.codec.der import decoder as der_decoder
from pyasn1.codec.der import encoder as der_encoder
def multipart_pem_to_der_dict(multipart_pem):
	A={};E=pem.parse(bytes(multipart_pem,'utf-8'))
	for F in E:
		C=F.as_text().splitlines();D=base64.b64decode(''.join(C[1:-1]));B=re.sub('-----BEGIN (.*)-----','\\g<1>',C[0])
		if B not in A:A[B]=[D]
		else:A[B].append(D)
	return A
def der_dict_to_multipart_pem(der_dict):
	H='-----\n';C=der_dict;A='';D=C.keys()
	for B in D:
		E=C[B]
		for F in E:G=base64.b64encode(F).decode('ASCII');A+='-----BEGIN '+B+H;A+=textwrap.fill(G,64)+'\n';A+='-----END '+B+H
	return A
def ders_to_degenerate_cms_obj(cert_ders):
	B=rfc5652.CertificateSet().subtype(implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,0))
	for E in cert_ders:F,G=der_decoder.decode(E,asn1Spec=rfc5280.Certificate());assert not G;D=rfc5652.CertificateChoices();D[_B]=F;B[len(B)]=D
	A=rfc5652.SignedData();A['version']=1;A['digestAlgorithms']=rfc5652.DigestAlgorithmIdentifiers().clear();A['encapContentInfo']['eContentType']=rfc5652.id_data;A[_C]=B;C=rfc5652.ContentInfo();C[_A]=rfc5652.id_signedData;C[_D]=der_encoder.encode(A);return C
def degenerate_cms_obj_to_ders(cms_obj):
	A=cms_obj
	if A[_A]!=rfc5652.id_signedData:raise KeyError('unexpected content type: '+str(A[_A]))
	D,H=der_decoder.decode(A[_D],asn1Spec=rfc5652.SignedData());E=D[_C];B=[]
	for F in E:C=F[_B];assert type(C)==rfc5280.Certificate;G=der_encoder.encode(C);B.append(G)
	return B