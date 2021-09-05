import sys
from typing import List, Optional


class Command(object):
    def execute(self, arguments: List[str]):
        raise NotImplemented

    def get_argument(self, index: int) -> Optional[str]:
        if len(sys.argv) < index:
            return None
        if index < 0:
            return None

        return sys.argv[index - 1]
