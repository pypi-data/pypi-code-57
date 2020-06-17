import getpass
import os
import dill
import toml
from dotenv import load_dotenv
from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client
from neo.libs import utils
from tabulate import tabulate


GLOBAL_HOME = os.path.expanduser("~")
GLOBAL_AUTH_URL = "https://keystone.wjv-1.neo.id:443/v3"
GLOBAL_USER_DOMAIN_NAME = "neo.id"
GLOBAL_REGION = {
    "wjv": "https://keystone.wjv-1.neo.id:443/v3",
    "jkt": "https://keystone.jkt-1.neo.id:443/v3",
}
DEFAULT_REGION = "wjv"


def get_username():
    return input("username: ")


def get_password():
    return getpass.getpass("password: ")


def get_region():
    show_region_list()
    region = input("region (Default: wjv): ")
    region = region.lower()
    try:
        if region == "":
            region = "wjv"
        print(GLOBAL_REGION[region])
        return GLOBAL_REGION[region]
    except KeyError:
        utils.log_err("Region not found, please check your region input")
        exit()


def show_region_list():
    print(
        tabulate(
            [[region, GLOBAL_REGION[region]] for region in GLOBAL_REGION],
            headers=["Region", "Auth URL"],
            tablefmt="fancy_grid",
        )
    )


def get_region_toml(username, password, auth_url):
    config = ""
    for region in GLOBAL_REGION:
        status = "ACTIVE" if GLOBAL_REGION[region] == auth_url else "IDLE"
        project_id = get_project_id(
            username, password, GLOBAL_REGION[region], GLOBAL_USER_DOMAIN_NAME
        )
        region_list = f"""
                        [region.{region}]
                        os_auth_url = "{GLOBAL_REGION[region]}"
                        os_project_id = "{project_id}"
                        os_user_domain_name = "{GLOBAL_USER_DOMAIN_NAME}"
                        status = "{status}"
                    """
        config += region_list
    return config


def generate_session(username, password, auth_url, user_domain_name, project_id=None):
    auth = v3.Password(
        username=username,
        password=password,
        project_id=project_id,
        auth_url=auth_url,
        user_domain_name=user_domain_name,
        reauthenticate=True,
        include_catalog=True,
    )
    sess = session.Session(auth=auth)
    return sess


def get_toml_config():
    return os.path.join(GLOBAL_HOME, ".neo", "config.toml")


def check_env():
    return os.path.isfile(get_toml_config())


def create_env_file(username, password, auth_url):
    region = get_region_toml(username, password, auth_url)
    config_list = f"""
                   [auth]
                   os_username = "{username}"
                   os_password = "{password}"
                   {region} 
                """
    configs = toml.loads(config_list)
    try:
        config_toml = get_toml_config()
        os.makedirs(os.path.dirname(config_toml), exist_ok=True)
        env_file = open(config_toml, "w+")
        env_file.write(toml.dumps(configs))
        env_file.close()
        return True
    except Exception as e:
        utils.log_err(e)
        return False


def load_env_file():
    if check_env():
        return toml.load(get_toml_config())


def get_env_values():
    if check_env():
        env_toml = load_env_file()
        neo_env = []
        for region in GLOBAL_REGION:
            default = "(default)" if region == DEFAULT_REGION else ""
            list_env = {
                "username": env_toml.get("auth").get("os_username"),
                "password": env_toml.get("auth").get("os_password"),
                "region": region + default,
                "auth_url": env_toml.get("region").get(region).get("os_auth_url"),
                "project_id": env_toml.get("region").get(region).get("os_project_id"),
                "user_domain_name": env_toml.get("region")
                .get(region)
                .get("os_user_domain_name"),
                "status": env_toml.get("region").get(region).get("status"),
            }
            neo_env.append(list_env)
        return neo_env
    # else:
    #    utils.log_err("Can't find NEO environment configuration. Maybe you haven't login yet?")


def is_current_env(auth_url, user_domain_name, username):
    """ check if auth_url and user_domain_name differ from current ~/.neo/config.toml"""
    envs = get_env_values()
    for env in envs:
        if (
            env["auth_url"] == auth_url
            and env["user_domain_name"] == user_domain_name
            and env["username"] == username
            and env["status"] == "ACTIVE"
        ):
            return True
        else:
            continue


