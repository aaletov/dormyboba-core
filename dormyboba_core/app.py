import logging
from pathlib import Path
import asyncio
from contextlib import asynccontextmanager
import importlib.resources
from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dependency_injector.wiring import Provide
from pydantic import BaseModel
from .container import Container
from .server import DormybobaServer
from .logger import setup_logging
from .repository import (
    DormybobaUserRepository,
    DormybobaRoleRepository,
)
from .entity import TokenConverter
from . import entity
from .api import InviteRegisterUserRequest

setup_logging()

dormyboba_server: DormybobaServer = Provide[Container.dormyboba_server]
token_converter: TokenConverter = Provide[Container.token_converter]
user_repository: DormybobaUserRepository = Provide[Container.user_repository]
role_repository: DormybobaRoleRepository = Provide[Container.role_repository]

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(dormyboba_server.run())
    yield

def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[__name__])
    app = FastAPI(lifespan=lifespan)
    return app

app = create_app()

path = Path(importlib.resources.files(__package__)).resolve()

app.mount("/static", StaticFiles(directory=(path / "static")), name="static")
templates = Jinja2Templates(directory=(path / "templates"))

@app.get("/")
async def read_root():
    return {"Dormyboba": "Core"}

@app.get("/invite/widget", response_class=HTMLResponse)
async def invite_widget(request: Request, token: str):
    logger = logging.getLogger("dormyboba")
    logger.info(token)
    return templates.TemplateResponse(
        request=request, name="widget.html",
    )

@app.post("/invite/registerUser", status_code=status.HTTP_201_CREATED)
async def invite_register_user(req: InviteRegisterUserRequest):
    logger = logging.getLogger("dormyboba")
    token = token_converter.decode(req.token)
    role = role_repository.getByName(token.role)
    user_repository.add(entity.DormybobaUser(
        user_id=req.userId,
        role=role,
        institute=None,
        academic_type=None,
        year=None,
        group=None,
        is_registered=False,
    ))
    logger.info(req)
    return

class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"

@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    """
    ## Perform a Health Check
    Endpoint to perform a healthcheck on. This endpoint can primarily be used Docker
    to ensure a robust container orchestration and management is in place. Other
    services which rely on proper functioning of the API service will not deploy if this
    endpoint returns any other HTTP status code except 200 (OK).
    Returns:
        HealthCheck: Returns a JSON response with the health status
    """
    return HealthCheck(status="OK")
