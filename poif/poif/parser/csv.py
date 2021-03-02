from io import BytesIO

from pandas import DataFrame, read_csv

from poif.parser.base import Parser


class CsvPandasParser(Parser):
    approved_extensions = ["csv"]

    @staticmethod
    def parse(to_parse: bytes) -> DataFrame:
        df = read_csv(BytesIO(to_parse))

        return df
