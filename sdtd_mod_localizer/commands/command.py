from pathlib import Path
from typing import List


class Command(object):
    def execute(self, arguments: List[str]):
        raise NotImplementedError

    @staticmethod
    def get_data_path() -> Path:
        return Path("./data/Mods")
