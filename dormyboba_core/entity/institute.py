from dataclasses import dataclass
import dormyboba_api.v1api_pb2 as apiv1
import dormyboba_api.v1api_pb2_grpc as apiv1grpc

from .. import model

@dataclass
class Institute:
    institute_id: int
    institute_name: str

    @staticmethod
    def from_api(api_institute: apiv1.Institute) -> 'Institute':
        return Institute(
            institute_id=api_institute.institute_id,
            institute_name=api_institute.institute_name,
        )
    
    def to_api(self) -> apiv1.Institute:
        return apiv1.Institute(
            institute_id=self.institute_id,
            institute_name=self.institute_name,
        )

    @staticmethod
    def from_model(model_institute: model.Institute) -> 'Institute':
        return Institute(
            institute_id=model_institute.institute_id,
            institute_name=model_institute.institute_name,
        )
    
    def to_model(self) -> model.Institute:
        return model.Institute(
            institute_id=self.institute_id,
            institute_name=self.institute_name,
        )
