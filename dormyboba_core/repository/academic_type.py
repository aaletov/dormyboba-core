from typing import Optional
import abc
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session
from ..import model
from ..import entity

class AcademicTypeRepository(metaclass=abc.ABCMeta):
    """An interface to academic type repository"""

    @abc.abstractmethod
    def getByName(self, name: str) -> Optional[entity.AcademicType]:
        raise NotImplementedError()
    
class SqlAlchemyAcademicTypeRepository(AcademicTypeRepository):
    """SqlAlchemy implementation of academic type repository"""

    def __init__(self, engine: Engine):
        self.engine = engine

    def getByName(self, name: str) -> Optional[entity.AcademicType]:
        with Session(self.engine) as session, session.begin():
            stmt = select(model.AcademicType).where(
                model.AcademicType.type_name == name,
            )
            res = session.execute(stmt).first()

            if res is None:
                return None

            academic_type: model.AcademicType = res[0]
            return entity.AcademicType.from_model(academic_type)
