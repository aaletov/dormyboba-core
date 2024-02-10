from typing import List, Optional
import abc
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session
from .. import entity
from .. import model

class InstituteRepository(abc.ABCMeta):
    """An interface to institue repository"""

    def list(self) -> List[entity.Institute]:
        raise NotImplementedError
    
class SqlAlchemyInstituteRepository(InstituteRepository):
    """SqlAlchemy implementation of institute repository"""

    def __init__(self, engine: Engine):
        self.engine = engine

    def list(self) -> List[entity.Institute]:
        with Session(self.engine) as session, session.begin():
            stmt = select(model.Institute)
            res = session.execute(stmt).all()
            return list([entity.Institute.from_model(row[0]) for row in res])
        
    def getByName(self, name: str) -> Optional[entity.Institute]:
        with Session(self.engine) as session, session.begin():
            stmt = select(model.Institute).where(
                model.Institute.institute_name == name,
            )
            res = session.execute(stmt).first()
            
            if res is None:
                return None
            
            return entity.Institute.from_model(res[0]) 
