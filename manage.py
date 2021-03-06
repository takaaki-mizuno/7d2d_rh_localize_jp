import sys

from sdtd_mod_localizer.commands import Analyze, Apply, Extract, Generate


def manage():
    if len(sys.argv) < 2:
        print("command name required")
        return

    command = sys.argv[1]
    if command == "generate":
        Generate().execute(sys.argv[2:])
    elif command == "apply":
        Apply().execute(sys.argv[2:])
    elif command == "analyze":
        Analyze().execute(sys.argv[2:])
    elif command == "extract":
        Extract().execute(sys.argv[2:])


if __name__ == '__main__':
    manage()
