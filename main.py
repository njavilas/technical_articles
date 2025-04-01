from typing import Any, Optional
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles

from etcd3 import client, Etcd3Client  # type: ignore
from etcd3.client import KVMetadata  # type: ignore
from etcd3.events import PutEvent, DeleteEvent # type: ignore
from etcd3.watch import WatchResponse # type: ignore
from starlette.templating import _TemplateResponse  # type: ignore

app: FastAPI = FastAPI()
etcd: Etcd3Client = client(host="localhost", port=2379)

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

def watch_callback_listener(event: WatchResponse) -> None:

    put_event = event.events[0] # type: ignore

    print(put_event.key.decode(), put_event.value.decode()) # type: ignore


etcd.add_watch_callback("config/database_url", watch_callback_listener) # type: ignore


@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request) -> _TemplateResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/key/{key}")
def api_get_key(key: str) -> dict[str, Any] | dict[str, str]:
    raw: tuple[Optional[bytes], Optional[KVMetadata]] = etcd.get(key)  # type: ignore

    if raw[0]:
        return {"key": key, "value": raw[0].decode("utf-8")}

    return {"error": "Key not found"}


@app.put("/api/key/{key}")
def api_put_key(key: str, value: str) -> dict[str, str]:
    etcd.put(key, value)  # type: ignore
    return {"message": f"Configuration {key} registered successfully"}


@app.delete("/api/key")
def api_delete_key(key: str) -> dict[str, str]:
    deleted = etcd.delete(key)  # type: ignore
    if deleted:
        return {"message": f"Key {key} deleted successfully"}
    return {"message": f"Key {key} not found"}


@app.get("/get-key", response_class=HTMLResponse)
def get_config(key: str) -> str:
    raw: tuple[Optional[bytes], Optional[KVMetadata]] = etcd.get(key)  # type: ignore

    if raw[0]:
        return f"<p>Clave '{key}': {raw[0].decode("utf-8")}</p>"

    return f"<p>Clave '{key}': not found</p>"


@app.get("/update-key", response_class=HTMLResponse)
def set_config(key: str, value: str) -> str:
    etcd.put(key, value)  # type: ignore
    return f"<p>Configuration {key} registered successfully with value {value}</p>"


@app.get("/delete-key", response_class=HTMLResponse)
def delete_config(key: str) -> str:
    deleted = etcd.delete(key)  # type: ignore
    if deleted:
        return f"<p>Key '{key}' deleted successfully</p>"
    return f"<p>Key '{key}' not found</p>"
