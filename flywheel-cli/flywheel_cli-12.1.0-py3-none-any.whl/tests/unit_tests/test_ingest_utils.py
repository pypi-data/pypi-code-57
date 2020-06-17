import datetime
from unittest import mock

import pytest
import pytz

import flywheel
from flywheel_cli.ingest import errors
from flywheel_cli.ingest import schemas as T
from flywheel_cli.ingest import utils


def test_encode_json_set():
    in_val = {"apple", "banana", "cherry"}

    ret_val = utils.encode_json(in_val)

    assert set(ret_val) == in_val


def test_encode_json_date():
    in_val = datetime.date(2019, 2, 15)
    ret_val = utils.encode_json(in_val)

    assert isinstance(ret_val, str)
    assert ret_val == '2019-02-15'


def test_encode_json_datetime_wo_tzinfo():
    in_val = datetime.datetime(2019, 2, 15, 10, 11, 12)

    ret_val = utils.encode_json(in_val)

    assert isinstance(ret_val, str)
    assert ret_val == '2019-02-15T10:11:12+00:00'


def test_encode_json_datetime_w_tzinfo():
    in_val = pytz.timezone('Europe/Amsterdam').localize(datetime.datetime(2019, 2, 15, 10, 11, 12))

    ret_val = utils.encode_json(in_val)

    assert isinstance(ret_val, str)
    assert ret_val == '2019-02-15T09:11:12+00:00'


def test_json_serializer():
    in_val = {
        "a": {'a': 'b'},
        "b": datetime.date(2019, 2, 15),
        "c": datetime.datetime(2019, 2, 15, 10, 11, 12),
        "d": 1
    }

    ret_val = utils.json_serializer(in_val)
    assert ret_val == '{"a":{"a":"b"},"b":"2019-02-15","c":"2019-02-15T10:11:12+00:00","d":1}'


def test_get_path_el_group():
    ret_val = utils.get_path_el(
        c_type='group',
        context={'_id': 'id', 'label': 'label'}
    )
    assert ret_val == 'id'

    ret_val = utils.get_path_el(
        c_type='group',
        context={'_id': 'id', 'label': 'label'},
        use_labels=True
    )
    assert ret_val == 'id'

def test_get_path_el_full_context():
    ret_val = utils.get_path_el(
        c_type='none',
        context={'_id': 'id', 'label': 'label'}
    )
    assert ret_val == '<id:id>'

    ret_val = utils.get_path_el(
        c_type='none',
        context={'_id': 'id', 'label': 'label'},
        use_labels=True
    )
    assert ret_val == 'label'


def test_get_path_el_partial_context():
    ret_val = utils.get_path_el(
        c_type='none',
        context={'_id': None, 'label': 'label'}
    )
    assert ret_val == 'label'

    ret_val = utils.get_path_el(
        c_type='none',
        context={'label': 'label'}
    )
    assert ret_val == 'label'


def test_get_path_el_no_info_raises():
    with pytest.raises(TypeError):
        utils.get_path_el(
            c_type='none',
            context={'no': 'key'}
        )

    with pytest.raises(TypeError):
        utils.get_path_el(
            c_type='none',
            context={'no': 'key'},
            use_labels=True
        )

    with pytest.raises(TypeError):
        utils.get_path_el(
            c_type='none',
            context={'_id': 'id'},
            use_labels=True
        )

    with pytest.raises(TypeError):
        utils.get_path_el(
            c_type='none',
            context={'_id': 'id', 'label': None},
            use_labels=True
        )


def test_get_api_key_logged_out_raises(mocker):
    mocker.patch('flywheel_cli.sdk_impl.load_config', return_value={})

    with pytest.raises(SystemExit):
        utils.get_api_key()


def test_get_api_key_logged_in_returns_key(mocker):
    mocker.patch('flywheel_cli.sdk_impl.load_config',
                 return_value={'key': 'apikey'})
    key = utils.get_api_key()
    assert key == 'apikey'


def test_auth_exception():
    ex = errors.AuthenticationError("message")
    assert isinstance(ex, errors.AuthenticationError)
    assert ex.code == 403

    ex = errors.AuthenticationError("message", 500)
    assert isinstance(ex, errors.AuthenticationError)
    assert ex.code == 500


def test_sdk_client_init(mocker):
    flywheel_mock = mocker.patch('flywheel_cli.ingest.utils.flywheel.Client')

    sdk = utils.SDKClient('api:key')

    flywheel_mock.assert_called_once_with(
        'api:key'
    )
    assert isinstance(sdk, utils.SDKClient)


