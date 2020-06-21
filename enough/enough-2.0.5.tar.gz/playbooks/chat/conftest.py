def pytest_addoption(parser):
    parser.addoption(
        "--enough-hosts",
        action="store",

        default="bind-host,chat-host,icinga-host",
        help="list of hosts"
    )
    parser.addoption(
        "--enough-service",
        action="store",
        default="chat",
        help="service"
    )
