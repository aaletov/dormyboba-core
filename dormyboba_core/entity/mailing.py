from typing import Optional, List
from dataclasses import dataclass
import datetime
from google.protobuf.timestamp_pb2 import Timestamp
import dormyboba_api.v1api_pb2 as apiv1
from .. import model
from .institute import Institute
from .academic_type import AcademicType
from .dormyboba_user import DormybobaUser

@dataclass
class Mailing:
    """A value object that represents mailing"""
    mailing_id: int
    theme: Optional[str]
    mailing_text: str
    at: Optional[datetime.datetime]
    institute: Optional[Institute]
    academic_type: Optional[AcademicType]
    year: Optional[int]
    is_event_generated: bool

    @staticmethod
    def from_api(api_mailing: apiv1.Mailing) -> 'Mailing':
        at = None if not(api_mailing.HasField("at")) else api_mailing.at.ToDatetime()
        return Mailing(
            mailing_id=api_mailing.mailing_id,
            theme=api_mailing.theme,
            mailing_text=api_mailing.mailing_text,
            at=at,
            institute=Institute.from_api(api_mailing),
            academic_type=AcademicType.from_api(api_mailing),
            year=api_mailing.year,
        )
    
    def to_api(self) -> apiv1.Mailing:
        at = None
        if self.at is not None:
            at = Timestamp()
            at.FromDatetime(self.at)
             
        return apiv1.Mailing(
            mailing_id=self.mailing_id,
            theme=self.theme,
            mailing_text=self.mailing_text,
            at=at,
            institute_id=self.institute.institute_id,
            academic_type_id=self.academic_type.type_id,
            year=self.year,
        )
    
    @staticmethod
    def from_model(model_mailing: model.Mailing) -> 'Mailing':
        return Mailing(
            mailing_id=model_mailing.mailing_id,
            theme=model_mailing.theme,
            mailing_text=model_mailing.mailing_text,
            at=model_mailing.at,
            institute=model.Institute.from_model(model_mailing.institute),
            academic_type=model.AcademicType.from_model(model_mailing.academic_type),
            year=model_mailing.enroll_year,
            is_event_generated=model_mailing.is_event_generated,
        )
    
    def to_model(self) -> model.Mailing:
        return model.Mailing(
            mailing_id=self.mailing_id,
            theme=self.theme,
            mailing_text=self.mailing_text,
            at=self.at,
            institute=self.institute.to_model(),
            academic_type=self.academic_type.to_model(),
            year=self.year,
            is_event_generated=self.is_event_generated,
        )

@dataclass
class MailingEvent:
    mailing: Mailing
    users: List[DormybobaUser]

    def to_api(self) -> apiv1.MailingEvent:
        return apiv1.MailingEvent(
            mailing=self.mailing.to_api(),
            users=list([user.to_api() for user in self.users]),
        )