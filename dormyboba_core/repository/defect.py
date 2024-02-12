from typing import Optional, List
import abc
from gspread import Cell, Worksheet
import dormyboba_api.v1api_pb2 as apiv1
from .. import model
from .. import entity

class DefectRepository(metaclass=abc.ABCMeta):
    """An interface to dormyboba repository"""

    @abc.abstractmethod
    def add(self, defect: entity.Defect) -> entity.Defect:
        raise NotImplementedError()
    
    @abc.abstractmethod
    def getById(self) -> Optional[entity.Defect]:
        raise NotImplementedError()
    
    @abc.abstractmethod
    def update(self, defect: entity.Defect) -> entity.Defect:
        raise NotImplementedError()

class GsheetDefectRepository(DefectRepository):
    """Gsheet implementation of dormyboba user repository"""
    
    def __init__(self, worksheet: Worksheet):
        self.worksheet = worksheet

    def add(self, defect: entity.Defect) -> entity.Defect:
        column = self.worksheet.col_values(1)
        i = len(column) + 1
        if None in column:
            i = column.index(None) + 1
        irange: List[Cell] = self.worksheet.range(i, 1, i+4, 5)

        values = defect.to_model()
        for cell, value in zip(irange, values):
            cell.value = value

        self.worksheet.update_cells(irange)
        return defect
    
    def getById(self, defect_id: str) -> Optional[entity.Defect]:
        column = self.worksheet.col_values(1)
        if defect_id not in column:
            return None

        i = column.index(defect_id) + 1
        irange: List[Cell] = self.worksheet.range(i, 1, i+4, 5)
        model_defect = model.from_irange(irange)
        return entity.Defect.from_model(model_defect)
    
    def update(self, defect: entity.Defect) -> entity.Defect:
        column = self.worksheet.col_values(1)
        if defect.defect_id not in column:
            raise ValueError("defect does not exist")

        i = column.index(defect.defect_id) + 1
        irange: List[Cell] = self.worksheet.range(i, 1, i+4, 5)

        values = defect.to_model()
        for cell, value in zip(irange, values):
            cell.value = value

        self.worksheet.update_cells(irange)
        return defect
