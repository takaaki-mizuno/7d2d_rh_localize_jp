import sys

from commands import Generate


def manage():
    if len(sys.argv) < 2:
        print("command name required")
        return

    command = sys.argv[1]
    if command == "generate":
        Generate().execute(sys.argv[2:])


if __name__ == '__main__':
    manage()
