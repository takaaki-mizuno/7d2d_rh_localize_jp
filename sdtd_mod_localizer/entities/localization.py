import csv
from collections import OrderedDict
from pathlib import Path
from typing import List, Optional
from typing import OrderedDict as OrderedDictType


class Localization(object):
    def __init__(self, path: Path):
        self._data: List[Optional[OrderedDictType[str, str]]] = []
