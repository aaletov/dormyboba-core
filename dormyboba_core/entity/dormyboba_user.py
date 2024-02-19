from dataclasses import dataclass
from typing import Optional
import dormyboba_api.v1api_pb2 as apiv1
import dormyboba_api.v1api_pb2_grpc as apiv1grpc
from .institute import Institute
from .academic_type import AcademicType
from .. import model
from .. import entity

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
    institute: Optional[Institute]
    academic_type: Optional[AcademicType]
    year: Optional[int]
    group: Optional[str]
    is_registered: bool

    @staticmethod
    def from_api(api_user: apiv1.DormybobaUser) -> 'DormybobaUser':
        institute = None if not(api_user.HasField("institute")) else entity.Institute(
            institute_id=api_user.institute.institute_id,
            institute_name=None,
        )
        academic_type = None if not(api_user.HasField("academic_type")) else entity.AcademicType(
            type_id=api_user.academic_type.type_id,
            type_name=None,
        )
        year = None if not(api_user.HasField("year")) else api_user.year
        group = None if not(api_user.HasField("group")) else api_user.group
        return DormybobaUser(
            user_id=api_user.user_id,
            role=DormybobaRole.from_api(api_user.role),
            institute=institute,
            academic_type=academic_type,
            year=year,
            group=group,
            is_registered=api_user.is_registered,
        )

    def to_api(self) -> apiv1.DormybobaUser:
        api_institute = None if self.institute is None else self.institute.to_api()
        api_academic_type = None if self.academic_type is None else self.academic_type.to_api()
        return apiv1.DormybobaUser(
            user_id=self.user_id,
            role=self.role.to_api(),
            institute=api_institute,
            academic_type=api_academic_type,
            year=self.year,
            group=self.group,
            is_registered=self.is_registered,
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
            is_registered=model_user.registration_complete,
        )

    def to_model(self) -> model.DormybobaUser:
        institute_id = None
        if self.institute is not None:
            institute_id = self.institute.to_model().institute_id

        academic_type_id = None
        if self.academic_type is not None:
            academic_type_id = self.academic_type.to_model().type_id

        return model.DormybobaUser(
            user_id=self.user_id,
            role_id=self.role.role_id,
            institute_id=institute_id,
            academic_type_id=academic_type_id,
            enroll_year=self.year,
            academic_group=self.group,
            registration_complete=self.is_registered,
        )
