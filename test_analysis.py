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

@pytest.mark.parametrize("date,expected", [
    ("01/01/2018 00:00", "2018-01-01 00:00"),
    ("12/31/2022 23:00", "2022-12-31 23:00"),
])
def test_load_data(tmp_path, date, expected):
    path = tmp_path / "sample.csv"
    path.write_text(
        f"DATE,VCAR,\n{date},2.5,\n"
    )

    result = main.load_data(path)

    assert result.index[0] == pd.Timestamp(expected)
    assert result["VCAR"].iloc[0] == 2.5
    assert result.columns.tolist() == ["VCAR"]