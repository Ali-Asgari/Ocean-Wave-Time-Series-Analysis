import pandas as pd
import pytest
import main

@pytest.mark.parametrize("start,end,expected", [
    ("2018-01-01", "2023-01-01", [2, 3]),
    ("2018-01-01", "2022-12-31", [2]),
    ("2023-01-01", "2024-01-01", [4]),
    ("2024-01-01", "2025-01-01", []),
    ("2016-01-01", "2017-12-31", []),
])
def test_filter_dates(start, end, expected):
    dates = pd.to_datetime([ "2017-12-31", "2018-01-01", "2022-12-31", "2023-01-01"])
    df = pd.DataFrame({"wave": [1, 2, 3, 4]}, index=dates)
    result = main.filter_dates(df, start, end)
    assert result["wave"].tolist() == expected