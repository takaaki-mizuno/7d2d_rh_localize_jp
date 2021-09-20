from typing import List, Optional, Tuple

from ..entities import Localization, Dictionary
from .command import Command
from pathlib import Path

from collections import OrderedDict


class Extract(Command):
    def execute(self, arguments: List[str]):
        path = self.get_path_from_arguments(arguments)
        if path is None:
            return

        dictionary = self._extract_texts(path)
        dictionary.save()

    def _extract_texts(self, path: Path) -> Dictionary:
        dictionary = self._load_exiting_data()

        files = sorted(path.glob("**/Localization.txt"), key=lambda x: str(x))
        for file in files:
            localization = Localization(file)
            for entry in localization.data:
                if entry is None:
                    continue
                if "english" not in entry:
                    continue
                english_text = entry["english"]
                if english_text == "":
                    continue
                key = entry["key"]
                if "japanese" in entry and entry["japanese"] != "":
                    japanese_text = entry["japanese"]
                else:
                    japanese_text = ""
                dictionary.add_entity(english=english_text, japanese=japanese_text, keys=[key])

        return dictionary

    def _load_exiting_data(self) -> Dictionary:
        data_path = self.get_data_path(directory="localizations").joinpath("localizations.txt")
        return Dictionary(path=data_path)
