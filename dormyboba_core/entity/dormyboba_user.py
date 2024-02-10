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
        return DormybobaRole(
            role_id=api_role.role_id,
            role_name=api_role.role_name,
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
        return DormybobaUser(
            user_id=model_user.user_id,
            role=DormybobaRole.from_model(model_user.role),
            institute=Institute.from_model(model_user.institute),
            academic_type=AcademicType.from_model(model_user.academic_type),
            year=model_user.enroll_year,
            group=model_user.academic_group,
        )

    def to_model(self) -> model.DormybobaUser:
        return model.DormybobaUser(
            user_id=self.user_id,
            role=self.role.to_model(),
            institue=self.institute.to_model(),
            academic_type=self.academic_type.to_model(),
            year=self.year,
            group=self.group,
        )
