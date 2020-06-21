import logging

log = logging.getLogger(__name__)


def patch_all():
    try:
        import athena.patch.pandas as patch_pandas

        patch_pandas.patch()
    except Exception:
        log.warning("Couldn't patch module pandas")

    try:
        import athena.patch.sklearn as patch_sklearn

        patch_sklearn.patch()
    except Exception:
        log.warning("Couldn't patch module sklearn")

    try:
        import athena.patch.subprocess as patch_subprocess

        patch_subprocess.patch()
    except Exception:
        log.warning("Couldn't patch module subprocess")
