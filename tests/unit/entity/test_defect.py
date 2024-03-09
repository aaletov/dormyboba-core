import pytest
from unittest.mock import Mock
from dormyboba_core.entity.defect import Defect, DefectType, DefectStatus

class ApiDefectTypeStub:
    ELECTRICITY = 0
    PLUMB = 1
    COMMON = 2

class ApiDefectStatusStub:
    CREATED = 0
    ACCEPTED = 1
    RESOLVED = 2

class ApiDefectStub:
    def __init__(self, defect_id, user_id, defect_type, description, defect_status):
        self.defect_id = defect_id
        self.user_id = user_id
        self.defect_type = defect_type
        self.description = description
        self.defect_status = defect_status
    
    def HasField(self, field):
        return getattr(self, field, None) is not None

class ModelDefectStub:
    def __init__(self, defect_id, user_id, defect_type, description, defect_status):
        self.defect_id = defect_id
        self.user_id = user_id
        self.defect_type = defect_type
        self.description = description
        self.defect_status = defect_status

@pytest.fixture
def api_defect_stub_with_full_fields():
    return ApiDefectStub(
        defect_id='1',
        user_id=1,
        defect_type=ApiDefectTypeStub.ELECTRICITY,
        description='Example Description',
        defect_status=ApiDefectStatusStub.CREATED,
    )

@pytest.fixture
def api_defect_stub_with_none_defect_id():
    return ApiDefectStub(
        defect_id=None,
        user_id=1,
        defect_type=ApiDefectTypeStub.ELECTRICITY,
        description='Example Description',
        defect_status=ApiDefectStatusStub.CREATED,
    )

def test_from_api(api_defect_stub_with_full_fields):
    result = Defect.from_api(api_defect_stub_with_full_fields)
    assert result.defect_id == api_defect_stub_with_full_fields.defect_id
    assert result.user_id == api_defect_stub_with_full_fields.user_id
    assert result.defect_type == DefectType.ELECTRICITY
    assert result.description == api_defect_stub_with_full_fields.description
    assert result.defect_status == DefectStatus.CREATED

def test_from_api_if_statement(api_defect_stub_with_none_defect_id):
    result = Defect.from_api(api_defect_stub_with_none_defect_id)
    assert result.defect_id == None
    assert result.user_id == api_defect_stub_with_none_defect_id.user_id
    assert result.defect_type == DefectType.ELECTRICITY
    assert result.description == api_defect_stub_with_none_defect_id.description
    assert result.defect_status == DefectStatus.CREATED

def test_to_api():
    defect = Defect(
        defect_id='1',
        user_id=1,
        defect_type=DefectType.ELECTRICITY,
        description='Example Description',
        defect_status=DefectStatus.CREATED,
    )
    result = defect.to_api()
    assert result.defect_id == defect.defect_id
    assert result.user_id == defect.user_id
    assert result.defect_type == ApiDefectTypeStub.ELECTRICITY
    assert result.description == defect.description
    assert result.defect_status == ApiDefectStatusStub.CREATED

def test_to_model():
    defect = Defect(
        defect_id='1',
        user_id=1,
        defect_type=DefectType.ELECTRICITY,
        description='Example Description',
        defect_status=DefectStatus.CREATED,
    )
    result = defect.to_model()
    assert result[0] == defect.defect_id
    assert result[1] == defect.user_id
    assert result[2] == "Электрика"
    assert result[3] == defect.description
    assert result[4] == "Добавлено"