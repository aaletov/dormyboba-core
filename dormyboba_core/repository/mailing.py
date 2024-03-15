from typing import List, Optional
import abc
import datetime
from sqlalchemy import Engine, select, insert, update, and_, or_
from sqlalchemy.orm import Session
from .. import entity
from .. import model

class MailingRepository(metaclass=abc.ABCMeta):
    """An interface to mailing repository"""

    @abc.abstractmethod
    def add(self, mailing: entity.Mailing) -> entity.Mailing:
        raise NotImplementedError()

    @abc.abstractmethod
    def getEvent(self) -> Optional[entity.MailingEvent]:
        raise NotImplementedError()

    @abc.abstractmethod
    def update(self, mailing: entity.Mailing) -> None:
        raise NotImplementedError()

class SqlAlchemyMailingRepository(MailingRepository):
    """SqlAlchemy implementation of mailing repository"""

    def __init__(self, engine: Engine):
        self.engine = engine

    def add(self, mailing: entity.Mailing) -> entity.Mailing:
        model_mailing = mailing.to_model()
        with Session(self.engine) as session, session.begin():
            session.add(model_mailing)
            session.flush()
            session.refresh(model_mailing)
            return entity.Mailing.from_model(model_mailing)

    def getEvent(self) -> Optional[entity.MailingEvent]:
        with Session(self.engine) as session, session.begin():
            stmt = select(model.Mailing).where(
                and_(
                    or_(
                        model.Mailing.at == None,
                        datetime.datetime.now() > model.Mailing.at,
                    ),
                    model.Mailing.is_event_generated == False,
                )
            )
            res = session.execute(stmt).first()

            if res is None:
                return None

            model_mailing: model.Mailing = res[0]
            conditions = []
            if model_mailing.institute is not None:
                conditions.append(
                    model.DormybobaUser.institute_id == model_mailing.institute_id,
                )
            if model_mailing.academic_type is not None:
                conditions.append(
                    model.DormybobaUser.academic_type_id == model_mailing.academic_type_id,
                )
            if model_mailing.enroll_year is not None:
                conditions.append(
                    model.DormybobaUser.enroll_year == model_mailing.enroll_year,
                )
            if model_mailing.academic_group is not None:
                conditions.append(
                    model.DormybobaUser.academic_group == model_mailing.academic_group,
                )

            stmt = select(model.DormybobaUser).where(
                and_(*conditions),
            )
            rows = session.execute(stmt).all()

            stmt = update(model.Mailing).where(
                model.Mailing.mailing_id == model_mailing.mailing_id,
            ).values(is_event_generated=True)
            session.execute(stmt)

            return entity.MailingEvent(
                mailing=entity.Mailing.from_model(model_mailing),
                users=list([entity.DormybobaUser.from_model(row[0]) for row in rows])
            )

    def update(self, mailing: entity.Mailing) -> None:
        model_mailing = mailing.to_model()
        with Session(self.engine) as session, session.begin():
            session.merge(model_mailing)
            return entity.Mailing.from_model(model_mailing)
