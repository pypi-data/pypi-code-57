def pytest_addoption(parser):
    parser.addoption(
        "--enough-hosts",
        action="store",

        default="bind-host,postfix-host,icinga-host,cloud-host",
        help="list of hosts"
    )
    parser.addoption(
        "--enough-service",
        action="store",
        default="cloud",
        help="service"
    )
