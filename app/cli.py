import argparse
import sys
from typing import List

from app.reader import CSVReader
from app.datastore import DataStore
from app.reports.registry import ReportFactory
from app.errors import AppError


def parse_args(argv: List[str]|None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate reports from CSV files")
    parser.add_argument("--files", nargs="+", required=True, help="CSV files")
    parser.add_argument("--report", required=True, help="Report name \
                        (student-performance, teacher-performance, subject-performance)")
    parser.add_argument("--precision", type=int, default=2, help="Decimal precision for averages")
    parser.add_argument("--top", type=int, default=None, help="Show top N entries (optional)")
    return parser.parse_args(argv)


def run(argv: List[str]|None = None) -> int:
    args = parse_args(argv)
    try:
        reader = CSVReader(args.files)
        datastore = DataStore()
        datastore.add_records(reader)
        # передаём precision и top в фабрику отчётов
        extra = {}
        if args.precision is not None:
            extra["precision"] = args.precision
        if args.top is not None:
            extra["top"] = args.top
        report = ReportFactory.create(args.report, datastore, **extra)
        
        report.build()
        print(report.render())
        return 0
    except AppError as exc:
        print(f"Error {getattr(exc, 'code', '')} {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"Unexpected error: {exc}", file=sys.stderr)
        return 1
    
    # report = createreport(args.report, datastore)
    # except AppError as exc:
    #     # централизованная обработка ошибок приложения
    #     print(f"Error: {exc}", file=sys.stderr)
    #     return 2
    # except Exception as exc:
    #     print(f"Unexpected error: {exc}", file=sys.stderr)
    #     return 1