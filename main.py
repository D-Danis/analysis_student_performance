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
    
    
# python3 main.py --file students1.csv students2.csv --report student-performance 
# python3 main.py --file students1.csv students2.csv --report subject-performance --precision 3
# python3 main.py --file students1.csv students2.csv --report teacher-performance --top 5
