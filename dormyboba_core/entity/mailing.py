from __future__ import annotations
from typing import Optional, List
from dataclasses import dataclass
import datetime
from google.protobuf.timestamp_pb2 import Timestamp
import dormyboba_api.v1api_pb2 as apiv1
from .. import model
from .. import entity

@dataclass
class Mailing:
    """A value object that represents mailing"""
    mailing_id: int
    theme: Optional[str]
    mailing_text: str
    at: Optional[datetime.datetime]
    institute: Optional[entity.Institute]
    academic_type: Optional[entity.AcademicType]
    year: Optional[int]
    group: Optional[str]
    is_event_generated: Optional[bool]

    @staticmethod
    def from_api(api_mailing: apiv1.Mailing) -> 'Mailing':
        mailing_id = None if not(api_mailing.HasField("mailing_id")) else api_mailing.mailing_id
        at = None if not(api_mailing.HasField("at")) else api_mailing.at.ToDatetime()
        institute = None if not(api_mailing.HasField("institute_id")) else entity.Institute(
            institute_id=api_mailing.institute_id,
            institute_name=None,
        )
        academic_type = None if not(api_mailing.HasField("academic_type_id")) else entity.AcademicType(
            type_id=api_mailing.academic_type_id,
            type_name=None,
        )
        year = None if not(api_mailing.HasField("year")) else api_mailing.year
        group = None if not(api_mailing.HasField("group")) else api_mailing.group
        return Mailing(
            mailing_id=mailing_id,
            theme=api_mailing.theme,
            mailing_text=api_mailing.mailing_text,
            at=at,
            institute=institute,
            academic_type=academic_type,
            year=year,
            group=group,
            is_event_generated=None,
        )

    def to_api(self) -> apiv1.Mailing:
        at = None
        if self.at is not None:
            at = Timestamp()
            at.FromDatetime(self.at)

        instutute_id = None if self.institute is None else self.institute.institute_id
        academic_type_id = None if self.academic_type is None else self.academic_type.type_id

        return apiv1.Mailing(
            mailing_id=self.mailing_id,
            theme=self.theme,
            mailing_text=self.mailing_text,
            at=at,
            institute_id=instutute_id,
            academic_type_id=academic_type_id,
            year=self.year,
            group=self.group,
        )

    @staticmethod
    def from_model(model_mailing: model.Mailing) -> 'Mailing':
        institute = None
        if model_mailing.institute is not None:
            institute = entity.Institute.from_model(model_mailing.institute)

        academic_type = None
        if model_mailing.academic_type is not None:
            academic_type = entity.AcademicType.from_model(model_mailing.academic_type)

        return Mailing(
            mailing_id=model_mailing.mailing_id,
            theme=model_mailing.theme,
            mailing_text=model_mailing.mailing_text,
            at=model_mailing.at,
            institute=institute,
            academic_type=academic_type,
            year=model_mailing.enroll_year,
            group=model_mailing.academic_group,
            is_event_generated=model_mailing.is_event_generated,
        )

    def to_model(self) -> model.Mailing:
        institute_id = None
        if self.institute is not None:
            institute_id = self.institute.to_model().institute_id

        academic_type_id = None
        if self.academic_type is not None:
            academic_type_id = self.academic_type.to_model().type_id

        return model.Mailing(
            mailing_id=self.mailing_id,
            theme=self.theme,
            mailing_text=self.mailing_text,
            at=self.at,
            institute_id=institute_id,
            academic_type_id=academic_type_id,
            enroll_year=self.year,
            academic_group=self.group,
            is_event_generated=self.is_event_generated,
        )

@dataclass
class MailingEvent:
    mailing: Mailing
    users: List[entity.DormybobaUser]

    def to_api(self) -> apiv1.MailingEvent:
        return apiv1.MailingEvent(
            mailing=self.mailing.to_api(),
            users=list([user.to_api() for user in self.users]),
        )