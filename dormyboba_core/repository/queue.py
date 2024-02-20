from typing import List, Optional
import abc
from datetime import datetime
from sqlalchemy import Engine, select, update, insert, delete, and_
from sqlalchemy.orm import Session
from .. import entity
from .. import model

class QueueRepository(metaclass=abc.ABCMeta):
    """An interface to queue repository"""

    @abc.abstractmethod
    def add(self, queue: entity.Queue) -> entity.Queue:
        raise NotImplementedError()

    @abc.abstractmethod
    def getById(self, queue_id: int) -> Optional[entity.Queue]:
        raise NotImplementedError()

    @abc.abstractmethod
    def update(self, queue: entity.Queue) -> entity.Queue:
        raise NotImplementedError()

    @abc.abstractmethod
    def addUser(self, queue: entity.Queue, user: entity.DormybobaUser) -> entity.Queue:
        raise NotImplementedError()

    @abc.abstractmethod
    def deleteUser(self, queue: entity.Queue, user: entity.DormybobaUser) -> entity.Queue:
        raise NotImplementedError()

    @abc.abstractmethod
    def moveQueue(self, queue: entity.Queue) -> entity.Queue:
        raise NotImplementedError()

    @abc.abstractmethod
    def getEvent(self) -> Optional[entity.QueueEvent]:
        raise NotImplementedError()

class SqlAlchemyQueueRepository(QueueRepository):
    """SqlAlchemy implementation of queue repository"""

    def __init__(self, engine: Engine):
        self.engine = engine

    def add(self, queue: entity.Queue) -> entity.Queue:
        model_queue = queue.to_model()
        with Session(self.engine) as session, session.begin():
            session.add(model_queue)
            return entity.Queue.from_model(model_queue)

    def getById(self, queue_id: int) -> Optional[entity.Queue]:
        with Session(self.engine) as session, session.begin():
            q = session.query(model.Queue)
            q = q.filter(model.Queue.queue_id == queue_id)
            res = q.one()
            return entity.Queue.from_model(res)

    def update(self, queue: entity.Queue) -> entity.Queue:
        with Session(self.engine) as session, session.begin():
            session.merge(queue.to_model())
            return entity.Queue.from_model(queue.to_model())

    def addUser(self, queue: entity.Queue, user: entity.DormybobaUser) -> entity.Queue:
        with Session(self.engine) as session, session.begin():
            stmt = select(model.Queue).where(
                model.Queue.queue_id == queue.queue_id)
            res = session.execute(stmt).first()

            if res is None:
                raise ValueError("No such queue")

            model_queue: model.Queue = res[0]
            if model_queue.active_user == None:
                stmt = update(model.Queue).where(
                    model.Queue.queue_id == model_queue.queue_id,
                ).values(
                    active_user_id=user.user_id
                )
            else:
                # just throw if user already joined queue
                stmt = insert(model.QueueToUser).values(
                    user_id=user.user_id,
                    queue_id=queue.queue_id,
                    joined=datetime.now(),
                )
            session.execute(stmt)
            session.flush()
            stmt = select(model.Queue).where(
                model.Queue.queue_id == queue.queue_id)
            model_queue = session.execute(stmt).first()[0]
            return entity.Queue.from_model(model_queue)

    def deleteUser(self, queue: entity.Queue, user: entity.DormybobaUser) -> None:
        with Session(self.engine) as session, session.begin():
            stmt = delete(model.QueueToUser).where(
                and_(
                    model.QueueToUser.user_id == user.user_id,
                    model.QueueToUser.queue_id == queue.queue_id,
                )
            )
            session.execute(stmt)

    def moveQueue(self, queue: entity.Queue) -> entity.Queue:
        with Session(self.engine) as session, session.begin():
            model_queue = session.merge(queue.to_model())

            if len(model_queue.queue_to_user) == 0:
                model_queue.active_user = None
            else:
                qtu = min(model_queue.queue_to_user, key=lambda qtu: qtu.joined)
                model_queue.active_user = qtu.user
                session.delete(qtu)

            return entity.Queue.from_model(model_queue)

    def getEvent(self) -> Optional[entity.QueueEvent]:
        with Session(self.engine) as session, session.begin():
            stmt = select(model.Queue).where(
                and_(
                    datetime.now() > model.Queue.open,
                    model.Queue.is_event_generated == False,
                )
            )
            res = session.execute(stmt).first()

            if res is None:
                return None

            model_queue: model.Queue = res[0]

            stmt = select(model.DormybobaUser)
            rows = session.execute(stmt).all()

            stmt = update(model.Queue).where(
                model.Queue.queue_id == model_queue.queue_id,
            ).values(is_event_generated=True)
            session.execute(stmt)

            return entity.QueueEvent(
                queue=entity.Queue.from_model(model_queue),
                users=list([entity.DormybobaUser.from_model(row[0]) for row in rows]),
            )
