import logging
import yaml
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dormyboba_core.server import serve 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

config = None
with open(BASE_DIR / "config.yaml", "r") as yamlfile:
    config = yaml.load(yamlfile, Loader=yaml.FullLoader)["dormyboba"]

pg_config = config["postgres"]
PG_USER = pg_config["user"]
PG_PASSWORD = pg_config["password"]
PG_HOST = pg_config["host"]
PG_DB = pg_config["db"]
DB_URL = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DB}"

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Creating engine...")
    engine = create_engine(DB_URL)
    session = Session(engine)
    serve(session)