def test_sdk_client_call_api_no_kwargs(mocker):
    flywheel_mock = mocker.patch('flywheel_cli.ingest.utils.flywheel.Client')

    sdk = utils.SDKClient('api:key')

    sdk.call_api("/path", 'GET')
    flywheel_mock.return_value.api_client.call_api.assert_called_once_with(
        '/path',
        'GET',
        _preload_content=True,
        _return_http_data_only=True,
        auth_settings=['ApiKey']
    )


def test_sdk_client_call_api_with_kwargs(mocker):
    flywheel_mock = mocker.patch('flywheel_cli.ingest.utils.flywheel.Client')

    sdk = utils.SDKClient('api:key')

    sdk.call_api(
        "/path",
        'GET',
        _preload_content=False,
        auth_settings=['Custom'],
        not_default="value"
    )
    flywheel_mock.return_value.api_client.call_api.assert_called_once_with(
        '/path',
        'GET',
        _preload_content=False,
        _return_http_data_only=True,
        auth_settings=['Custom'],
        not_default='value'
    )


def test_sdk_client_create_upload_ticket(mocker):
    flywheel_mock = mocker.patch('flywheel_cli.ingest.utils.flywheel.Client')
    flywheel_mock.return_value.api_client.call_api.return_value = {'ticket': 'ticketid', 'urls':{'filename': 'fileurl'}}

    sdk = utils.SDKClient('api:key')

    response = sdk.create_upload_ticket("/url", 'filename')
    assert response == ('ticketid', 'fileurl')

    flywheel_mock.return_value.api_client.call_api.assert_called_once_with(
        '/url',
        'POST',
        _preload_content=True,
        _return_http_data_only=True,
        auth_settings=['ApiKey'],
        body={'metadata': {}, 'filenames': ['filename']},
        query_params=[('ticket', '')],
        response_type=object
    )

    flywheel_mock.reset_mock()

    response = sdk.create_upload_ticket("/url", 'filename', {'meta': 'data'})
    assert response == ('ticketid', 'fileurl')

    flywheel_mock.return_value.api_client.call_api.assert_called_once_with(
        '/url',
        'POST',
        _preload_content=True,
        _return_http_data_only=True,
        auth_settings=['ApiKey'],
        body={'metadata': {'meta': 'data'}, 'filenames': ['filename']},
        query_params=[('ticket', '')],
        response_type=object
    )


def test_sdk_client_signed_url_upload(mocker):
    flywheel_mock = mocker.patch('flywheel_cli.ingest.utils.flywheel.Client')
    flywheel_mock.return_value.api_client.call_api.return_value = {'ticket': 'ticketid', 'urls':{'filename': 'fileurl'}}
    file = mock.Mock()

    sdk = utils.SDKClient('api:key')

    sdk.signed_url_upload(
        "cont_name",
        "cont_id",
        "filename",
        file,
        {'meta': 'meta'}
    )

    flywheel_mock.return_value.api_client.call_api.assert_has_calls([
        mock.call(
            '/cont_names/cont_id/files',
            'POST',
            _preload_content=True,
            _return_http_data_only=True,
            auth_settings=['ApiKey'],
            body={'metadata': {'meta': 'meta'}, 'filenames': ['filename']},
            query_params=[('ticket', '')],
            response_type=object
        ),
        mock.call(
            '/cont_names/cont_id/files',
            'POST',
            _preload_content=True,
            _return_http_data_only=True,
            auth_settings=['ApiKey'],
            query_params=[('ticket', 'ticketid')]
        )
    ])


def test_sdk_client_upload_not_signed(mocker):
    flywheel_mock = mocker.patch('flywheel_cli.ingest.utils.flywheel.Client')
    mocker.patch('os.fstat', return_value=AttributeDict({'st_size': 10}))
    uploader = mock.Mock()
    filespec = mock.Mock()
    flywheel_mock.return_value.upload_file_to_cont_name = uploader
    filespec_mock = mocker.patch('flywheel.FileSpec', return_value=filespec)
    file_mock = mock.MagicMock()

    sdk = utils.SDKClient('api:key')
    sdk.signed_url = False

    sdk.upload(
        "cont_name",
        "cont_id",
        "filename",
        file_mock,
        {'meta': 'meta'}
    )

    filespec_mock.assert_called_once_with(
        'filename',
        file_mock,
    )

    uploader.assert_called_once_with(
        'cont_id',
        filespec,
        metadata='{"meta":"meta"}'
    )


def test_lru_cache_max_length():
    cache = utils.LRUCache(max_length=2)

    cache['key1'] = 'value1'
    cache['key2'] = 'value2'

    assert cache['key1'] == 'value1'
    assert cache['key2'] == 'value2'
    assert len(cache.cache) == 2

    cache['key3'] = 'value3'
    assert len(cache.cache) == 2

    with pytest.raises(KeyError):
        cache['key1']
    assert cache['key2'] == 'value2'
    assert cache['key3'] == 'value3'


