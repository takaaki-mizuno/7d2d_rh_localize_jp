import shutil
from pathlib import Path
from typing import List, Optional

from .command import Command


class Generate(Command):
    def execute(self, arguments: List[str]):
        path = self.get_mod_path_from_arguments(arguments)
        if path is None:
            return
        self.copy_localized_text(path)

    @staticmethod
    def get_mod_path_from_arguments(arguments: List[str]) -> Optional[Path]:
        if len(arguments) == 0:
            print("Please provide original mod path")
            return None

        mod_path = Path(arguments[0])
        if not mod_path.exists():
            print("Provided path does not exist. : {}".format(str(mod_path)))
            return None

        path = mod_path.joinpath("Mods")
        if not path.exists():
            print("Provided path seems not a mod directory. : {}".format(
                str(mod_path)))
            return None

        return path

    @staticmethod
    def copy_localized_text(original_path: Path):
        data_path = Path("./data/Mods").absolute()
        for file in original_path.glob("**/Localization.txt"):
            relative_path = file.relative_to(str(original_path))
            destination_path = data_path.joinpath(relative_path)
            if not destination_path.parent.exists():
                destination_path.parent.mkdir(parents=True)
            shutil.copy(file, destination_path)
            print("Copy: {}".format(str(relative_path)))
