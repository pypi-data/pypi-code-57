from nomnomdata.engine.components import Connection, Parameter, ParameterGroup
from nomnomdata.engine.parameters import Enum, Int, String

AWSTokenConnection = Connection(
    connection_type_uuid="AWS5D-TO99M",
    description="AWS Access Key Information",
    alias="AWS:Token",
    categories=["aws", "access", "credentials"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                type=String(),
                name="aws_access_key_id",
                display_name="Access Key ID",
                description="First part of the Access Key.",
                required=True,
            ),
            Parameter(
                type=String(),
                name="aws_secret_access_key",
                display_name="Secret Access Key",
                description="Second part of the Access Key.",
                required=True,
            ),
            Parameter(
                type=String(),
                name="region",
                display_name="Region",
                description="Specify the AWS region that the session will be created within.",
                required=True,
            ),
            name="secret_info",
            display_name="Secret Info",
        ),
    ],
)

AWSS3BucketConnection = Connection(
    connection_type_uuid="AWSS3-BKH32",
    alias="AWS:Database:Redshift Legacy",
    description="Redshift database configuration and options.",
    categories=["aws", "redshift", "database"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                type=String(),
                name="bucket",
                display_name="Bucket",
                description="Name of the Bucket",
                required=True,
            ),
            Parameter(
                type=String(),
                name="endpoint_url",
                display_name="S3 Endpoint URL",
                description="S3 Endpoint url for non-AWS hosted buckets",
            ),
            Parameter(
                type=String(),
                name="prefix",
                display_name="Folder Path Prefix",
                description="S3 Endpoint url for non-AWS hosted buckets",
            ),
            Parameter(
                type=String(),
                name="s3_temp_space",
                display_name="S3 Temporary Path",
                description="S3 Endpoint url for non-AWS hosted buckets",
            ),
            name="bucket_info",
            display_name="Bucket Info",
        ),
        ParameterGroup(
            Parameter(
                type=String(),
                name="access_key_id",
                display_name="Access Key ID",
                description="First part of the Access Key.",
                required=True,
            ),
            Parameter(
                type=String(),
                name="secret_access_key",
                display_name="Secret Access Key",
                description="Second part of the Access Key.",
                required=True,
            ),
            name="secret_info",
            display_name="Secret Info",
        ),
    ],
)

FTPConnection = Connection(
    connection_type_uuid="FTP92-TS0BZ",
    alias="FTP",
    description="FTP, FTPS or SFTP configuration.",
    categories=["generic", "ftp", "ftps"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                type=Enum(choices=["FTP", "FTPS Explicit", "SFTP"]),
                name="type",
                display_name="FTP Type",
                description="Type of FTP authentication to use",
                required=True,
            ),
            name="authentication_parameters",
            display_name="Authentication Parameters",
        ),
        ParameterGroup(
            Parameter(
                type=String(), name="host_name", display_name="Hostname", required=True
            ),
            Parameter(
                type=Int(min=1, max=65535),
                name="port",
                display_name="FTP Port",
                description="Port 21 is the typical port for FTP and explicitly negotiated FTPS. Port 22 is the typical port for SFTP.",
                required=True,
                default=21,
            ),
            Parameter(type=String(), name="username", display_name="Username",),
            Parameter(type=String(), name="password", display_name="Password",),
            Parameter(
                type=String(),
                name="ssh_key",
                display_name="SSH Private Key",
                description="This field is only used for key based SFTP authentication.",
            ),
            name="server_parameters",
            description="Server Parameters",
        ),
    ],
)
