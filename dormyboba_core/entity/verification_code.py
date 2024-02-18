from __future__ import annotations
from dataclasses import dataclass
import dormyboba_api.v1api_pb2 as apiv1
from .dormyboba_user import DormybobaRole
from .. import model

@dataclass
class VerificationCode:
    verification_code: int
    role: DormybobaRole

    @staticmethod
    def from_model(model_code: model.VerificationCode) -> 'VerificationCode':
        return VerificationCode(
            verification_code=model_code.code,
            role=DormybobaRole.from_model(model_code.role),
        )
    
    def to_model(self) -> model.VerificationCode:
        return model.VerificationCode(
            code=self.verification_code,
            role_id=self.role.role_id,
        )