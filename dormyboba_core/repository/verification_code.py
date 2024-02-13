from typing import Optional
import abc
from sqlalchemy import Engine, select, insert
from sqlalchemy.orm import Session
from .. import entity
from .. import model

class VerificationCodeRepository(metaclass=abc.ABCMeta):
    """An interface to verification code repository"""

    @abc.abstractmethod
    def getByCode(self, code: int) -> entity.VerificationCode:
        raise NotImplementedError()
    
    @abc.abstractmethod
    def getRole(self, verification_code: entity.VerificationCode) -> Optional[entity.DormybobaRole]:
        raise NotImplementedError()
    
    @abc.abstractmethod
    def add(self, verification_code: entity.VerificationCode) -> None:
        raise NotImplementedError()
    
class SqlAlchemyVerificationCodeRepository(VerificationCodeRepository):
    """SqlAlchemy implementation of verification code repository"""

    def __init__(self, engine: Engine):
        self.engine = engine

    def add(self, verification_code: entity.VerificationCode) -> None:
        with Session(self.engine) as session, session.begin():
            stmt = select(model.DormybobaRole).where(
                model.DormybobaRole.role_name == verification_code.role.role_name,
            )
            res = session.execute(stmt).first()
            role: model.DormybobaRole = res[0]
            stmt = insert(model.VerificationCode).values(
                code=verification_code.verification_code,
                role_id=role.role_id,
            )
            session.execute(stmt)

    def getByCode(self, code: int) -> Optional[entity.VerificationCode]:
        with Session(self.engine) as session, session.begin():
            stmt = select(model.VerificationCode).where(
                model.VerificationCode.code == code,
            )
            res = session.execute(stmt).first()
            return None if res is None else entity.VerificationCode.from_model(res[0])
    
    def getRole(self, verification_code: entity.VerificationCode) -> Optional[entity.DormybobaRole]:
        with Session(self.engine) as session, session.begin():
            stmt = select(model.DormybobaRole).join(
                model.VerificationCode,
                model.DormybobaRole.role_id == model.VerificationCode.role_id,
            ).where(
                model.VerificationCode.code == verification_code.verification_code,
            )
            res = session.execute(stmt).first()
            if res is None:
                return None
            return entity.DormybobaRole.from_model(res[0])
    