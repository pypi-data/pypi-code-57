# manual stuff
from pywintypes import IID
PSGUID_STORAGE             = IID('{B725F130-47EF-101A-A5F1-02608C9EEBAC}')
PSGUID_SUMMARYINFORMATION  = IID('{F29F85E0-4FF9-1068-AB91-08002B27B3D9}')
PSGUID_HTMLINFORMATION     = IID('{D1B5D3F0-C0B3-11CF-9A92-00A0C908DBF1}')
PSGUID_HTML2_INFORMATION   = IID('{C82BF597-B831-11D0-B733-00AA00A1EBD2}')

IFILTER_INIT_CANON_PARAGRAPHS	= 1
IFILTER_INIT_HARD_LINE_BREAKS	= 2
IFILTER_INIT_CANON_HYPHENS	= 4
IFILTER_INIT_CANON_SPACES	= 8
IFILTER_INIT_APPLY_INDEX_ATTRIBUTES	= 16
IFILTER_INIT_APPLY_CRAWL_ATTRIBUTES  = 256
IFILTER_INIT_APPLY_OTHER_ATTRIBUTES	= 32
IFILTER_INIT_INDEXING_ONLY	= 64
IFILTER_INIT_SEARCH_LINKS	= 128
IFILTER_INIT_FILTER_OWNED_VALUE_OK = 512

IFILTER_FLAGS_OLE_PROPERTIES	= 1

CHUNK_TEXT	= 0x1
CHUNK_VALUE	= 0x2
CHUNK_NO_BREAK	= 0
CHUNK_EOW	= 1
CHUNK_EOS	= 2
CHUNK_EOP	= 3
CHUNK_EOC	= 4

NOT_AN_ERROR = 0x00080000
FILTER_E_END_OF_CHUNKS = -2147215616
FILTER_E_NO_MORE_TEXT = -2147215615
FILTER_E_NO_MORE_VALUES = -2147215614
FILTER_E_ACCESS = -2147215613
FILTER_W_MONIKER_CLIPPED = 0x00041704
FILTER_E_NO_TEXT = -2147215611
FILTER_E_NO_VALUES = -2147215610
FILTER_E_EMBEDDING_UNAVAILABLE = -2147215609
FILTER_E_LINK_UNAVAILABLE = -2147215608
FILTER_S_LAST_TEXT = 0x00041709
FILTER_S_LAST_VALUES = 0x0004170A
FILTER_E_PASSWORD = -2147215605
FILTER_E_UNKNOWNFORMAT = -2147215604

# Generated by h2py from PropIdl.h
PROPSETFLAG_DEFAULT = ( 0 )
PROPSETFLAG_NONSIMPLE = ( 1 )
PROPSETFLAG_ANSI = ( 2 )
PROPSETFLAG_UNBUFFERED = ( 4 )
PROPSETFLAG_CASE_SENSITIVE = ( 8 )
PROPSET_BEHAVIOR_CASE_SENSITIVE = ( 1 )
PID_DICTIONARY = ( 0 )
PID_CODEPAGE = ( 0x1 )
PID_FIRST_USABLE = ( 0x2 )
PID_FIRST_NAME_DEFAULT = ( 0xfff )
PID_LOCALE = ( (-2147483648) )
PID_MODIFY_TIME = ( (-2147483647) )
PID_SECURITY = ( (-2147483646) )
PID_BEHAVIOR = ( (-2147483645) )
PID_ILLEGAL = ( (-1) )
PID_MIN_READONLY = ( (-2147483648) )
PID_MAX_READONLY = ( (-1073741825) )
PIDDI_THUMBNAIL = 0x00000002
PIDSI_TITLE = 0x00000002
PIDSI_SUBJECT = 0x00000003
PIDSI_AUTHOR = 0x00000004
PIDSI_KEYWORDS = 0x00000005
PIDSI_COMMENTS = 0x00000006
PIDSI_TEMPLATE = 0x00000007
PIDSI_LASTAUTHOR = 0x00000008
PIDSI_REVNUMBER = 0x00000009
PIDSI_EDITTIME = 0x0000000a
PIDSI_LASTPRINTED = 0x0000000b
PIDSI_CREATE_DTM = 0x0000000c
PIDSI_LASTSAVE_DTM = 0x0000000d
PIDSI_PAGECOUNT = 0x0000000e
PIDSI_WORDCOUNT = 0x0000000f
PIDSI_CHARCOUNT = 0x00000010
PIDSI_THUMBNAIL = 0x00000011
PIDSI_APPNAME = 0x00000012
PIDSI_DOC_SECURITY = 0x00000013
PIDDSI_CATEGORY = 0x00000002
PIDDSI_PRESFORMAT = 0x00000003
PIDDSI_BYTECOUNT = 0x00000004
PIDDSI_LINECOUNT = 0x00000005
PIDDSI_PARCOUNT = 0x00000006
PIDDSI_SLIDECOUNT = 0x00000007
PIDDSI_NOTECOUNT = 0x00000008
PIDDSI_HIDDENCOUNT = 0x00000009
PIDDSI_MMCLIPCOUNT = 0x0000000A
PIDDSI_SCALE = 0x0000000B
PIDDSI_HEADINGPAIR = 0x0000000C
PIDDSI_DOCPARTS = 0x0000000D
PIDDSI_MANAGER = 0x0000000E
PIDDSI_COMPANY = 0x0000000F
PIDDSI_LINKSDIRTY = 0x00000010
PIDMSI_EDITOR = 0x00000002
PIDMSI_SUPPLIER = 0x00000003
PIDMSI_SOURCE = 0x00000004
PIDMSI_SEQUENCE_NO = 0x00000005
PIDMSI_PROJECT = 0x00000006
PIDMSI_STATUS = 0x00000007
PIDMSI_OWNER = 0x00000008
PIDMSI_RATING = 0x00000009
PIDMSI_PRODUCTION = 0x0000000A
PIDMSI_COPYRIGHT = 0x0000000B
PRSPEC_INVALID = -1
PRSPEC_LPWSTR = 0
PRSPEC_PROPID = 1
CCH_MAX_PROPSTG_NAME = 31
