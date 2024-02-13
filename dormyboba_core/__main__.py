import logging
import yaml
from pathlib import Path
import asyncio
from sqlalchemy import create_engine
import gspread
from .server import serve

CONFIG_DIR = Path("/").resolve() / "config"

config = None
with open(CONFIG_DIR / "config.yaml", "r") as yamlfile:
    config = yaml.load(yamlfile, Loader=yaml.FullLoader)["dormyboba"]

pg_config = config["postgres"]
PG_USER = pg_config["user"]
PG_PASSWORD = pg_config["password"]
PG_HOST = pg_config["host"]
PG_DB = pg_config["db"]
DB_URL = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DB}"

gc_config = config["gc"]
DEFECT_SHEET_ID = gc_config["defect_sheet_id"]

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Creating engine...")
    engine = create_engine(DB_URL)

    gc = gspread.service_account(filename=CONFIG_DIR / "service_account.json")
    defect_sheet = gc.open_by_key(DEFECT_SHEET_ID)
    worksheet = defect_sheet.get_worksheet(0)

    asyncio.run(serve(engine, worksheet))
