from typing import Tuple, List
from gspread import Cell

Defect = Tuple[str, int, str, str, str]

def from_irange(irange: List[Cell]) -> Defect:
    return (
        irange[0].value,
        int(irange[1].value),
        irange[2].value,
        irange[3].value,
        irange[4].value,
    )
