import datetime
import unittest
from dormyboba_core import entity, model
from sqlalchemy import create_engine
from unittest.mock import patch
from sqlalchemy.orm import Session
from dormyboba_core.repository.mailing import SqlAlchemyMailingRepository


class TestSqlAlchemyMailingRepository(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.repo = SqlAlchemyMailingRepository(self.engine)
        model.Base.metadata.create_all(self.engine)

    def test_add_mailing(self):
        mailing = entity.Mailing(
            mailing_id=1,
            at=datetime.datetime.now(),
            is_event_generated=False,
            theme = "sample theme",
            mailing_text= "sample text",
            institute=entity.Institute(institute_id=1, institute_name="sample institue"),
            academic_type=entity.AcademicType(type_id=1, type_name="sample name"),
            year=2024,
            group='A',
        )
        added_mailing = self.repo.add(mailing)
        self.assertEqual(added_mailing.mailing_id, 1)

    def test_get_event(self):
        with Session(self.engine) as session, session.begin():
            model_mailing = model.Mailing(
                mailing_id=1,
                at=datetime.datetime.now() - datetime.timedelta(10),
                is_event_generated=False,
            )
            session.add(model_mailing)

        mailing_event = self.repo.getEvent()
        self.assertIsNotNone(mailing_event)
        self.assertEqual(mailing_event.mailing.mailing_id, 1)

    @patch('dormyboba_core.model.generated.Mailing')
    def test_update_mailing(self, mock_model_mailing):
        mailing = entity.Mailing(
            mailing_id=1,
            at=datetime.datetime.now(),
            is_event_generated=False,
            theme="sample theme",
            mailing_text="sample text",
            institute=entity.Institute(institute_id=1, institute_name="sample institue"),
            academic_type=entity.AcademicType(type_id=1, type_name="sample name"),
            year=2022,
            group='A',
        )
        mock_model_mailing.to_model.return_value = model.Mailing()
        self.repo.update(mailing)
