import shutil
from pathlib import Path
from typing import List, Optional

from .command import Command


class Generate(Command):
    def execute(self, arguments: List[str]):
        path = self.get_path_from_arguments(arguments)
        if path is None:
            return
        self.copy_localized_text(path)

    def copy_localized_text(self, original_path: Path):
        data_path = self.get_data_path()
        for file in original_path.glob("**/Localization.txt"):
            relative_path = file.relative_to(str(original_path))
            destination_path = data_path.joinpath(relative_path)
            if not destination_path.parent.exists():
                destination_path.parent.mkdir(parents=True)
            shutil.copy(file, destination_path)
            print("Copy: {}".format(str(relative_path)))
