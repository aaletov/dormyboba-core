import pytest
from unittest.mock import Mock
from dormyboba_core.entity.academic_type import AcademicType

@pytest.fixture
def api_academic_type_mock_with_full_fields():
    return Mock(spec=['type_id', 'type_name'], type_id=1, type_name='Example Type')

@pytest.fixture
def api_academic_type_mock_with_none_name():
    return Mock(spec=['type_id', 'type_name'], type_id=1, type_name='')

def test_from_api(api_academic_type_mock_with_full_fields):
    result = AcademicType.from_api(api_academic_type_mock_with_full_fields)
    assert result.type_id == api_academic_type_mock_with_full_fields.type_id
    assert result.type_name == api_academic_type_mock_with_full_fields.type_name

def test_from_api_if_statement(api_academic_type_mock_with_none_name):
    result = AcademicType.from_api(api_academic_type_mock_with_none_name)
    assert result.type_id == api_academic_type_mock_with_none_name.type_id
    assert result.type_name == None

def test_to_api():
    academic_type = AcademicType(type_id=1, type_name='Example Type')
    result = academic_type.to_api()
    assert result.type_id == academic_type.type_id
    assert result.type_name == academic_type.type_name

def test_from_model(api_academic_type_mock_with_full_fields):
    result = AcademicType.from_model(api_academic_type_mock_with_full_fields)
    assert result.type_id == api_academic_type_mock_with_full_fields.type_id
    assert result.type_name == api_academic_type_mock_with_full_fields.type_name

def test_to_model():
    academic_type = AcademicType(type_id=1, type_name='Example Type')
    result = academic_type.to_model()
    assert result.type_id == academic_type.type_id
    assert result.type_name == academic_type.type_name
