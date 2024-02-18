import unittest
from unittest.mock import Mock, patch
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from dormyboba_core.repository.academic_type import SqlAlchemyAcademicTypeRepository, AcademicTypeRepository
import dormyboba_core.model as model
from sqlalchemy.sql import text


class TestSqlAlchemyAcademicTypeRepository(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.repo = SqlAlchemyAcademicTypeRepository(self.engine)
        model.Base.metadata.create_all(self.engine)

    def test_list(self):
        with Session(self.engine) as session, session.begin():
            academic_type = model.AcademicType(type_id=1, type_name="student")
            session.add(academic_type)

        result = self.repo.list()
        self.assertEqual(len(result), 1)

    def test_getByName(self):
        with Session(self.engine) as session, session.begin():
            academic_type = model.AcademicType(type_id=1, type_name="student")
            session.add(academic_type)

        result = self.repo.getByName("student")
        self.assertEqual(result.type_id, 1)
        self.assertEqual(result.type_name, "student")

class ConcreteAcademicTypeRepository(AcademicTypeRepository):

    def list(self):
        return []

    def getByName(self, name):
        return None

class TestConcreteAcademicTypeRepository(unittest.TestCase):

    def setUp(self):
        self.repo = ConcreteAcademicTypeRepository()

    def test_list(self):
        result = self.repo.list()
        self.assertEqual(len(result), 0)

    def test_getByName(self):
        result = self.repo.getByName('test')
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
