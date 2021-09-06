import sys
from pathlib import Path
from typing import List, Optional


class Command(object):
    def execute(self, arguments: List[str]):
        raise NotImplemented

    @staticmethod
    def get_data_path() -> Path:
        return Path("./data/Mods")
