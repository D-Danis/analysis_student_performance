#!/usr/bin/.venv python3
import sys
import logging

from app.cli import run


logging.basicConfig(level=logging.INFO)


def main() -> None:
    code = run()
    sys.exit(code)




if __name__ == '__main__':
    main()