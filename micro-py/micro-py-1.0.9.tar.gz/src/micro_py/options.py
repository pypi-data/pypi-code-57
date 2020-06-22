"""
    client_request_timeout value  Sets the client request timeout. e.g 500ms, 5s, 1m. Default: 5s [%MICRO_CLIENT_REQUEST_TIMEOUT%]
   --client_retries value          Sets the client retries. Default: 1 (default: 1) [%MICRO_CLIENT_RETRIES%]
   --client_pool_size value        Sets the client connection pool size. Default: 1 (default: 0) [%MICRO_CLIENT_POOL_SIZE%]
   --server_pool_size value        Sets the client connection pool size. Default: 1 (default: 0) [%MICRO_SERVER_POOL_SIZE%]
   --client_pool_ttl value         Sets the client connection pool ttl. e.g 500ms, 5s, 1m. Default: 1m [%MICRO_CLIENT_POOL_TTL%]
   --register_ttl value            Register TTL in seconds (default: 60) [%MICRO_REGISTER_TTL%]
   --register_interval value       Register interval in seconds (default: 30) [%MICRO_REGISTER_INTERVAL%]
   --server value                  Server for go-micro; rpc [%MICRO_SERVER%]
   --server_name value             Name of the server. go.micro.srv.example [%MICRO_SERVER_NAME%]
   --server_version value          Version of the server. 1.1.0 [%MICRO_SERVER_VERSION%]
   --server_id value               Id of the server. Auto-generated if not specified [%MICRO_SERVER_ID%]
   --server_address value          Bind address for the server. 127.0.0.1 [%MICRO_SERVER_ADDRESS%]
   --server_port value          Bind address for the server. 127.0.0.1 [%MICRO_SERVER_PORT%]
   --server_advertise value        Used instead of the server_address when registering with discovery. 127.0.0.1:8080 [%MICRO_SERVER_ADVERTISE%]
   --server_metadata value         A list of key-value pairs defining metadata. version=1.0.0 [%MICRO_SERVER_METADATA%]
   --broker value                  Broker for pub/sub. http, nats, rabbitmq [%MICRO_BROKER%]
   --broker_address value          Comma-separated list of broker addresses [%MICRO_BROKER_ADDRESS%]
   --profile value                 Debug profiler for cpu and memory stats [%MICRO_DEBUG_PROFILE%]
   --registry value                Registry for discovery. etcd, mdns [%MICRO_REGISTRY%]
   --registry_address value        Comma-separated list of registry addresses [%MICRO_REGISTRY_ADDRESS%]
   --runtime value                 Runtime for building and running services e.g local, kubernetes (default: "local") [%MICRO_RUNTIME%]
   --selector value                Selector used to pick nodes for querying [%MICRO_SELECTOR%]
   --transport value               Transport mechanism used; http [%MICRO_TRANSPORT%]
   --transport_address value       Comma-separated list of transport addresses [%MICRO_TRANSPORT_ADDRESS%]
   --local                         Enable local only development
   --enable_acme                   Enables ACME support via Let's Encrypt. ACME hosts should also be specified. [%MICRO_ENABLE_ACME%]
   --acme_hosts value              Comma separated list of hostnames to manage ACME certs for [%MICRO_ACME_HOSTS%]
   --acme_provider value           The provider that will be used to communicate with Let's Encrypt. Valid options: autocert, certmagic [%MICRO_ACME_PROVIDER%]
   --enable_tls                    Enable TLS support. Expects cert and key file to be specified [%MICRO_ENABLE_TLS%]
   --tls_cert_file value           Path to the TLS Certificate file [%MICRO_TLS_CERT_FILE%]
   --tls_key_file value            Path to the TLS Key file [%MICRO_TLS_KEY_FILE%]
   --tls_client_ca_file value      Path to the TLS CA file to verify clients against [%MICRO_TLS_CLIENT_CA_FILE%]

"""
import uuid
import socket


def get_open_port():
    """
    获取随机可用的端口
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


def get_ip_address():
    """
    获取本机ip
    :return:
    """
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    # fqdnName = socket.getfqdn(socket.gethostname())
    # ip = socket.gethostbyname(fqdnName)

    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.connect(('baidu.com', 0))
    # ip = s.getsockname()[0]

    return ip


OPS = {
    "client_request_timeout": ["MICRO_CLIENT_REQUEST_TIMEOUT", 5],
    "client_retries": ["MICRO_CLIENT_RETRIES", 1],
    "client_pool_size": ["MICRO_CLIENT_POOL_SIZE", 1],
    "client_pool_ttl": ["MICRO_CLIENT_POOL_TTL", 60],
    "register_ttl": ["MICRO_REGISTER_TTL", 600],
    "register_interval": ["MICRO_REGISTER_INTERVAL", 300],
    "server_name": ["MICRO_SERVER_NAME", "go.micro.srv.example"],
    "server_version": ["MICRO_SERVER_VERSION", " 1.1.0"],
    "server_id": ["MICRO_SERVER_ID", uuid.uuid4()],
    "server_address": ["MICRO_SERVER_ADDRESS", get_ip_address()],
    "server_port": ["MICRO_SERVER_PORT", get_open_port()],
    "server_pool_size": ["MICRO_SERVER_POOL_SIZE", 1],
    "registry": ["MICRO_REGISTRY", ""],
    "registry_address": ["MICRO_REGISTRY_ADDRESS", ""],
}
