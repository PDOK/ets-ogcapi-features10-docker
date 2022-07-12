#!/bin/env python3
import argparse
import sys
from pathlib import Path

from junitparser import JUnitXml

def parse_args():
    parser = argparse.ArgumentParser(description='parse junit result.')
    parser.add_argument('result_dir', type=str, help='result dir')
    parser.add_argument('--exit-on-fail', dest='exit_on_fail', action='store_true')

    args = parser.parse_args()
    return args


def main(root_dir, exit_on_fail):
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

    print("\n".join(failed_cases))
    if failed_cases and exit_on_fail:
        sys.exit(1)


if __name__ == "__main__":
    args = parse_args()
    result_dir = args.result_dir
    exit_on_fail = args.exit_on_fail
    main(result_dir, exit_on_fail)
