from typing import List, Optional
import abc
from sqlalchemy.orm import Session
from sqlalchemy import Engine, select, insert
from .. import entity
from .. import model

class DormybobaUserRepository(metaclass=abc.ABCMeta):
    """An interface to dormyboba user repository"""

    @abc.abstractmethod
    def list(self) -> List[entity.DormybobaUser]:
        raise NotImplementedError()

    @abc.abstractmethod
    def add(self, user: entity.DormybobaUser) -> entity.DormybobaUser:
        raise NotImplementedError()

    @abc.abstractmethod
    def getById(self, user_id: int) -> Optional[entity.DormybobaUser]:
        raise NotImplementedError()

    @abc.abstractmethod
    def listByRole(self, role: entity.DormybobaRole) -> List[entity.DormybobaUser]:
        raise NotImplementedError()

class SqlAlchemyDormybobaUserRepository(DormybobaUserRepository):
    """SqlAlchemy implementation of dormyboba user repository"""

    def __init__(self, engine: Engine):
        self.engine = engine

    def list(self) -> List[entity.DormybobaUser]:
        return super().list()

    def add(self, user: entity.DormybobaUser) -> entity.DormybobaUser:
        model_user = user.to_model()
        with Session(self.engine) as session, session.begin():
            session.add(model_user)
            session.flush()
            return entity.DormybobaUser.from_model(model_user)

    def update(self, user: entity.DormybobaUser) -> entity.DormybobaUser:
        model_user = user.to_model()
        with Session(self.engine) as session, session.begin():
            model_user = session.merge(model_user)
            session.flush()
            return entity.DormybobaUser.from_model(model_user)

    def getById(self, user_id: int) -> Optional[entity.DormybobaUser]:
        with Session(self.engine) as session, session.begin():
            stmt = select(model.DormybobaUser).where(
                model.DormybobaUser.user_id == user_id,
            )
            res = session.execute(stmt).first()
            if res is None:
                return None
            user: model.DormybobaUser = res[0]
            return entity.DormybobaUser.from_model(user)

    def listByRole(self, role: entity.DormybobaRole) -> List[entity.DormybobaUser]:
        with Session(self.engine) as session, session.begin():
            stmt = select(model.DormybobaUser).join(
                model.DormybobaRole,
                model.DormybobaUser.role_id == role.role_id,
            )
            res = session.execute(stmt).all()
            return list([entity.DormybobaUser.from_model(row[0]) for row in res])

class DormybobaRoleRepository(metaclass=abc.ABCMeta):
    """An interface to dormyboba user repository"""

    @abc.abstractmethod
    def getByName(role_name: str) -> Optional[entity.DormybobaRole]:
        raise NotImplementedError()

class SqlAlchemyDormybobaRoleRepository(DormybobaRoleRepository):
    """SqlAlchemy implementation of dormyboba role repository"""

    def __init__(self, engine: Engine):
        self.engine = engine

    def getByName(self, role_name: str) -> Optional[entity.DormybobaRole]:
        with Session(self.engine) as session, session.begin():
            model_role = session.query(model.DormybobaRole).filter(
                model.DormybobaRole.role_name == role_name
            ).first()

            if model_role is None:
                return None

            return entity.DormybobaRole.from_model(model_role)