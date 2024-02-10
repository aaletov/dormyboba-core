from typing import Dict
from dataclasses import dataclass
from enum import Enum
import random
import dormyboba_api.v1api_pb2 as apiv1
from .. import model

class DefectType(Enum):
    ELECTRICITY = 0
    PLUMB = 1
    COMMON = 2

    @staticmethod
    def _get_api_to_entity_map() -> Dict[apiv1.DefectType, 'DefectType']:
        return {
            apiv1.ELECTRICITY: DefectType.ELECTRICITY,
            apiv1.PLUMB: DefectType.PLUMB,
            apiv1.COMMON: DefectType.COMMON,
        }

    @staticmethod
    def _get_entity_to_api_map() -> Dict['DefectType', apiv1.DefectType]:
        return {v: k for k, v in DefectType._get_api_to_entity_map.items()}

    @staticmethod
    def from_api(api_type: apiv1.DefectType) -> 'DefectType':
        return DefectType._get_api_to_entity_map()[api_type]

    def to_api(self) -> apiv1.DefectType:
        _TYPE_ENTITY_TO_API: Dict[DefectType, apiv1.DefectType] = {
            DefectType.ELECTRICITY: apiv1.ELECTRICITY,
            DefectType.PLUMB: apiv1.PLUMB,
            DefectType.COMMON: apiv1.COMMON,
        }
        return _TYPE_ENTITY_TO_API[self.value]
    
    @staticmethod
    def _get_model_to_entity_map() -> Dict[str, 'DefectType']:
        return {
            "Электрика": DefectType.ELECTRICITY,
            "Сантехника": DefectType.PLUMB,
            "Общее": DefectType.COMMON,
        }
    
    @staticmethod
    def _get_entity_to_model_map() -> Dict['DefectType', str]:
        return {v: k for k, v in DefectType._get_model_to_entity_map.items()}
    
    @staticmethod
    def from_model(model_type: str) -> 'DefectType':
        return DefectType._get_model_to_entity_map()[model_type]
        
    def to_model(self) -> str:
        return DefectType._get_entity_to_model_map()[self.value]

class DefectStatus(Enum):
    CREATED = 0
    ACCEPTED = 1
    RESOLVED = 2

    @staticmethod
    def _get_api_to_entity_map() -> Dict[apiv1.DefectStatus, 'DefectStatus']:
        return {
            apiv1.CREATED: DefectStatus.CREATED,
            apiv1.ACCEPTED: DefectStatus.ACCEPTED,
            apiv1.RESOLVED: DefectStatus.RESOLVED,
        }
    
    @staticmethod
    def _get_entity_to_api_map() -> Dict['DefectStatus', apiv1.DefectStatus]:
        return {v: k for k, v in DefectStatus._get_api_to_entity_map.items()}

    @staticmethod
    def from_api(api_type: apiv1.DefectStatus) -> 'DefectStatus':
        return DefectStatus._get_api_to_entity_map()[api_type]

    def to_api(self) -> apiv1.DefectStatus:
        return DefectStatus._get_entity_to_api_map()[self.value]
    
    @staticmethod
    def _get_model_to_entity_map() -> Dict[str, 'DefectStatus']:
        return {
            "Добавлено": DefectStatus.CREATED,
            "Принято": DefectStatus.ACCEPTED,
            "Решено": DefectStatus.RESOLVED,
        }
    
    @staticmethod
    def _get_entity_to_model_map() -> Dict['DefectStatus', str]:
        return {v: k for k, v in DefectStatus._get_model_to_entity_map.items()}
    
    @staticmethod
    def from_model(model_type: str) -> 'DefectStatus':
        return DefectStatus._get_model_to_entity_map()[model_type]
        
    def to_model(self) -> str:
        return DefectStatus._get_entity_to_model_map()[self.value]

@dataclass
class Defect:
    defect_id: str
    user_id: int
    defect_type: DefectType
    description: str
    defect_status: DefectStatus

    def __init__(
        self,
        user_id: int,
        defect_type: DefectType,
        description: str,
        defect_status: DefectStatus, 
    ):
        self.defect_id = "DD" + str(random.randint(1000, 9999))
        self.user_id = user_id
        self.defect_type = defect_type
        self.description = description
        self.defect_status = defect_status

    @staticmethod
    def from_api(api_defect: apiv1.Defect) -> 'Defect':
        return Defect(
            defect_id=api_defect.defect_id,
            user_id=api_defect.user_id,
            defect_type=DefectType.from_api(api_defect.defect_type),
            description=api_defect.description,
            defect_status=DefectStatus.from_api(api_defect.defect_status),
        )

    def to_api(self) -> apiv1.Defect:
        return apiv1.Defect(
            defect_id=self.defect_id,
            user_id=self.user_id,
            defect_type=self.defect_type.to_api(),
            description=self.description,
            defect_status=self.defect_status.to_api(),
        )
    
    @staticmethod
    def from_model(model_defect: model.Defect) -> 'Defect':
        defect = Defect(
            user_id=model_defect[1],
            defect_type=DefectType.from_model(model_defect[2]),
            description=model_defect[3],
            defect_status=DefectStatus.from_model(model_defect[4])
        )
        defect.defect_id = model_defect[0]
        return defect
    
    def to_model(self) -> model.Defect:
        return (
            self.defect_id,
            self.user_id,
            self.defect_type.to_model(),
            self.description,
            self.defect_status.to_model(),
        )
