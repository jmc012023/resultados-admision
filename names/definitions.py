from dataclasses import dataclass
from enum import Enum

@dataclass(frozen=True)
class WebPageContent:
    id_result: int
    periods: str
    test_type: str
    details: str
    link: str

class WPDataColumnNames(Enum):
    ID_RESULT = 'id_result'
    PERIODS = 'periods'
    DETAILS = 'details'

class ResultColumnNames(Enum):
    NAMES = "names"
    GRADE = "grade"
    CAREER = "career"
    STATUS = "status"
    DATE = "date"
    YEAR_PERIOD = "year_period"
    PERIOD = "period"
    TEST_TYPE = "test_type"
    MOD = "mod"
    PLACE = "place"
    LINK = "link"

class LinksDataColumnNames(Enum):
    ALL_RESULT = 'all_result'
    N_DF = 'n_df'

class GradesColumnNames(Enum):
    ONE = 'one'
    TWO = 'two'
    THREE = 'three'
    FOUR = 'four'
    FIVE = 'five'