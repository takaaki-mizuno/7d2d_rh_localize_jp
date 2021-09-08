import csv
from collections import OrderedDict
from pathlib import Path
from typing import List, Optional
from typing import OrderedDict as OrderedDictType


class Localization(object):
    def __init__(self, path: Path):
        self._is_localization_file: bool = False
        self._path: Path = path
        self._header: List[str] = []
        self._normalized_header: List[str] = []
        self._data: List[Optional[OrderedDictType[str, str]]] = []
        self._parse_file()

    def _parse_file(self):
        raw_text = self._path.read_text(encoding="utf-8")
        text_lines = raw_text.split("\n")
        if len(text_lines) <= 1:
            self._is_localization_file = False
            return

        self._is_localization_file = True
        self._header = list(csv.reader([text_lines[0]]))[0]
        self._normalized_header = [header.lower() for header in self._header]

        bodies = text_lines[1:]

        self._data = []
        for body_text in bodies:
            if body_text == "":
                self._data.append(None)
                continue

            body = list(csv.reader([body_text]))[0]
            if len(body) == 1:
                self._data.append(None)
                continue

            data = OrderedDict()
            for index, header in enumerate(self._header):
                normalized_header = header.lower()
                if len(body) > index:
                    data[normalized_header] = body[index]
                else:
                    data[normalized_header] = ""

            self._data.append(data)

    @property
    def is_localization_file(self):
        return self._is_localization_file

    @property
    def has_english(self) -> True:
        return "english" in self._normalized_header

    @property
    def has_japanese(self) -> True:
        return "japanese" in self._normalized_header

    @property
    def data(self) -> List[Optional[OrderedDictType[str, str]]]:
        return self._data

    @property
    def header(self) -> List[str]:
        return self._header

    @property
    def normalized_header(self) -> List[str]:
        return self._normalized_header
