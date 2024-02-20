from datetime import datetime, timedelta
import unittest
from unittest.mock import Mock, patch
from dormyboba_core import entity
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from dormyboba_core.repository.queue import SqlAlchemyQueueRepository
import dormyboba_core.model as model
from sqlalchemy.sql import text


class TestSqlAlchemyQueueRepository(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.repo = SqlAlchemyQueueRepository(self.engine)
        model.Base.metadata.create_all(self.engine)

    def test_add(self):
        user = entity.DormybobaUser(
            role=entity.DormybobaRole(role_id=1, role_name='student'),
            user_id=1,
            institute=entity.Institute(institute_id=1, institute_name="sample institue"),
            academic_type=entity.AcademicType(type_id=1, type_name="sample name"),
            year=2024,
            group='3530904/00104',
            is_registered=True
        )
        queue = entity.Queue(
            title='sample title',
            description='sample desc',
            active_user=user,
            queue_id=1,
            is_event_generated=True,
            open=datetime.now(),
            close=datetime.now(),
        )
        result = self.repo.add(queue)
        self.assertEqual(result.queue_id, 1)

    def test_getById(self):
        with Session(self.engine) as session, session.begin():
            model_queue = model.Queue(queue_id=1, open=datetime.now())
            session.add(model_queue)

        result = self.repo.getById(1)
        self.assertEqual(result.queue_id, 1)

    def test_deleteUser(self):
        user = entity.DormybobaUser(
            role=entity.DormybobaRole(role_id=1, role_name='student'),
            user_id=1,
            institute=entity.Institute(institute_id=1, institute_name="sample institue"),
            academic_type=entity.AcademicType(type_id=1, type_name="sample name"),
            year=2024,
            group='3530904/00104',
            is_registered=True
        )
        queue = entity.Queue(
            title='sample title',
            description='sample desc',
            active_user=user,
            queue_id=1,
            is_event_generated=True,
            open=datetime.now(),
            close=datetime.now(),
        )
        with Session(self.engine) as session, session.begin():
            model_queue = queue.to_model()
            session.add(model_queue)

        self.repo.deleteUser(queue, user)
        result = self.repo.getById(1)
        self.assertEqual(result.active_user, None)

    def test_update(self):
        user = entity.DormybobaUser(
            role=entity.DormybobaRole(role_id=1, role_name='student'),
            user_id=1,
            institute=entity.Institute(institute_id=1, institute_name="sample institue"),
            academic_type=entity.AcademicType(type_id=1, type_name="sample name"),
            year=2024,
            group='3530904/00104',
            is_registered=True
        )
        queue = entity.Queue(
            title='sample title',
            description='sample desc',
            active_user=user,
            queue_id=1,
            is_event_generated=True,
            open=datetime.now(),
            close=datetime.now(),
        )
        with Session(self.engine) as session, session.begin():
            model_queue = queue.to_model()
            session.add(model_queue)
        updated_queue = entity.Queue(
            title='new title',
            description='sample desc',
            active_user=user,
            queue_id=1,
            is_event_generated=True,
            open=datetime.now(),
            close=datetime.now(),
        )
        result = self.repo.update(updated_queue)
        self.assertEqual(result.title, 'new title')
    
    def test_moveQueue(self):
        user = entity.DormybobaUser(
            role=entity.DormybobaRole(role_id=1, role_name='student'),
            user_id=1,
            institute=entity.Institute(institute_id=1, institute_name="sample institue"),
            academic_type=entity.AcademicType(type_id=1, type_name="sample name"),
            year=2024,
            group='3530904/00104',
            is_registered=True
        )
        queue = entity.Queue(
            title='sample title',
            description='sample desc',
            active_user=user,
            queue_id=1,
            is_event_generated=True,
            open=datetime.now(),
            close=datetime.now(),
        )
        with Session(self.engine) as session, session.begin():
            model_queue = queue.to_model()
            qtu = model.QueueToUser(user_id=1, queue_id=1, joined=datetime.now())
            model_queue.queue_to_user.append(qtu)
            session.add(model_queue)

        result = self.repo.moveQueue(queue)
        self.assertIsNone(result.active_user)

    def test_getEvent(self):
        with Session(self.engine) as session, session.begin():
            open_time = datetime.now() - timedelta(10)
            model_queue = model.Queue(queue_id=1, open=datetime.now(), close=open_time)
            session.add(model_queue)

        result = self.repo.getEvent()
        self.assertIsNotNone(result)