def get_active_env():
    if check_env():
        env_toml = load_env_file()
        active_env = {}
        for region in GLOBAL_REGION:
            if (env_toml.get("region").get(region).get("status")) == "ACTIVE":
                active_env["username"] = env_toml.get("auth").get("os_username")
                active_env["password"] = env_toml.get("auth").get("os_password")
                active_env["auth_url"] = (
                    env_toml.get("region").get(region).get("os_auth_url")
                )
                active_env["project_id"] = (
                    env_toml.get("region").get(region).get("os_project_id")
                )
                active_env["user_domain_name"] = (
                    env_toml.get("region").get(region).get("os_user_domain_name")
                )
                dump_session(
                    generate_session(
                        active_env["username"],
                        active_env["password"],
                        active_env["auth_url"],
                        active_env["user_domain_name"],
                        active_env["project_id"],
                    )
                )
                return active_env
            else:
                continue


def get_project_id(username, password, auth_url, user_domain_name):
    sess = generate_session(
        username=username,
        password=password,
        auth_url=auth_url,
        user_domain_name=user_domain_name,
    )
    keystone = client.Client(session=sess)
    # project_list = [t.id for t in keystone.projects.list(user=sess.get_user_id())]
    enabled_project = []
    for project in keystone.projects.list(user=sess.get_user_id()):
        if project.enabled == True:
            enabled_project.append(project.id)

    if len(enabled_project) == 0:
        utils.log_err("Something wrong with your project. Please contact Support")
        exit()
    elif len(enabled_project) > 1:
        return enabled_project[0]
    else:
        return enabled_project[0]


def do_fresh_login(username=None, auth_url=None):
    if username != None:
        username = username
        password = get_password()
        auth_url = auth_url
    else:
        username = get_username()
        password = get_password()
        if auth_url != None:
            auth_url = auth_url
        else:
            auth_url = get_region()

    try:
        project_id = get_project_id(
            username, password, auth_url, GLOBAL_USER_DOMAIN_NAME
        )
        dump_session(
            generate_session(
                auth_url=auth_url,
                username=username,
                password=password,
                project_id=project_id,
                user_domain_name=GLOBAL_USER_DOMAIN_NAME,
            )
        )
        # generate fresh neo.env
        # passing username and password to pass toml config
        create_env_file(username, password, auth_url)
        utils.log_info("Login Success")
    except Exception as e:
        utils.log_err(e)
        utils.log_err("Login Failed")


def regenerate_sess():
    """ Regenerate session from old neo.env"""
    env_data = get_active_env()
    dump_session(
        generate_session(
            auth_url=env_data["auth_url"],
            username=env_data["username"],
            password=env_data["password"],
            project_id=env_data["project_id"],
            user_domain_name=env_data["user_domain_name"],
        )
    )


def login_check(username=None, region=None):
    try:
        print("Connecting to region " + region + " at " + GLOBAL_REGION[region])
        auth_url = GLOBAL_REGION[region]
        old_env_data = get_active_env()
        if check_env() and check_session():
            if is_current_env(
                auth_url, GLOBAL_USER_DOMAIN_NAME, username=old_env_data["username"]
            ):
                print("You have logged in")
                print("You are already logged.")
                print("  use 'neo login -D' to see your current account")
            else:
                print("You have switch user or region, doing relogin")
                do_fresh_login(username, auth_url)
        elif check_env() and not check_session():
            print("Retrieving old login data ...")
            regenerate_sess()
            utils.log_info("Login Success")
        else:
            do_fresh_login(username, auth_url)
    except KeyError as e:
        utils.log_err("Region " + str(e) + " is  not found")


def do_login(username=None, region=None):
    if region == None and username == None:
        if check_env() and check_session():
            print("You have logged in")
            print("  use 'neo login -D' to see your current account")
        else:
            do_fresh_login()
    elif region == None or username == None:
        if username == None:
            utils.log_err("You need to specify a username")
        elif region == None:
            login_check(username, DEFAULT_REGION)
    else:
        region = region.lower()
        login_check(username, region)


def do_logout():
    temp = utils.tmp_dir()
    if check_session():
        home = os.path.expanduser("~")
        os.remove(os.path.join(temp, "session.pkl"))
        utils.del_tmp_dir(temp)
        os.remove(get_toml_config())
        utils.log_info("Logout Success")


def dump_session(sess):
    temp = utils.tmp_dir()
    try:
        with open("{}/session.pkl".format(temp), "wb") as f:
            dill.dump(sess, f)
    except:
        utils.log_err("Dump session failed")


def load_dumped_session():
    temp = utils.tmp_dir()
    try:
        if check_session():
            sess = None
            with open("{}/session.pkl".format(temp), "rb") as f:
                sess = dill.load(f)
            return sess
        else:
            regenerate_sess()
            return load_dumped_session()
    except Exception as e:
        utils.log_err("Loading Session Failed")
        utils.log_err("Please login first")
        utils.log_err(e)


def check_session():
    temp = utils.tmp_dir()
    return os.path.isfile("{}/session.pkl".format(temp))
