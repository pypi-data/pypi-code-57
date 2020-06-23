from pathlib import Path

from fastapi import FastAPI  # type: ignore
from fastapi.responses import FileResponse  # type: ignore

from pullframe.persist import PERSIST
from pullframe.types import Request

app = FastAPI()


@app.post("/")
async def root(request: Request) -> FileResponse:
    persist = PERSIST[request.demand.cache_format.value](
        Path(request.directory)
    )
    df = persist.supply(
        request.demand, include_start=request.demand.start is None
    )
    path = persist.dump_path(request)
    persist.dump(path, df)
    return FileResponse(str(path))