def test_lru_cache_default_value():
    cache = utils.LRUCache(max_length=2)
    cache['key1'] = 'value1'

    assert cache.get('key1') == 'value1'
    assert cache.get('key1', 'default') == 'value1'
    assert cache.get('key2', 'default') == 'default'

    with pytest.raises(KeyError):
        cache['key2']


def test_get_fw_auth_invalid_api_key_format_raise():
    with pytest.raises(Exception):
        utils.get_fw_auth('apikey')


def test_get_fw_auth_invalid_api_key_raise(mocker):
    flywheel_mock = mocker.patch('flywheel_cli.ingest.utils.flywheel.Client')
    flywheel_mock.return_value.get_auth_status.side_effect = flywheel.ApiException()

    with pytest.raises(errors.AuthenticationError) as execinfo:
        utils.get_fw_auth('api:key')

    assert execinfo.value.args[0] == "Invalid API key"
    assert execinfo.value.code == 403


def test_get_fw_auth_not_admin_raise(mocker):
    flywheel_mock = mocker.patch('flywheel_cli.ingest.utils.flywheel.Client')
    flywheel_mock.return_value.get_auth_status.return_value = AuthStatus(is_admin=False)
    flywheel_mock.reset_mock()

    with pytest.raises(errors.AuthenticationError) as execinfo:
        utils.get_fw_auth('api:key1')

    assert execinfo.value.args[0] == "Admin access required"
    assert execinfo.value.code == 403


def test_get_fw_auth_without_client(mocker):
    flywheel_mock = mocker.patch('flywheel_cli.ingest.utils.flywheel.Client')
    flywheel_mock.return_value.get_auth_status.return_value = AuthStatus(is_admin=True)
    flywheel_mock.reset_mock()
    # new apikey is needed because of LRU cache
    fw_auth = utils.get_fw_auth('api:key2')

    flywheel_mock.assert_called_once_with(
        'api:key2'
    )

    assert isinstance(fw_auth, T.FWAuth)
    assert fw_auth.api_key == 'api:key2'
    assert fw_auth.host == 'api'
    assert fw_auth.user == '1234'
    assert fw_auth.is_admin


def test_get_fw_auth_with_client_different_key_raise(mocker):
    api_key = 'api:key'
    flywheel_mock = mocker.patch('flywheel_cli.ingest.utils.flywheel.Client')
    flywheel_mock.return_value.get_auth_status.return_value = AuthStatus(is_admin=True)
    flywheel_mock.return_value.api_client.configuration = flywheel.flywheel.config_from_api_key(api_key)

    fw = flywheel.Client(api_key)
    flywheel_mock.reset_mock()

    with pytest.raises(AssertionError):
        utils.get_fw_auth('api:key4', fw)


def test_get_fw_auth_with_client_raise(mocker):
    api_key = 'api:key4'
    flywheel_mock = mocker.patch('flywheel_cli.ingest.utils.flywheel.Client')
    flywheel_mock.return_value.get_auth_status.return_value = AuthStatus(is_admin=False)
    flywheel_mock.return_value.api_client.configuration = flywheel.flywheel.config_from_api_key(api_key)
    fw = flywheel.Client(api_key)
    flywheel_mock.reset_mock()

    with pytest.raises(errors.AuthenticationError):
        utils.get_fw_auth(api_key, fw)

    flywheel_mock.assert_not_called()


def test_get_fw_auth_with_client_same_key(mocker):
    api_key = 'api:key5'
    flywheel_mock = mocker.patch('flywheel_cli.ingest.utils.flywheel.Client')
    flywheel_mock.return_value.get_auth_status.return_value = AuthStatus(is_admin=True)
    flywheel_mock.return_value.api_client.configuration = flywheel.flywheel.config_from_api_key(api_key)
    fw = flywheel.Client(api_key)
    flywheel_mock.reset_mock()

    fw_auth = utils.get_fw_auth(api_key, fw)

    flywheel_mock.assert_not_called()
    assert isinstance(fw_auth, T.FWAuth)
    assert fw_auth.api_key == 'api:key5'
    assert fw_auth.host == 'api'
    assert fw_auth.user == '1234'
    assert fw_auth.is_admin



class AuthStatus():
    def __init__(self, is_admin):
        self.is_admin = is_admin

    @property
    def user_is_admin(self):
        return self.is_admin

    @property
    def origin(self):
        return AttributeDict({'id': '1234'})


class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
