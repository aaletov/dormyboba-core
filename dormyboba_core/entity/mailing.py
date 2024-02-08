from typing import Optional
from dataclasses import dataclass
import datetime
from .common import (
    Institute,
    AcademicType
)

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