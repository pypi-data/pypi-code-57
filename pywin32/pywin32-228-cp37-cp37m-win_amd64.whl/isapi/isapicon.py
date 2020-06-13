"""Constants needed by ISAPI filters and extensions."""
#  ======================================================================
#  Copyright 2002-2003 by Blackdog Software Pty Ltd.
# 
#                          All Rights Reserved
# 
#  Permission to use, copy, modify, and distribute this software and
#  its documentation for any purpose and without fee is hereby
#  granted, provided that the above copyright notice appear in all
#  copies and that both that copyright notice and this permission
#  notice appear in supporting documentation, and that the name of 
#  Blackdog Software not be used in advertising or publicity pertaining to
#  distribution of the software without specific, written prior
#  permission.
# 
#  BLACKDOG SOFTWARE DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
#  INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN
#  NO EVENT SHALL BLACKDOG SOFTWARE BE LIABLE FOR ANY SPECIAL, INDIRECT OR
#  CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
#  OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
#  NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
#  CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#  ======================================================================

# HTTP reply codes

HTTP_CONTINUE                     = 100
HTTP_SWITCHING_PROTOCOLS          = 101
HTTP_PROCESSING                   = 102
HTTP_OK                           = 200
HTTP_CREATED                      = 201
HTTP_ACCEPTED                     = 202
HTTP_NON_AUTHORITATIVE            = 203
HTTP_NO_CONTENT                   = 204
HTTP_RESET_CONTENT                = 205
HTTP_PARTIAL_CONTENT              = 206
HTTP_MULTI_STATUS                 = 207
HTTP_MULTIPLE_CHOICES             = 300
HTTP_MOVED_PERMANENTLY            = 301
HTTP_MOVED_TEMPORARILY            = 302
HTTP_SEE_OTHER                    = 303
HTTP_NOT_MODIFIED                 = 304
HTTP_USE_PROXY                    = 305
HTTP_TEMPORARY_REDIRECT           = 307
HTTP_BAD_REQUEST                  = 400
HTTP_UNAUTHORIZED                 = 401
HTTP_PAYMENT_REQUIRED             = 402
HTTP_FORBIDDEN                    = 403
HTTP_NOT_FOUND                    = 404
HTTP_METHOD_NOT_ALLOWED           = 405
HTTP_NOT_ACCEPTABLE               = 406
HTTP_PROXY_AUTHENTICATION_REQUIRED= 407
HTTP_REQUEST_TIME_OUT             = 408
HTTP_CONFLICT                     = 409
HTTP_GONE                         = 410
HTTP_LENGTH_REQUIRED              = 411
HTTP_PRECONDITION_FAILED          = 412
HTTP_REQUEST_ENTITY_TOO_LARGE     = 413
HTTP_REQUEST_URI_TOO_LARGE        = 414
HTTP_UNSUPPORTED_MEDIA_TYPE       = 415
HTTP_RANGE_NOT_SATISFIABLE        = 416
HTTP_EXPECTATION_FAILED           = 417
HTTP_UNPROCESSABLE_ENTITY         = 422
HTTP_INTERNAL_SERVER_ERROR        = 500
HTTP_NOT_IMPLEMENTED              = 501
HTTP_BAD_GATEWAY                  = 502
HTTP_SERVICE_UNAVAILABLE          = 503
HTTP_GATEWAY_TIME_OUT             = 504
HTTP_VERSION_NOT_SUPPORTED        = 505
HTTP_VARIANT_ALSO_VARIES          = 506

HSE_STATUS_SUCCESS                  = 1
HSE_STATUS_SUCCESS_AND_KEEP_CONN    = 2
HSE_STATUS_PENDING                  = 3
HSE_STATUS_ERROR                    = 4

SF_NOTIFY_SECURE_PORT               = 0x00000001
SF_NOTIFY_NONSECURE_PORT            = 0x00000002
SF_NOTIFY_READ_RAW_DATA             = 0x00008000
SF_NOTIFY_PREPROC_HEADERS           = 0x00004000
SF_NOTIFY_AUTHENTICATION            = 0x00002000
SF_NOTIFY_URL_MAP                   = 0x00001000
SF_NOTIFY_ACCESS_DENIED             = 0x00000800
SF_NOTIFY_SEND_RESPONSE             = 0x00000040
SF_NOTIFY_SEND_RAW_DATA             = 0x00000400
SF_NOTIFY_LOG                       = 0x00000200
SF_NOTIFY_END_OF_REQUEST            = 0x00000080
SF_NOTIFY_END_OF_NET_SESSION        = 0x00000100

SF_NOTIFY_ORDER_HIGH                = 0x00080000
SF_NOTIFY_ORDER_MEDIUM              = 0x00040000
SF_NOTIFY_ORDER_LOW                 = 0x00020000
SF_NOTIFY_ORDER_DEFAULT             = SF_NOTIFY_ORDER_LOW

SF_NOTIFY_ORDER_MASK               = (SF_NOTIFY_ORDER_HIGH   |    \
                                      SF_NOTIFY_ORDER_MEDIUM |    \
                                      SF_NOTIFY_ORDER_LOW)

SF_STATUS_REQ_FINISHED = 134217728 # 0x8000000
SF_STATUS_REQ_FINISHED_KEEP_CONN = 134217728 + 1
SF_STATUS_REQ_NEXT_NOTIFICATION = 134217728 + 2
SF_STATUS_REQ_HANDLED_NOTIFICATION = 134217728 + 3
SF_STATUS_REQ_ERROR = 134217728 + 4
SF_STATUS_REQ_READ_NEXT = 134217728 + 5

HSE_IO_SYNC =                    0x00000001   # for WriteClient
HSE_IO_ASYNC =                   0x00000002   # for WriteClient/TF/EU
HSE_IO_DISCONNECT_AFTER_SEND =   0x00000004   # for TF
HSE_IO_SEND_HEADERS =            0x00000008   # for TF
HSE_IO_NODELAY =                 0x00001000   # turn off nagling 
# These two are only used by VectorSend
HSE_IO_FINAL_SEND =              0x00000010
HSE_IO_CACHE_RESPONSE =          0x00000020

HSE_EXEC_URL_NO_HEADERS =                    0x02
HSE_EXEC_URL_IGNORE_CURRENT_INTERCEPTOR =    0x04
HSE_EXEC_URL_IGNORE_VALIDATION_AND_RANGE =   0x10
HSE_EXEC_URL_DISABLE_CUSTOM_ERROR =          0x20
HSE_EXEC_URL_SSI_CMD =                       0x40
HSE_EXEC_URL_HTTP_CACHE_ELIGIBLE =           0x80
