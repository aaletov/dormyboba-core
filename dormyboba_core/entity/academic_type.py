from typing import Optional
from dataclasses import dataclass
import dormyboba_api.v1api_pb2 as apiv1
import dormyboba_api.v1api_pb2_grpc as apiv1grpc

from .. import model

@dataclass
class AcademicType:
    type_id: int
    type_name: Optional[str]

    @staticmethod
    def from_api(api_academic_type: apiv1.AcademicType) -> 'AcademicType':
        type_name = None
        if api_academic_type.type_name != "":
            type_name = api_academic_type.type_name
        return AcademicType(
            type_id=api_academic_type.type_id,
            type_name=type_name,
        )
    
    def to_api(self) -> apiv1.AcademicType:
        return apiv1.AcademicType(
            type_id=self.type_id,
            type_name=self.type_name,
        )
    
    @staticmethod
    def from_model(model_academic_type: model.AcademicType) -> 'AcademicType':
        return AcademicType(
            type_id=model_academic_type.type_id,
            type_name=model_academic_type.type_name,
        )
    
    def to_model(self) -> model.AcademicType:
        return model.AcademicType(
            type_id=self.type_id,
            type_name=self.type_name,
        )
