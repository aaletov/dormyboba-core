import pytest
import datetime
from unittest.mock import Mock
from dormyboba_core.entity.mailing import Mailing

class EntityInstituteStub:
    institute_id = 1
    institute_name = 'Example Institute'

class EntityAcademicTypeStub:
    type_id = 1
    type_name = 'Example Type'

class ApiMailingStub:
    mailing_id = 1
    theme = 'Example Theme'
    mailing_text = 'Example Text'
    at = Mock()
    at.ToDatetime.return_value = datetime.datetime(2022, 1, 1)
    institute_id = 1
    academic_type_id = 1
    year = 2022
    group = 'A123'

    def HasField(self, field_name):
        return field_name in ["mailing_id", "at", "institute_id", "academic_type_id", "year", "group"]

@pytest.fixture
def api_mailing_stub_with_full_fields():
    return ApiMailingStub()

class ModelMailingStub:
    mailing_id = 1
    theme = 'Example Theme'
    mailing_text = 'Example Text'
    at = datetime.datetime(2022, 1, 1)
    institute = EntityInstituteStub()
    academic_type = EntityAcademicTypeStub()
    enroll_year = 2022
    academic_group = 'A123'
    is_event_generated = True

@pytest.fixture
def model_mailing_stub_with_full_fields():
    return ModelMailingStub()

def test_from_api(api_mailing_stub_with_full_fields):
    result = Mailing.from_api(api_mailing_stub_with_full_fields)
    assert result.mailing_id == api_mailing_stub_with_full_fields.mailing_id
    assert result.theme == api_mailing_stub_with_full_fields.theme
    assert result.mailing_text == api_mailing_stub_with_full_fields.mailing_text
    assert result.at == datetime.datetime(2022, 1, 1)

    assert result.institute.institute_id == api_mailing_stub_with_full_fields.institute_id
    assert result.institute.institute_name == None 

    assert result.academic_type.type_id == api_mailing_stub_with_full_fields.academic_type_id
    assert result.academic_type.type_name == None

    assert result.year == api_mailing_stub_with_full_fields.year
    assert result.group == api_mailing_stub_with_full_fields.group
    assert result.is_event_generated == None

def test_to_api(api_mailing_stub_with_full_fields):
    mailing = Mailing.from_api(api_mailing_stub_with_full_fields)
    result = mailing.to_api()

    assert result.mailing_id == api_mailing_stub_with_full_fields.mailing_id
    assert result.theme == api_mailing_stub_with_full_fields.theme
    assert result.mailing_text == api_mailing_stub_with_full_fields.mailing_text
    assert result.at.ToDatetime() == datetime.datetime(2022, 1, 1)

    assert result.institute_id == api_mailing_stub_with_full_fields.institute_id
    assert result.academic_type_id == api_mailing_stub_with_full_fields.academic_type_id
    assert result.year == api_mailing_stub_with_full_fields.year
    assert result.group == api_mailing_stub_with_full_fields.group

def test_from_model(model_mailing_stub_with_full_fields):
    result = Mailing.from_model(model_mailing_stub_with_full_fields)
    assert result.mailing_id == model_mailing_stub_with_full_fields.mailing_id
    assert result.theme == model_mailing_stub_with_full_fields.theme
    assert result.mailing_text == model_mailing_stub_with_full_fields.mailing_text
    assert result.at == model_mailing_stub_with_full_fields.at

    assert result.institute.institute_id == model_mailing_stub_with_full_fields.institute.institute_id
    assert result.institute.institute_name == model_mailing_stub_with_full_fields.institute.institute_name

    assert result.academic_type.type_id == model_mailing_stub_with_full_fields.academic_type.type_id
    assert result.academic_type.type_name == model_mailing_stub_with_full_fields.academic_type.type_name

    assert result.year == model_mailing_stub_with_full_fields.enroll_year
    assert result.group == model_mailing_stub_with_full_fields.academic_group
    assert result.is_event_generated == model_mailing_stub_with_full_fields.is_event_generated

def test_to_model(model_mailing_stub_with_full_fields):
    mailing = Mailing.from_model(model_mailing_stub_with_full_fields)
    result = mailing.to_model()

    assert result.mailing_id == model_mailing_stub_with_full_fields.mailing_id
    assert result.theme == model_mailing_stub_with_full_fields.theme
    assert result.mailing_text == model_mailing_stub_with_full_fields.mailing_text
    assert result.at == model_mailing_stub_with_full_fields.at

    assert result.institute_id == model_mailing_stub_with_full_fields.institute.institute_id
    assert result.is_event_generated == model_mailing_stub_with_full_fields.is_event_generated
