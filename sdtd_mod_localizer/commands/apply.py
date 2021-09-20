import shutil
from pathlib import Path
from typing import List, Optional

from .command import Command
from ..entities import Dictionary, Localization

import csv


class Apply(Command):
    def execute(self, arguments: List[str]):
        path = self.get_path_from_arguments(arguments)
        if path is None:
            return
        #        self.copy_localized_text(path)
        localizations = self._generate_localizations(path)
        self._store_localization_data(path, localizations)

    def _generate_localizations(self, game_path: Path) -> List[List[str]]:
        dictionary = self._load_dictionary()
        localizations = [["Key", "japanese"]]
        files = sorted(game_path.glob("**/Localization.txt"), key=lambda x: str(x))

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
                entity = dictionary.get_entity(english_text)
                if entity is None:
                    continue
                if entity.japanese != "":
                    if "japanese" in entry and entity.japanese == entry["japanese"]:
                        continue
                    if "japanese" in entry:
                        print(entity.japanese, entry["japanese"])
                    localizations.append([key, entity.japanese])

        return localizations

    def _load_dictionary(self) -> Dictionary:
        data_path = self.get_data_path(directory="localizations").joinpath("localizations.txt")
        return Dictionary(path=data_path)

    def _store_localization_data(self, game_path: Path, localizations: List[List[str]]):
        target_mod_path = game_path.joinpath("zzz_AutoLocalizationJP")
        if not target_mod_path.exists():
            target_mod_path.mkdir()

        templates_path = self.get_data_path(directory="templates")
        shutil.copy(templates_path.joinpath("ModInfo.xml"), target_mod_path.joinpath("ModInfo.xml"))
        mod_config_path = target_mod_path.joinpath("Config")
        if not mod_config_path.exists():
            mod_config_path.mkdir()
        localization_file_path = mod_config_path.joinpath("Localization.txt")
        with localization_file_path.open("w", encoding="utf-8") as handler:
            writer = csv.writer(handler, lineterminator='\r\n', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerows(localizations)

    def copy_localized_text(self, game_path: Path):
        data_path = self.get_data_path()
        error = False
        for file in data_path.glob("**/Localization.txt"):
            relative_path = file.relative_to(str(data_path))
            destination_path = game_path.joinpath(relative_path)
            if not destination_path.exists():
                print("File does not exists: {}".format(str(destination_path)))
                error = True

        if error:
            print(
                "Game data file is not consistent."
                + "Your mod version may be different from this localized files"
            )
            return

        for file in data_path.glob("**/Localization.txt"):
            relative_path = file.relative_to(str(data_path))
            destination_path = game_path.joinpath(relative_path)
            shutil.copy(file, destination_path)
            print("Copy: {}".format(str(relative_path)))
