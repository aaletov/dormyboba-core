import pytest
from unittest.mock import Mock
from dormyboba_core.entity.institute import Institute

@pytest.fixture
def api_institute_mock_with_full_fields():
    return Mock(spec=['institute_id', 'institute_name'], institute_id=1, institute_name='Example Institute')

@pytest.fixture
def api_institute_mock_with_none_name():
    return Mock(spec=['institute_id', 'institute_name'], institute_id=1, institute_name='')

def test_from_api(api_institute_mock_with_full_fields):
    result = Institute.from_api(api_institute_mock_with_full_fields)
    assert result.institute_id == api_institute_mock_with_full_fields.institute_id
    assert result.institute_name == api_institute_mock_with_full_fields.institute_name

def test_from_api_if_statement(api_institute_mock_with_none_name):
    result = Institute.from_api(api_institute_mock_with_none_name)
    assert result.institute_id == api_institute_mock_with_none_name.institute_id
    assert result.institute_name == None

def test_to_api():
    institute = Institute(institute_id=1, institute_name='Example Institute')
    result = institute.to_api()
    assert result.institute_id == institute.institute_id
    assert result.institute_name == institute.institute_name

def test_from_model(api_institute_mock_with_full_fields):
    result = Institute.from_model(api_institute_mock_with_full_fields)
    assert result.institute_id == api_institute_mock_with_full_fields.institute_id
    assert result.institute_name == api_institute_mock_with_full_fields.institute_name

def test_to_model():
    institute = Institute(institute_id=1, institute_name='Example Institute')
    result = institute.to_model()
    assert result.institute_id == institute.institute_id
    assert result.institute_name == institute.institute_name
