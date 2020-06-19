"""Constants file."""
PACKAGE_NAME = "veeam_em"

__version__ = '0.0.1'

API_ENDPOINT_BASE = 'https://localhost:9398'
API_VERSION = 'latest'
API_DEFAULT_CONTENT_TYPE = 'application/json'
API_DEFAULT_XMLNS = 'http://www.veeam.com/ent/v1.0'

DEFAULT_TIMEOUT = 60
DEFAULT_DEBUG = False
VERIFY_SSL = True
DATETIME_FMT = '%Y-%m-%d %H:%M'

HORT_PLATFORMS = {
    'VMware': [
        "VM",
        "Host",
        "Cluster",
        "Template",
        "VirtualApp",
        "Vc",
        "Datacenter",
        "Folder",
        "Datastore",
        "ComputeResource",
        "ResourcePool",
        "Tag",
        "Category",
        "StoragePod",
    ],
    'Hyperv': ["Vm", "Host", "Cluster", "Scvmm", "HostGroup", "VmGroup"],
    'vCloud': [
        "VcdSystem",
        "Organization",
        "OrgVdc",
        "Vapp",
        "Vm",
        "VappTemplate",
        "VmTemplate",
    ],
}
