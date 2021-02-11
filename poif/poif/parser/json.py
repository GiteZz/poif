import json

from poif.parser.base import Parser


class JsonParser(Parser):
    approved_extensions = ["mapping", "json"]

    @staticmethod
    def parse(to_parse: bytes) -> dict:
        json_string = to_parse.decode("utf-8")

        return json.loads(json_string)
