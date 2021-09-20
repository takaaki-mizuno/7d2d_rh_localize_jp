from pathlib import Path
from typing import List, Optional


class Command(object):
    def execute(self, arguments: List[str]):
        raise NotImplementedError

    @staticmethod
    def get_data_path(directory: str = "Mods") -> Path:
        return Path("./data").joinpath(directory)

    @staticmethod
    def get_path_from_arguments(arguments: List[str]) -> Optional[Path]:
        if len(arguments) == 0:
            print("Please provide path as a first argument")
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
