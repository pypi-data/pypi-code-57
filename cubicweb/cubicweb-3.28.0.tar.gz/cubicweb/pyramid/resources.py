# copyright 2017 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# copyright 2014-2016 UNLISH S.A.S. (Montpellier, FRANCE), all rights reserved.
#
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of CubicWeb.
#
# CubicWeb is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# CubicWeb is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with CubicWeb.  If not, see <http://www.gnu.org/licenses/>.

from pyramid.httpexceptions import HTTPNotFound

from cubicweb import rdf


def negociate_mime_type(request, possible_mimetypes):
    accepted_headers_by_weight = sorted(
        request.accept.parsed or [], key=lambda h: h[1], reverse=True
    )
    mime_type_negociated = None
    for parsed_header in accepted_headers_by_weight:
        accepted_mime_type = parsed_header[0]
        if accepted_mime_type in possible_mimetypes:
            mime_type_negociated = accepted_mime_type
            break
    return mime_type_negociated


def rdf_context_from_eid(request):
    mime_type = negociate_mime_type(request, rdf.RDF_MIMETYPE_TO_FORMAT)
    if mime_type is None:
        raise HTTPNotFound()
    entity = request.cw_request.entity_from_eid(request.matchdict['eid'])
    return RDFResource(entity, mime_type)


class RDFResource:
    def __init__(self, entity, mime_type):
        self.entity = entity
        self.mime_type = mime_type
