#!/bin/env python3
import argparse
import sys
from pathlib import Path

from junitparser import JUnitXml

def parse_args():
    parser = argparse.ArgumentParser(description='parse junit result.')
    parser.add_argument('result_dir', type=str, help='result dir')
    args = parser.parse_args()
    return args.result_dir


def main(root_dir):
    dir_path = Path(root_dir)
    if not dir_path.exists():
        print(f"test dir '{root_dir}' should exist")
        sys.exit(1)

    failed_cases = []

    for junit_test in dir_path.glob("**/**/TEST-org.opengis.cite.*.xml"):
        test_xml = JUnitXml.fromfile(str(junit_test))
        failed = [case.message for suite in test_xml for case in suite if case.type == "java.lang.Throwable"]
        if failed:
            failed_cases += [f"### {test_xml.name}"] + failed + [""]

    if failed_cases:
        print("\n".join(failed_cases))
        sys.exit(1)


if __name__ == "__main__":
    result_dir = parse_args()
    main(result_dir)
