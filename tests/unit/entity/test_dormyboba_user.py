import pytest
from unittest.mock import Mock
from dormyboba_core.entity.dormyboba_user import DormybobaUser, DormybobaRole, Institute, AcademicType
from dormyboba_core.entity.dormyboba_user import apiv1, model, entity

class ApiDormybobaRoleStub:
    role_id = 1
    role_name = 'Example Role'

class ApiDormybobaInstituteStub:
    institute_id = 1
    institute_name = 'Example Institute'

class ApiDormybobaAcademicTypeStub:
    type_id = 1
    type_name = 'Example Type'

class ApiDormybobaUserStub:
    user_id = 1
    role = ApiDormybobaRoleStub()
    institute = ApiDormybobaInstituteStub()
    academic_type = ApiDormybobaAcademicTypeStub()
    year = 2022
    group = 'A123'
    is_registered = True

    def HasField(self, field_name):
        return field_name in ["institute", "academic_type", "year", "group"]

@pytest.fixture
def api_dormyboba_user_stub_with_full_fields():
    return ApiDormybobaUserStub()

def test_from_api(api_dormyboba_user_stub_with_full_fields):
    result = DormybobaUser.from_api(api_dormyboba_user_stub_with_full_fields)
    assert result.user_id == api_dormyboba_user_stub_with_full_fields.user_id
    assert result.role == DormybobaRole.from_api(api_dormyboba_user_stub_with_full_fields.role)

    assert result.institute.institute_id == api_dormyboba_user_stub_with_full_fields.institute.institute_id
    assert result.institute.institute_name == None

    assert result.academic_type.type_id == api_dormyboba_user_stub_with_full_fields.academic_type.type_id
    assert result.academic_type.type_name == None

    assert result.year == api_dormyboba_user_stub_with_full_fields.year
    assert result.group == api_dormyboba_user_stub_with_full_fields.group
    assert result.is_registered == api_dormyboba_user_stub_with_full_fields.is_registered


class ModelDormybobaRoleStub:
    role_id = 1
    role_name = 'Example Role'

class ModelDormybobaInstituteStub:
    institute_id = 1
    institute_name = 'Example Institute'

class ModelDormybobaAcademicTypeStub:
    type_id = 1
    type_name = 'Example Type'

class ModelDormybobaUserStub:
    user_id = 1
    role = ModelDormybobaRoleStub()
    institute = ModelDormybobaInstituteStub()
    academic_type = ModelDormybobaAcademicTypeStub()
    enroll_year = 2022
    academic_group = 'A123'
    registration_complete = True

@pytest.fixture
def model_dormyboba_user_stub_with_full_fields():
    return ModelDormybobaUserStub()

def test_from_model(model_dormyboba_user_stub_with_full_fields):
    result = DormybobaUser.from_model(model_dormyboba_user_stub_with_full_fields)
    assert result.user_id == model_dormyboba_user_stub_with_full_fields.user_id
    assert result.role == DormybobaRole.from_model(model_dormyboba_user_stub_with_full_fields.role)
    assert result.institute == Institute.from_model(model_dormyboba_user_stub_with_full_fields.institute)
    assert result.academic_type == AcademicType.from_model(model_dormyboba_user_stub_with_full_fields.academic_type)
    assert result.year == model_dormyboba_user_stub_with_full_fields.enroll_year
    assert result.group == model_dormyboba_user_stub_with_full_fields.academic_group
    assert result.is_registered == model_dormyboba_user_stub_with_full_fields.registration_complete
