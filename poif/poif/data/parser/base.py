from abc import ABC, abstractmethod
from io import BytesIO
from typing import Any

from poif.data.parser.csv import CsvPandasParser
from poif.data.parser.image import ImageParser


class Parser(ABC):
    @staticmethod
    @abstractmethod
    def parse(bytes: BytesIO) -> Any:
        pass


class ParseMixin:
    parsers = [ImageParser, CsvPandasParser]
    parser_by_extension = {}

    for parser in parsers:
        for supported_extension in parser.approved_extensions:
            parser_by_extension[supported_extension] = parser

    def parse_file(self, file_bytes, extension):
        if extension not in self.parser_by_extension.keys():
            raise Exception('Extension not supported')
        return self.parser_by_extension[extension].parse(file_bytes)