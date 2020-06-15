#  BSD 3-Clause License
#
#  Copyright (c) 2019, Elasticsearch BV
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
#  * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
#  * Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import decimal
import re
import base64


EVENTS_API_PATH = "v1"
AGENT_CONFIG_PATH = "/api/graphql"

TRACE_CONTEXT_VERSION = 0
TRACEPARENT_HEADER_NAME = "traceparent"
TRACESTATE_HEADER_NAME = "tracestate"

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

KEYWORD_MAX_LENGTH = 1024

HTTP_WITH_BODY = {"POST", "PUT", "PATCH", "DELETE"}
MAX_BODY_SIZE = 512000
MASK = 8 * "*"
ENCODED_MASK = base64.b64encode(MASK.encode('utf-8'))

EXCEPTION_CHAIN_MAX_DEPTH = 50

ERROR = "error"
TRANSACTION = "transaction"
SPAN = "span"
METRICSET = "metricset"
EVENT = "event"

LABEL_RE = re.compile('[.*"]')
HARDCODED_PROCESSORS = []

DEFAULT_SANITIZE_FIELD_NAMES = frozenset(
    ["authorization", "password", "secret", "passwd", "password", "token", "api_key", "access_token", "sessionid"]
)
HOST_BLACK_LIST = set(['app.hoss.com', 'app.hossapp.dev', "ingress.hoss.com", "ingress.hossapp.dev", 'apitracker.net', 'apitracker.com'])

try:
    # Python 2
    LABEL_TYPES = (bool, int, long, float, decimal.Decimal)
except NameError:
    # Python 3
    LABEL_TYPES = (bool, int, float, decimal.Decimal)

AGENT_CONFIG_GRAPHQL_QUERY = """
query AgentConfig {
  agentConfig {
    accountApiConfiguration {
      uuid
      hostBlacklist
      sanitizedHeaders
      sanitizedQueryParams
      sanitizedBodyFields {
        type
        value
      }
      bodyCapture
    }
    apis {
      uuid
      name
      rootDomain
      hosts
      logo
      configuration(mergeWithAccountConfiguration: true) {
        uuid
        sanitizedHeaders
        sanitizedQueryParams
        bodyCapture
        sanitizedBodyFields {
          type
          value
        }
      }
    }
  }
}
"""