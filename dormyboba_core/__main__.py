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
import yaml
from pathlib import Path
import asyncio
from sqlalchemy import create_engine
import gspread
from .config import parse_config
from .server import serve

warnings.filterwarnings("ignore", category=SyntaxWarning)

if __name__ == "__main__":
    arguments = docopt(__doc__, version='Naval Fate 2.0')
    config_dir = arguments["--config-dir"]
    config_path = Path(config_dir).resolve()

    logging.basicConfig(level=logging.DEBUG)
    logging.info("Creating engine...")

    config = parse_config(config_path / "config.yaml")
    engine = create_engine(config.pg_config.db_url)

    gc = gspread.service_account(filename=(config_path / "service_account.json"))
    defect_sheet = gc.open_by_key(config.gsheet_config.defect_sheet_id)
    worksheet = defect_sheet.get_worksheet(0)

    asyncio.run(serve(engine, worksheet))
