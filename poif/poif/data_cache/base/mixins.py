from poif.data_cache.base.parsers.csv import CsvPandasParser
from poif.data_cache.base.parsers.image import ImageParser


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