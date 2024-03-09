import unittest
from unittest.mock import Mock, patch
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from dormyboba_core.repository.institute import SqlAlchemyInstituteRepository, InstituteRepository
import dormyboba_core.model as model
from sqlalchemy.sql import text


class TestSqlAlchemyInstituteRepository(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.repo = SqlAlchemyInstituteRepository(self.engine)
        model.Base.metadata.create_all(self.engine)

    def test_list(self):
        with Session(self.engine) as session, session.begin():
            institute1 = model.Institute(institute_name="Institute A")
            institute2 = model.Institute(institute_name="Institute B")
            session.add(institute1)
            session.add(institute2)

        result = self.repo.list()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].institute_name, "Institute A")
        self.assertEqual(result[1].institute_name, "Institute B")

    def test_getByName_existing(self):
        with Session(self.engine) as session, session.begin():
            institute = model.Institute(institute_name="Institute A")
            session.add(institute)

        result = self.repo.getByName("Institute A")
        self.assertIsNotNone(result)
        self.assertEqual(result.institute_name, "Institute A")

    def test_getByName_non_existing(self):
        with Session(self.engine) as session, session.begin():
            institute = model.Institute(institute_name="Institute A")
            session.add(institute)

        result = self.repo.getByName("Non-existent Institute")
        self.assertIsNone(result)

