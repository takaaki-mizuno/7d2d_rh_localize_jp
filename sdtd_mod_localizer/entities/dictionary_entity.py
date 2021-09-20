from typing import List


class DirectoryEntity(object):
    def __init__(self, english: str, japanese: str, keys: List[str]):
        self._english = english
        self._japanese = japanese
        self._keys = keys

    @property
    def english(self) -> str:
        return self._english

    @property
    def japanese(self) -> str:
        return self._japanese

    @property
    def keys(self) -> List[str]:
        return self._keys

    def add_keys(self, keys: List[str]):
        self._keys.extend(keys)

    def update_japanese(self, japanese: str):
        if japanese != "":
            self._japanese = japanese

    def to_csv(self)->str:
        return '"{}","{}",{}'.format(self.english, self.japanese, ",".join(self.keys))
