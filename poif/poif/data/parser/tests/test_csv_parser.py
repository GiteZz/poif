import tempfile

import pandas as pd
import pytest

from poif.data.parser.csv import CsvPandasParser


@pytest.fixture
def create_csv() -> pd.DataFrame:
    csv_data = {'Name': ['Dirk', 'Jos'], 'Age': [49, 30]}

    return pd.DataFrame(data=csv_data)


def test_correct_loading(create_csv):
    csv_file = tempfile.mkstemp(suffix='.csv}')[1]
    create_csv.to_csv(csv_file)
    read_csv = pd.read_csv(csv_file)

    with open(csv_file, 'rb') as f:
        file_bytes = f.read()

    parsed_df = CsvPandasParser.parse(file_bytes)

    # a = pd.DataFrame.compare(create_csv, parsed_df)
    assert read_csv.equals(parsed_df)