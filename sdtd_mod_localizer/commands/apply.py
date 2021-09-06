import shutil
from pathlib import Path
from typing import List, Optional

from .command import Command


class Apply(Command):
    def execute(self, arguments: List[str]):
        path = self.get_target_path_from_arguments(arguments)
        if path is None:
            return
        self.copy_localized_text(path)

    @staticmethod
    def get_target_path_from_arguments(arguments: List[str]) -> Optional[Path]:
        if len(arguments) == 0:
            print("Please provide your 7dtd path")
            return None

        mod_path = Path(arguments[0])
        if not mod_path.exists():
            print("Provided path does not exist. : {}".format(str(mod_path)))
            return None

        path = mod_path.joinpath("Mods")
        if not path.exists():
            print("Provided path seems not has  a Mod directory. : {}".format(
                str(mod_path)))
            return None

        return path

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
                "Game data file is not consistent. Your mod version may be different from this localized files"
            )
            return

        for file in data_path.glob("**/Localization.txt"):
            relative_path = file.relative_to(str(data_path))
            destination_path = game_path.joinpath(relative_path)
            shutil.copy(file, destination_path)
            print("Copy: {}".format(str(relative_path)))
