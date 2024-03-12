import os
from pathlib import Path
from dependency_injector import containers, providers
from sqlalchemy import create_engine, Engine
import gspread
from gspread import Worksheet

from .repository import (
    SqlAlchemyDormybobaUserRepository,
    SqlAlchemyDormybobaRoleRepository,
    SqlAlchemyInstituteRepository,
    SqlAlchemyAcademicTypeRepository,
    GsheetDefectRepository,
    SqlAlchemyMailingRepository,
    SqlAlchemyQueueRepository,
)
from .entity import Token, TokenConverter
from .service import DormybobaCoreServicer
from .server import DormybobaServer

CONFIG_DIR = Path(os.getenv("CONFIG_DIR")).resolve()

def construct_engine(
    user: str,
    password: str,
    host: str,
    db: str,
) -> Engine:
    db_url=f"postgresql+psycopg2://{user}:{password}@{host}/{db}"
    return create_engine(db_url, connect_args={"connect_timeout": 30})

def construct_worksheet(
    config_dir: str,
    defect_sheet_id: str,
) -> Worksheet:
    gc = gspread.service_account(filename=(config_dir / "service_account.json"))
    defect_sheet = gc.open_by_key(defect_sheet_id)
    return defect_sheet.get_worksheet(0)

class Container(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=[CONFIG_DIR / "config.yaml"])

    engine = providers.Singleton(
        construct_engine,
        user=config.dormyboba.postgres.user,
        password=config.dormyboba.postgres.password,
        host=config.dormyboba.postgres.host,
        db=config.dormyboba.postgres.db,
    )

    worksheet = providers.Singleton(
        construct_worksheet,
        config_dir=CONFIG_DIR,
        defect_sheet_id=config.dormyboba.gc.defect_sheet_id,
    )

    user_repository = providers.Singleton(
        SqlAlchemyDormybobaUserRepository,
        engine,
    )

    role_repository = providers.Singleton(
        SqlAlchemyDormybobaRoleRepository,
        engine,
    )

    institute_repository = providers.Singleton(
        SqlAlchemyInstituteRepository,
        engine,
    )

    academic_type_repository = providers.Singleton(
        SqlAlchemyAcademicTypeRepository,
        engine,
    )

    mailing_repository = providers.Singleton(
        SqlAlchemyMailingRepository,
        engine,
    )

    queue_repository = providers.Singleton(
        SqlAlchemyQueueRepository,
        engine,
    )

    sheet_repository = providers.Singleton(
        GsheetDefectRepository,
        worksheet,
    )

    token_converter = providers.Singleton(
        TokenConverter,
        config.dormyboba.private_key
    )

    dormyboba_servicer = providers.Singleton(
        DormybobaCoreServicer,
        user_repository=user_repository,
        role_repository=role_repository,
        institute_repository=institute_repository,
        academic_type_repository=academic_type_repository,
        mailing_repository=mailing_repository,
        queue_repository=queue_repository,
        sheet_repository=sheet_repository,
        token_converter=token_converter,
    )

    dormyboba_server = providers.Singleton(
        DormybobaServer,
        dormyboba_servicer,
    )
