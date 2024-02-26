"""Dormyboba-core.

Usage:
    dormyboba_core (-h | --help)
    dormyboba_core --config-dir=<cd>

Options:
    -h --help            Show this screen.
    --config-dir=<cd>    Config dir/

"""
from docopt import docopt
import warnings
import logging
from pathlib import Path
import asyncio
from sqlalchemy import create_engine
import gspread
import uvicorn
from contextlib import asynccontextmanager
import importlib.resources
from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .config import parse_config, DormybobaConfig
from .logger import setup_logging
from .repository import (
    SqlAlchemyDormybobaUserRepository,
    SqlAlchemyDormybobaRoleRepository,
    SqlAlchemyInstituteRepository,
    SqlAlchemyAcademicTypeRepository,
    GsheetDefectRepository,
    SqlAlchemyMailingRepository,
    SqlAlchemyQueueRepository,
)
from . import entity
from .entity import Token, TokenConverter
from .service import DormybobaCoreServicer
from .server import DormybobaServer
from .api import InviteRegisterUserRequest

warnings.filterwarnings("ignore", category=SyntaxWarning)

setup_logging()

ARGUMENTS = docopt(__doc__, version='DormybobaCore')
CONFIG_PATH = Path(ARGUMENTS["--config-dir"]).resolve()
CONFIG = parse_config(CONFIG_PATH / "config.yaml")

ENGINE = create_engine(CONFIG.pg_config.db_url)

def get_worksheet(config: DormybobaConfig) -> None:
    gc = gspread.service_account(filename=(CONFIG_PATH / "service_account.json"))
    defect_sheet = gc.open_by_key(config.gsheet_config.defect_sheet_id)
    return defect_sheet.get_worksheet(0)

WORKSHEET = get_worksheet(CONFIG)

user_repository = SqlAlchemyDormybobaUserRepository(ENGINE)
role_repository = SqlAlchemyDormybobaRoleRepository(ENGINE)
institute_repository = SqlAlchemyInstituteRepository(ENGINE)
academic_type_repository = SqlAlchemyAcademicTypeRepository(ENGINE)
mailing_repository = SqlAlchemyMailingRepository(ENGINE)
queue_repository = SqlAlchemyQueueRepository(ENGINE)
sheet_repository = GsheetDefectRepository(WORKSHEET)

token_converter = TokenConverter(CONFIG.private_key)

dormyboba_servicer = DormybobaCoreServicer(
    user_repository=user_repository,
    role_repository=role_repository,
    institute_repository=institute_repository,
    academic_type_repository=academic_type_repository,
    mailing_repository=mailing_repository,
    queue_repository=queue_repository,
    sheet_repository=sheet_repository,
    token_converter=token_converter,
)

dormyboba_server = DormybobaServer(dormyboba_servicer)

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(dormyboba_server.run())
    yield

app = FastAPI(lifespan=lifespan)

path = Path(importlib.resources.files(__package__)).resolve()

app.mount("/static", StaticFiles(directory=(path / "static")), name="static")
templates = Jinja2Templates(directory=(path / "templates"))

@app.get("/")
async def read_root():
    return {"Dormyboba": "Core"}

logger = logging.getLogger("dormyboba")

@app.get("/invite/widget", response_class=HTMLResponse)
async def invite_widget(request: Request, token: str):
    logger.info(token)
    return templates.TemplateResponse(
        request=request, name="widget.html",
    )

@app.post("/invite/registerUser", status_code=status.HTTP_201_CREATED)
async def invite_register_user(req: InviteRegisterUserRequest):
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

if __name__ == "__main__":
    uvicorn.run("dormyboba_core.__main__:app", host="0.0.0.0", port=8000, workers=2)
