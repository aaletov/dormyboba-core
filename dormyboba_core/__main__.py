import logging
import yaml
from pathlib import Path
import asyncio
from sqlalchemy import create_engine
import gspread
from .config import parse_config
from .server import serve

CONFIG_DIR = Path("/").resolve() / "config"

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Creating engine...")

    config = parse_config(CONFIG_DIR / "config.yaml")
    engine = create_engine(config.pg_config.db_url)

    gc = gspread.service_account(filename=CONFIG_DIR / "service_account.json")
    defect_sheet = gc.open_by_key(config.gsheet_config.defect_sheet_id)
    worksheet = defect_sheet.get_worksheet(0)

    asyncio.run(serve(engine, worksheet))
