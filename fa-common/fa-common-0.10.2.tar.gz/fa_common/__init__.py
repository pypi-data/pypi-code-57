import functools
from typing import Awaitable, Callable, Type

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.cors import CORSMiddleware

from .config import DatabaseType, Settings, StorageType, get_settings
from .exception_handlers import setup_exception_handlers
from .exceptions import (
    BadRequestError,
    DatabaseError,
    ForbiddenError,
    HTTPException,
    NotFoundError,
    NotImplementedError,
    StorageError,
    UnauthorizedError,
    UnknownError,
)
from .models import CamelModel, FileDownloadRef
from .responses import UJSONResponse
from .utils import (
    async_get,
    force_async,
    force_sync,
    get_current_app,
    get_logger,
    get_now,
    get_remote_schema,
    get_timezone,
    logger,
    resolve_dotted_path,
    sizeof_fmt,
)

__author__ = "Samuel Bradley"
__email__ = "sam.bradley@csiro.au"
__version__ = "0.10.2"


def create_app(
    env_path: str = None,
    disable_gzip: bool = False,
    on_start: Callable[[FastAPI], Awaitable[None]] = None,
    on_stop: Callable[[FastAPI], Awaitable[None]] = None,
) -> FastAPI:
    settings = get_settings(env_path)

    if settings.SENTRY_DSN is not None:
        import sentry_sdk

        sentry_sdk.init(settings.SENTRY_DSN)

    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_PRE_PATH}/openapi.json",
    )

    # CORS
    origins = []
    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        origins_raw = settings.BACKEND_CORS_ORIGINS
        for origin in origins_raw:
            use_origin = origin.strip()
            origins.append(use_origin)
        logger.info(f"Allowing Origins {origins}")
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    setup_exception_handlers(app)

    # Adds support for GZIP response
    if not disable_gzip:
        app.add_middleware(GZipMiddleware, minimum_size=5000)

    if settings.SECURE:
        from secure import SecureHeaders, SecureCookie

        secure_headers = SecureHeaders()

        @app.middleware("http")
        async def set_secure_headers(request, call_next):
            response = await call_next(request)
            secure_headers.starlette(response)
            return response

    @app.on_event("startup")
    async def on_start_app() -> None:
        await start_app(app)
        if on_start is not None:
            await on_start(app)

    @app.on_event("shutdown")
    async def stop_app() -> None:
        logger.info("Stopping App")
        # await close_db_connection(app)
        if on_stop is not None:
            await on_stop(app)

    return app


async def start_app(app: FastAPI):
    from fa_common.storage import setup_storage
    from fa_common.db import setup_db, create_indexes

    if get_settings().USE_FIREBASE:
        import firebase_admin

        if not len(firebase_admin._apps):
            firebase_admin.initialize_app()

    setup_db(app)
    setup_storage(app)
    if get_settings().ENABLE_WORKFLOW:
        try:
            from fa_common.workflow import setup_gitlab

            setup_gitlab(app)
        except ValueError as err:
            logger.error(
                "Gitlab dependencies are missing, if you are planning to use workflows make sure the optional"
                + " dependencies are installed"
            )
            raise err  # App probably doesn't want to use gitlab

    await create_indexes()
