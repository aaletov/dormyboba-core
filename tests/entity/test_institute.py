import pytest
from unittest.mock import Mock
from dormyboba_core.entity.institute import Institute

@pytest.fixture
def api_institute_example():
    return Mock(spec=['institute_id', 'institute_name'], institute_id=1, institute_name='Example Institute')

def test_from_api(api_institute_example):
    result = Institute.from_api(api_institute_example)
    assert result.institute_id == api_institute_example.institute_id
    assert result.institute_name == api_institute_example.institute_name

def test_to_api():
    institute = Institute(institute_id=1, institute_name='Example Institute')
    result = institute.to_api()
    assert result.institute_id == institute.institute_id
    assert result.institute_name == institute.institute_name

def test_from_model():
    model_institute = Mock(spec=['institute_id', 'institute_name'], institute_id=1, institute_name='Example Institute')
    result = Institute.from_model(model_institute)
    assert result.institute_id == model_institute.institute_id
    assert result.institute_name == model_institute.institute_name

def test_to_model():
    institute = Institute(institute_id=1, institute_name='Example Institute')
    result = institute.to_model()
    assert result.institute_id == institute.institute_id
    assert result.institute_name == institute.institute_name
