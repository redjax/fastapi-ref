import sys

import stackprinter

stackprinter.set_excepthook(style="darkbg2")

from pathlib import Path

from loguru import logger as log
from pydantic import BaseModel
from config import settings, api_settings
from red_utils.loguru_utils import init_logger
import uvicorn

ENV = settings.env

if __name__ == "__main__":
    ## If this file was run directly, initialize logger.
    init_logger()

log.debug(
    f"[{ENV}] API settings reload ({type(api_settings.api_reload)}): {api_settings.api_reload}"
)


class UvicornCustomServer(BaseModel):
    """Customize a Uvicorn server by passing a dict
    to UvicornCustomServer.parse_obj(dict).

    Run server with instance's .run_server(). This function
    builds a Uvicorn server with the config on the instance,
    then runs it.
    """

    app: str = "main:app"
    host: str = "0.0.0.0"
    port: int = 8000
    root_path: str = "/"
    reload: bool = False

    def run_server(self) -> None:
        uvicorn.run(
            app=self.app,
            host=self.host,
            port=self.port,
            reload=self.reload,
            root_path=self.root_path,
        )


app = "api:app"
host = api_settings.api_host or "0.0.0.0"
port = api_settings.api_port or 8000
_reload = api_settings.api_reload or False
root_path = "/api/v1"
debug = api_settings.api_debug or False

log.debug(f"API settings port: {api_settings.api_port}")
uvi_dev_conf: dict = {
    "host": host,
    "port": port,
    "reload": _reload,
}

# dev_server = UvicornCustomServer.parse_obj(_uvi_dev_conf)
dev_server = UvicornCustomServer.model_validate(uvi_dev_conf)
prod_server = UvicornCustomServer()


if __name__ == "__main__":
    log.debug(f"API settings: {api_settings._wrapped}")
    match ENV:
        case "dev":
            server = dev_server
        case "prod":
            server = prod_server
        case _:
            server = prod_server

    log.info(f"Starting [{ENV}] Uvicorn server")
    log.debug(f"Uvicorn config: {server}")

    log.debug(f"Serving app {server.app} on port {server.port}")
    server.run_server()
