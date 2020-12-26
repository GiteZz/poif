from io import BytesIO

import pandas as pd

from poif.data.cache.base import Parser


class CsvPandasParser(Parser):
    approved_extensions = ['csv']
    @staticmethod
    def parse(to_parse: bytes) -> pd.DataFrame:
        df = pd.read_csv(BytesIO(to_parse))

        return df
