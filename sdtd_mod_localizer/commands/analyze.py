from typing import List, Optional, Tuple

from ..entities import Localization
from .command import Command
from pathlib import Path


class Analyze(Command):
    def execute(self, arguments: List[str]):
        if len(arguments) == 0:
            path = self.get_data_path()
        else:
            path = self.get_path_from_arguments(arguments)

        if path is not None:
            self.analyze_localization_result(path)

    def analyze_localization_result(self, data_path: Path):

        total_english = 0
        total_japanese = 0
        for file in data_path.glob("**/Localization.txt"):
            localization = Localization(file)
            english_count, japanese_count = self._analyze_localization_file(
                localization)
            relative_path = file.relative_to(str(data_path))
            if english_count > 0:
                print("{}: E: {}, J: {}  Ratio: {}%".format(
                    str(relative_path), english_count, japanese_count,
                    round(japanese_count * 100 / english_count, 2)))
            total_english += english_count
            total_japanese += japanese_count

        if total_english > 0:
            print("\n\nTotal: E: {}, J: {}  Ratio: {}%".format(
                total_english, total_japanese,
                round(total_japanese * 100 / total_english, 2)))
        else:
            print("No translation")

    @staticmethod
    def _analyze_localization_file(
            localization: Localization) -> Tuple[int, int]:
        if not localization.is_localization_file \
                or not localization.has_english:
            return 0, 0

        english_count = 0
        japanese_count = 0
        for entry in localization.data:
            if entry is None:
                continue
            if "english" not in entry:
                continue
            english_text = entry["english"]

            english_count += 1
            if "japanese" in entry:
                japanese_text = entry["japanese"]
                if japanese_text != "" and japanese_text != english_text:
                    japanese_count += 1

        return english_count, japanese_count
