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
from pathlib import Path
import asyncio
from sqlalchemy import create_engine
import gspread
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .config import parse_config, DormybobaConfig
from .server import serve
from .logger import setup_logging

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

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(serve(ENGINE, WORKSHEET))
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
