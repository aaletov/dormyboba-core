import unittest
from dormyboba_core import entity, model
from sqlalchemy import create_engine
from unittest.mock import patch
from sqlalchemy.orm import Session
from dormyboba_core.repository.dormyboba_user import (
    SqlAlchemyDormybobaUserRepository,
    SqlAlchemyDormybobaRoleRepository,
)


class TestSqlAlchemyDormybobaUserRepository(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.repo = SqlAlchemyDormybobaUserRepository(self.engine)
        model.Base.metadata.create_all(self.engine)

    def test_add_user(self):
        user = entity.DormybobaUser(
            role=entity.DormybobaRole(role_id=1, role_name='student'),
            user_id=1,
            institute=entity.Institute(institute_id=1, institute_name="sample institue"),
            academic_type=entity.AcademicType(type_id=1, type_name="sample name"),
            year=2024,
            group='3530904/00104',
            is_registered=True
        )
        added_user = self.repo.add(user)
        self.assertEqual(added_user.user_id, 1)

    def test_get_user_by_id(self):
        with Session(self.engine) as session, session.begin():
            model_user = model.DormybobaUser(
                user_id=1,
                role_id=1,
                registration_complete=True
            )
            session.add(model_user)

        retrieved_user = self.repo.getById(1)
        self.assertEqual(retrieved_user.user_id, 1)

    def test_get_user_by_invalid_id(self):
        retrieved_user = self.repo.getById(100)
        self.assertIsNone(retrieved_user)


class TestSqlAlchemyDormybobaRoleRepository(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.repo = SqlAlchemyDormybobaRoleRepository(self.engine)
        model.Base.metadata.create_all(self.engine)

    def test_get_role_by_name(self):
        with Session(self.engine) as session, session.begin():
            model_role = model.DormybobaRole(role_id=1, role_name='admin')
            session.add(model_role)

        retrieved_role = self.repo.getByName('admin')
        self.assertEqual(retrieved_role.role_name, 'admin')

    def test_get_role_by_invalid_name(self):
        retrieved_role = self.repo.getByName('invalid_role')
        self.assertIsNone(retrieved_role)

