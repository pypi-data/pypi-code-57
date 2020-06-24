import pytest

from tktl.commands.deployments import (
    GetDeployment,
    GetDeploymentEcr,
    GetDeploymentId,
    PatchDeploymentStatus,
)
from tktl.core.exceptions.exceptions import APIClientException


def test_get_deployment_commands(capsys):
    cmd = GetDeployment()
    with pytest.raises(APIClientException) as e:
        cmd.execute("fake", "branch", "name")

    cmd = GetDeploymentEcr()
    with pytest.raises(APIClientException) as e:
        cmd.execute("fake", "branch", "name")

    cmd = GetDeploymentId()
    with pytest.raises(APIClientException) as e:
        cmd.execute("fake", "branch", "name")

    cmd = PatchDeploymentStatus()
    with pytest.raises(APIClientException) as e:
        cmd.execute("fake", "status")

    # print(response)
    # repr(response)
    # print(response.dict())
    # assert response.status_code == 423

    #
    # out, err = capsys.readouterr()
    # assert 'API Key cannot be empty.\n' == err
    #
    # cmd.execute(api_key='ABC')
    # assert os.path.exists(os.path.expanduser('~/.tktl/config.json'))
    # with open(os.path.expanduser('~/.tktl/config.json'), 'r') as j:
    #     d = json.load(j)
    #     assert d['api-key'] == 'ABC'

# def test_login(capsys, user_password_key):
#     cmd = LogInCommand()
#     with pytest.raises(InvalidInputError):
#         cmd.execute(None, None, None)
#
#     with pytest.raises(InvalidInputError):
#         cmd.execute(None, 'me', None)
#
#     u, p, k = user_password_key
#
#     assert cmd.execute(u, p, None) is True
#     out, err = capsys.readouterr()
#     assert out == 'Login successful!\n'
#     assert cmd.execute(None, None, k) is True
#     out, err = capsys.readouterr()
#     assert out == 'Login successful!\n'
#
#     assert cmd.execute(u, 'whatever', None) is False
#     out, err = capsys.readouterr()
#     assert err == 'Request failed: Incorrect username or password\n'
#
