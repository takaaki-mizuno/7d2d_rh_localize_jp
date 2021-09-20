import csv
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List, Optional, Union
from typing import OrderedDict as OrderedDictType
from .dictionary_entity import DirectoryEntity
from collections import OrderedDict


class Dictionary(object):
    def __init__(self, path: Path):
        self._is_dictionary_file: bool = False
        self._path: Path = path
        self._data: OrderedDictType[str, DirectoryEntity] = OrderedDict()
        self._parse_file()

    def _parse_file(self):
        if not self._path.exists():
            return

        raw_text = self._path.read_text(encoding="utf-8")
        text_lines = raw_text.split("\n")
        if len(text_lines) <= 1:
            self._is_dictionary_file = False
            return

        self._data = OrderedDict()
        for body_text in text_lines:
            if body_text == "":
                continue

            body = list(csv.reader([body_text]))[0]
            if len(body) == 1:
                continue

            english = body[0]
            japanese = body[1]
            keys = body[2:]

            self.add_entity(english=english, japanese=japanese, keys=keys)

    def get_entity(self, english: str) -> Optional[DirectoryEntity]:
        if english in self._data:
            return self._data[english]

        return None

    def add_entity(self, english: str, japanese: str, keys: Union[List[str], str]):
        if english in self._data:
            entity = self._data[english]
            entity.update_japanese(japanese)
            entity.add_keys(keys)
        else:
            entity = DirectoryEntity(english=english, japanese=japanese, keys=keys)
            self._data[english] = entity

    def save(self):
        csv_data = []
        for key in self._data.keys():
            csv_data.append(self._data[key].to_csv())

        self._path.write_text("\n".join(csv_data) + "\n")
