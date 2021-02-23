import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, List, Optional

import cv2


class Writer(ABC):
    approved_extensions: List[str]

    @classmethod
    @abstractmethod
    def write(cls, parsed_content: Any, location: Path, extension: str):
        pass


class ImageWriter(Writer):
    approved_extensions = ["jpg", "png", "jpeg"]

    @classmethod
    def write(cls, parsed_content: Any, location: Path, extension: str):
        success, buffer = cv2.imencode(f".{extension}", parsed_content)
        buffer.tofile(str(location))


class JsonWriter(Writer):
    approved_extensions = ["json"]

    @classmethod
    def write(cls, parsed_content: Any, location: Path, extension: str):
        with open(location, "w") as f:
            json.dump(parsed_content, f)


class CacheManager:
    writers = [ImageWriter, JsonWriter]
    writer_by_extension = {}

    for writer in writers:
        for supported_extension in writer.approved_extensions:
            writer_by_extension[supported_extension] = writer

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    def get_cached_location(self, tag: str) -> Path:
        return self.base_dir / tag

    def get(self, tag: str) -> Optional[bytes]:
        cached_location = self.get_cached_location(tag)
        if not cached_location.is_file():
            return None

        with open(cached_location, "rb") as f:
            file_content = f.read()

        return file_content

    def write(self, parsed_content: Any, tag: str, extension: str):
        cached_location = self.get_cached_location(tag)

        if extension not in self.writer_by_extension.keys():
            raise Exception("Extension not supported")
        self.writer_by_extension[extension].write(parsed_content, cached_location, extension)
