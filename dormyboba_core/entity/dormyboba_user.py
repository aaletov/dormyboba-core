from dataclasses import dataclass
import dormyboba_api.v1api_pb2 as apiv1
import dormyboba_api.v1api_pb2_grpc as apiv1grpc
from .institute import Institute
from .academic_type import AcademicType
from .. import model

@dataclass
class DormybobaRole:
    role_id: int
    role_name: str

    @staticmethod
    def from_api(api_role: apiv1.DormybobaRole) -> 'DormybobaRole':
        role_name = None if api_role.role_name == "" else api_role.role_name
        return DormybobaRole(
            role_id=api_role.role_id,
            role_name=role_name,
        )
    
    def to_api(self) -> apiv1.DormybobaRole:
        return apiv1.DormybobaRole(
            role_id=self.role_id,
            role_name=self.role_name,
        )

    @staticmethod
    def from_model(model_role: apiv1.DormybobaRole) -> 'DormybobaRole':
        return DormybobaRole(
            role_id=model_role.role_id,
            role_name=model_role.role_name,
        )

    def to_model(self) -> model.DormybobaRole:
        return model.DormybobaRole(
            role_id=self.role_id,
            role_name=self.role_name,
        )

@dataclass
class DormybobaUser:
    user_id: int
    role: DormybobaRole
    institute: Institute
    academic_type: AcademicType
    year: int
    group: str

    @staticmethod
    def from_api(api_user: apiv1.DormybobaUser) -> 'DormybobaUser':
        return DormybobaUser(
            user_id=api_user.user_id,
            role=DormybobaRole.from_api(api_user.role),
            institute=Institute.from_api(api_user.institute),
            academic_type=AcademicType.from_api(api_user.academic_type),
            year=api_user.year,
            group=api_user.group,
        )
    
    def to_api(self) -> apiv1.DormybobaUser:
        return apiv1.DormybobaUser(
            user_id=self.user_id,
            role=self.role.to_api(),
            institute=self.institute.to_api(),
            academic_type=self.academic_type.to_api(),
            year=self.year,
            group=self.group,
        )
    
    @staticmethod
    def from_model(model_user: model.DormybobaUser) -> 'DormybobaUser':
        model_role = None
        if model_user.role is not None:
            model_role=DormybobaRole.from_model(model_user.role)
        
        model_institute = None
        if model_user.institute is not None:
            model_institute = Institute.from_model(model_user.institute)
        
        model_academic_type = None
        if model_user.academic_type is not None:
            model_academic_type = AcademicType.from_model(model_user.academic_type)
        
        return DormybobaUser(
            user_id=model_user.user_id,
            role=model_role,
            institute=model_institute,
            academic_type=model_academic_type,
            year=model_user.enroll_year,
            group=model_user.academic_group,
        )

    def to_model(self) -> model.DormybobaUser:
        return model.DormybobaUser(
            user_id=self.user_id,
            role_id=self.role.role_id,
            institute_id=self.institute.institute_id,
            academic_type_id=self.academic_type.type_id,
            enroll_year=self.year,
            academic_group=self.group,
        )
