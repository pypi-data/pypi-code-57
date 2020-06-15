import json
from urllib.parse import urlsplit, parse_qs
import pytest
import furl
import httpretty

from urllib.parse import urlencode
from dli.client.listener import _Listener
from tests.test_session import UnitTestEnv


@pytest.fixture
def mock_listener_client():
    _Listener.run(debug=True, port=9999)

    with _Listener.app.test_client() as client:
        yield client

@httpretty.activate
def auth(mock_listener_client, state, sam_status='200', cat_status='200',
         headers=True, cookies=True):
    postbox = '1'

    sam_response = json.dumps({'id_token': 'ID', 'access_token': 'ACCESS'})
    httpretty.register_uri(
        httpretty.POST,
        'http://sam.local/sso/oauth2/realms/root/realms/Customers/access_token',
        status=sam_status,
        body=sam_response
    )

    cat_response = json.dumps({'access_token': 'JWT'})
    httpretty.register_uri(
        httpretty.POST,
        'http://catalogue.local/api/identity/v2/auth/token',
        status=cat_status,
        body=cat_response,
    )

    target_builder = furl.furl("/")

    if headers:
        target_builder.args = {
            'code': 'CODE',
            'state' : state,
            'client_id': 'CLIENT_ID'
        }

    session = mock_listener_client.session_transaction()
    with session as s:
        if cookies:
            s['postbox'] = '1'

        t = UnitTestEnv()
        s["sam_client"] = t.sam_client
        s["catalogue"] = t.catalogue
        s["code_verifier"] = "test"
        s["sam"] = t.sam

    b = mock_listener_client.get(target_builder.url)
    return b


def test_listener_is_up(mock_listener_client):
    a = mock_listener_client.application.url_map
    rules = ['/shutdown', '/login']
    assert(all(k in [x.rule for x in a.iter_rules()] for k in rules))


@httpretty.activate
def test_login(mock_listener_client):
    response_text = 'Login'
    httpretty.register_uri(
        httpretty.HEAD, 'http://catalogue.local/login',
        status=302,
        body=response_text,
        adding_headers={"Location": "https://sam.local"}
    )
    postbox = 1
    a = mock_listener_client.get(
        f"/login?postbox={postbox}&{urlencode(UnitTestEnv().__dict__)}"
    )
    parts = urlsplit(a.headers["Location"])
    assert(parts.netloc == "sam.local")

    params = parse_qs(parts.query)
    keys = ['state', 'client_id', 'response_type','redirect_uri',
     'scope','code_challenge','code_challenge_method']
    assert(all(k in params.keys() for k in keys))
    assert(params["state"][0] == str(postbox))
    assert(params["redirect_uri"][0].startswith("http://localhost"))


def test_miss_postbox_login(mock_listener_client):
    b = mock_listener_client.get("/login")
    assert(b.status_code == 403)


def test_miss_env_login(mock_listener_client):
    b = mock_listener_client.get("/login?postbox=1")
    assert(b.status_code == 500)

@httpretty.activate
def test_miss_cookie_authenticate(mock_listener_client):
    # todo this module's fixture use requires precedence
    # cookie is a side effect on mock_listener_client
    b = auth(mock_listener_client, 1, cookies=False)
    print(b.data)
    assert(b.status_code == 500)
    assert("internal error" in str(b.data.decode("utf-8")))

@httpretty.activate
def test_authenticate(mock_listener_client):
    b = auth(mock_listener_client, 1)
    assert(b.status_code == 200)
    assert("now logged in" in str(b.data.decode("utf-8")))

@httpretty.activate
def test_authenticate_get(mock_listener_client):
    b = auth(mock_listener_client, 1)
    assert(b.status_code == 200)
    assert("now logged in" in str(b.data.decode("utf-8")))
    assert(json.loads(mock_listener_client.get("/get/1").data)["jwt"] == 'JWT')

@httpretty.activate
def test_miss_headers_authenticate(mock_listener_client):
    b = auth(mock_listener_client, 1, headers=False)
    assert(b.status_code == 403)

@httpretty.activate
def test_mitm_authenticate(mock_listener_client):
    b = auth(mock_listener_client, 2)
    assert(b.status_code==403)

@httpretty.activate
def test_bad_SAM_response_authenticate(mock_listener_client):
    b = auth(mock_listener_client, 1, sam_status='403')
    assert(b.status_code==403)

@httpretty.activate
def test_bad_Catalogue_response_authenticate(mock_listener_client):
    b = auth(mock_listener_client, 1, cat_status='403')
    assert (b.status_code == 403)

