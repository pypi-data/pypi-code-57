import idem_linux.grains.system.init_system
import io
import pytest
import mock
from dict_tools import data

SYSTEMD_DATA = """
systemd 245 (245.4-2-manjaro)
+PAM +AUDIT -SELINUX -IMA -APPARMOR +SMACK -SYSVINIT +UTMP +LIBCRYPTSETUP +GCRYPT +GNUTLS +ACL +XZ +LZ4 +SECCOMP +BLKID +ELFUTILS +KMOD +IDN2 -IDN +PCRE2 default-hierarchy=hybrid
"""


@pytest.mark.asyncio
async def test_load_systemd(mock_hub):
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict(
        {"stdout": SYSTEMD_DATA, "retcode": 0}
    )
    with mock.patch("shutil.which", return_value=True):
        await idem_linux.grains.system.init_system.load_systemd(mock_hub)
    assert mock_hub.grains.GRAINS.systemd.version == "245"
    assert (
        mock_hub.grains.GRAINS.systemd.features
        == "+PAM +AUDIT -SELINUX -IMA -APPARMOR +SMACK "
        "-SYSVINIT +UTMP +LIBCRYPTSETUP +GCRYPT +GNUTLS "
        "+ACL +XZ +LZ4 +SECCOMP +BLKID +ELFUTILS +KMOD "
        "+IDN2 -IDN +PCRE2 default-hierarchy=hybrid"
    )


@pytest.mark.asyncio
async def test_load_init_systemd(mock_hub):
    with mock.patch("os.path.exists", side_effect=(False, True)) and mock.patch(
        "shutil.which", return_value=False
    ) and mock.patch("os.stat", return_value=True):
        await idem_linux.grains.system.init_system.load_init(mock_hub)
    assert mock_hub.grains.GRAINS.init == "systemd"


@pytest.mark.asyncio
async def test__load_cgroup(mock_hub):
    with mock.patch("os.path.exists", return_value=True) and mock.patch(
        "aiofiles.threadpool.sync_open", return_value=io.StringIO("12:/sytemd:docker"),
    ):
        assert "docker" == await idem_linux.grains.system.init_system._load_cgroup(
            mock_hub
        )


def test__load_systemd(mock_hub):
    with mock.patch("os.path.exists", return_value=True) and mock.patch(
        "os.stat", return_value=True
    ):
        assert "systemd" == idem_linux.grains.system.init_system._load_systemd(mock_hub)


@pytest.mark.asyncio
async def test__load_bin_upstart(mock_hub):
    mock_hub.OPT = mock_hub.pop.data.imap({"grains": {"file_buffer_size": 9999}})
    with mock.patch(
        "aiofiles.threadpool.sync_open",
        return_value=io.StringIO("this is an upstart\x00init"),
    ):
        assert "upstart" == await idem_linux.grains.system.init_system._load_bin(
            mock_hub, ""
        )


@pytest.mark.asyncio
async def test__load_bin_sysvinit(mock_hub):
    mock_hub.OPT = mock_hub.pop.data.imap({"grains": {"file_buffer_size": 9999}})
    with mock.patch(
        "aiofiles.threadpool.sync_open",
        return_value=io.StringIO("this is an sysvinit\x00init"),
    ):
        assert "sysvinit" == await idem_linux.grains.system.init_system._load_bin(
            mock_hub, ""
        )


@pytest.mark.asyncio
async def test__load_bin_systemd(mock_hub):
    mock_hub.OPT = mock_hub.pop.data.imap({"grains": {"file_buffer_size": 9999}})
    with mock.patch(
        "aiofiles.threadpool.sync_open",
        return_value=io.StringIO("this is an systemd\x00init"),
    ):
        assert "systemd" == await idem_linux.grains.system.init_system._load_bin(
            mock_hub, ""
        )


@pytest.mark.asyncio
async def test__load_cmdline_runit(mock_hub):
    with mock.patch("os.path.exists", return_value=False) and mock.patch(
        "shutil.which", return_value="runit"
    ) and mock.patch(
        "aiofiles.threadpool.sync_open",
        return_value=io.StringIO("init /test/bin/init\x00runit"),
    ):
        assert "runit" == await idem_linux.grains.system.init_system._load_cmdline(
            mock_hub
        )


@pytest.mark.asyncio
async def test__load_cmdline_my_init(mock_hub):
    with mock.patch("os.path.exists", return_value=False) and mock.patch(
        "shutil.which", return_value=""
    ) and mock.patch(
        "aiofiles.threadpool.sync_open",
        return_value=io.StringIO("init /test/sbin/my_init\x00runit"),
    ):
        assert "runit" == await idem_linux.grains.system.init_system._load_cmdline(
            mock_hub
        )
