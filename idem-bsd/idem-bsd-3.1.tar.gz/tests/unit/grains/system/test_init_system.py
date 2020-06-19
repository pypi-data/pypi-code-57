import io
import pytest
import mock


@pytest.mark.asyncio
async def test_load_init_rc(mock_hub, hub):
    with mock.patch("shutil.which", return_value=True):
        mock_hub.grains.system.init_system.load_init = (
            hub.grains.system.init_system.load_init
        )
        await mock_hub.grains.system.init_system.load_init()

    assert mock_hub.grains.GRAINS.init == "rc"


@pytest.mark.asyncio
async def test_load_init_systemd(mock_hub, hub):
    with mock.patch("shutil.which", return_value=False):
        with mock.patch("os.path.exists", return_value=True):
            with mock.patch("os.stat", return_value=True):
                mock_hub.grains.system.init_system.load_init = (
                    hub.grains.system.init_system.load_init
                )
                await mock_hub.grains.system.init_system.load_init()
    assert mock_hub.grains.GRAINS.init == "systemd"


@pytest.mark.asyncio
async def test_load_init_upstart(mock_hub, hub):
    with mock.patch("shutil.which", side_effect=[False, "/bin/init"]):
        with mock.patch("os.path.exists", side_effect=[False, True]):
            with mock.patch(
                "aiofiles.threadpool.sync_open",
                side_effect=[
                    io.StringIO("1\x00"),
                    io.StringIO("this is an upstart\x00init"),
                ],
            ):
                mock_hub.grains.system.init_system.load_init = (
                    hub.grains.system.init_system.load_init
                )
                await mock_hub.grains.system.init_system.load_init()
    assert mock_hub.grains.GRAINS.init == "upstart"


@pytest.mark.asyncio
async def test_load_init_sysvinit(mock_hub, hub):
    with mock.patch("shutil.which", side_effect=[False, "/bin/init"]):
        with mock.patch("os.path.exists", side_effect=[False, True]):
            with mock.patch(
                "aiofiles.threadpool.sync_open",
                side_effect=[
                    io.StringIO("1\x00"),
                    io.StringIO("this is an sysvinit\x00init"),
                ],
            ):
                mock_hub.grains.system.init_system.load_init = (
                    hub.grains.system.init_system.load_init
                )
                await mock_hub.grains.system.init_system.load_init()
    assert mock_hub.grains.GRAINS.init == "sysvinit"


@pytest.mark.asyncio
async def test_load_init_systemdb(mock_hub, hub):
    with mock.patch("shutil.which", side_effect=[False, "/bin/init"]):
        with mock.patch("os.path.exists", side_effect=[False, True]):
            with mock.patch(
                "aiofiles.threadpool.sync_open",
                side_effect=[
                    io.StringIO("1\x00"),
                    io.StringIO("this is an systemd\x00init"),
                ],
            ):
                mock_hub.grains.system.init_system.load_init = (
                    hub.grains.system.init_system.load_init
                )
                await mock_hub.grains.system.init_system.load_init()
    assert mock_hub.grains.GRAINS.init == "systemd"


@pytest.mark.asyncio
async def test_load_init_supervisord(mock_hub, hub):
    with mock.patch("os.path.exists", side_effect=[False, True]):
        with mock.patch(
            "aiofiles.threadpool.sync_open",
            return_value=io.StringIO("init /test/bin/supervisord\x00"),
        ):
            with mock.patch(
                "shutil.which", side_effect=[False, "", "/test/bin/supervisord"]
            ):
                mock_hub.grains.system.init_system.load_init = (
                    hub.grains.system.init_system.load_init
                )
                await mock_hub.grains.system.init_system.load_init()
    assert mock_hub.grains.GRAINS.init == "supervisord"


@pytest.mark.asyncio
async def test_load_init_dumb_init(mock_hub, hub):
    with mock.patch("os.path.exists", side_effect=[False, True]):
        with mock.patch(
            "aiofiles.threadpool.sync_open",
            return_value=io.StringIO("init /test/bin/dumb-init\x00"),
        ):
            with mock.patch(
                "shutil.which", side_effect=[False, "", "", "/test/bin/dumb-init"]
            ):
                mock_hub.grains.system.init_system.load_init = (
                    hub.grains.system.init_system.load_init
                )
                await mock_hub.grains.system.init_system.load_init()
    assert mock_hub.grains.GRAINS.init == "dumb-init"


@pytest.mark.asyncio
async def test_load_init_tini(mock_hub, hub):
    with mock.patch("os.path.exists", side_effect=[False, True]):
        with mock.patch(
            "aiofiles.threadpool.sync_open",
            return_value=io.StringIO("init /test/bin/tini\x00"),
        ):
            with mock.patch(
                "shutil.which", side_effect=[False, "", "", "", "/test/bin/tini"]
            ):
                mock_hub.grains.system.init_system.load_init = (
                    hub.grains.system.init_system.load_init
                )
                await mock_hub.grains.system.init_system.load_init()
    assert mock_hub.grains.GRAINS.init == "tini"


@pytest.mark.asyncio
async def test_load_init_runit(mock_hub, hub):
    with mock.patch("os.path.exists", side_effect=[False, True]):
        with mock.patch(
            "aiofiles.threadpool.sync_open",
            return_value=io.StringIO("init /test/bin/init\x00runit"),
        ):
            with mock.patch("shutil.which", side_effect=[False, "", "", "", ""]):
                mock_hub.grains.system.init_system.load_init = (
                    hub.grains.system.init_system.load_init
                )
                await mock_hub.grains.system.init_system.load_init()
    assert mock_hub.grains.GRAINS.init == "runit"


@pytest.mark.asyncio
async def test_load_init_my_init(mock_hub, hub):
    with mock.patch("os.path.exists", side_effect=[False, True]):
        with mock.patch(
            "aiofiles.threadpool.sync_open",
            return_value=io.StringIO("init /sbin/my_init\x00"),
        ):
            with mock.patch("shutil.which", side_effect=[False, "", "", "", ""]):
                mock_hub.grains.system.init_system.load_init = (
                    hub.grains.system.init_system.load_init
                )
                await mock_hub.grains.system.init_system.load_init()
    assert mock_hub.grains.GRAINS.init == "runit"


@pytest.mark.asyncio
async def test_load_init(mock_hub, hub):
    with mock.patch("os.path.exists", side_effect=[False, True]):
        with mock.patch(
            "aiofiles.threadpool.sync_open",
            return_value=io.StringIO("init /test/bin/unknown\x00"),
        ):
            with mock.patch("shutil.which", side_effect=[False, "", "", "", "", ""]):
                mock_hub.grains.system.init_system.load_init = (
                    hub.grains.system.init_system.load_init
                )
                await mock_hub.grains.system.init_system.load_init()
    assert mock_hub.grains.GRAINS.init == "init"
