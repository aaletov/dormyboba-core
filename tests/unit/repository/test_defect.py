import unittest
from unittest.mock import Mock
from dormyboba_core import entity
from dormyboba_core.entity.defect import DefectStatus, DefectType
from gspread import Worksheet
from dormyboba_core.repository import GsheetDefectRepository
from dormyboba_core.entity import Defect

class TestGsheetDefectRepository(unittest.TestCase):

    def setUp(self):
        self.mock_worksheet = Mock(spec=Worksheet)
        self.repository = GsheetDefectRepository(self.mock_worksheet)

    def test_update_nonexistent_defect(self):
        defect = Defect(
            defect_id='1',
            user_id=1,
            description='sample desc',
            defect_type=DefectType.ELECTRICITY,
            defect_status=DefectStatus.CREATED,
        )
        self.mock_worksheet.col_values.return_value = [['1', 2, '3', '4', '5']]
        self.mock_worksheet.range.return_value = [['1', 2, '3', '4', '5']]
        with self.assertRaises(ValueError):
            self.repository.update(defect)

    def test_get_defect_by_nonexistent_id(self):
        self.mock_worksheet.col_values.return_value = [['1', 2, '3', '4', '5']]
        result = self.repository.getById('10')
        self.assertIsNone(result)

