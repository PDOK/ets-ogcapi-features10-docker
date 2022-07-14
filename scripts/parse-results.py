#!/bin/env python3
import argparse

from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import print
from junitparser import JUnitXml, Failure, Error


err_console = Console(stderr=True)
console = Console()
failed_table = Table(show_lines=True)
skipped_table = Table(show_lines=True)


def main(result_dir, service_url, pretty_print, exit_on_fail):
    """
    Parse junit result.
    """

    failed_cases = []
    failed_tuples = []

    skipped_cases = []
    skipped_tuples = []

    dir_path = Path(args.result_dir)
    for junit_test in dir_path.glob("**/**/TEST-org.opengis.cite.*.xml"):
        test_xml = JUnitXml.fromfile(str(junit_test))

        failed = [case for suite in test_xml for case in suite if type(case) is Failure]
        failed_message = [case.message for case in failed]
        failed_tuples += [
            (junit_test.name, test_xml.name, case.message) for case in failed
        ]
        if failed:
            failed_cases += [f"### {test_xml.name}"] + failed_message + [""]

        skipped = [case for suite in test_xml for case in suite if type(case) is Error]
        skipped_message = [case.message for case in skipped]
        skipped_tuples += [
            (junit_test.name, test_xml.name, case.message) for case in skipped
        ]
        if skipped:
            skipped_cases += [f"### {test_xml.name}"] + skipped_message + [""]

    if pretty_print:
        console.print("ogcapi-features-1.0-1.4 Test Suite Run", style="bold italic underline", justify="center")
        console.print(f"\nOutput test run saved in '{result_dir}'\n",  justify="center")

        if service_url:
            console.print(f"\nTest instance '{service_url}'\n",  justify="center")

        failed_table.add_column(
            "Case Name", justify="right", style="cyan", no_wrap=False, overflow="fold"
        )
        failed_table.add_column(
            "Error", justify="right", style="red", no_wrap=False, overflow="fold"
        )
        failed_table.add_column(
            "File", justify="right", style="magenta", no_wrap=False, overflow="fold"
        )
        for case in failed_tuples:
            failed_table.add_row(case[1], case[2], str(case[0]))

        failed_table.title = f"FAILED TEST CASES ({len(failed_tuples)})"
        console.print(failed_table)

        skipped_table.add_column(
            "Case Name", justify="right", style="cyan", no_wrap=False, overflow="fold"
        )
        skipped_table.add_column(
            "Error", justify="right", style="yellow", no_wrap=False, overflow="fold"
        )
        skipped_table.add_column(
            "File", justify="right", style="magenta", no_wrap=False, overflow="fold"
        )
        for case in skipped_tuples:
            skipped_table.add_row(case[1], case[2], str(case[0]))

        skipped_table.title = f"SKIPPED TEST CASES ({len(skipped_tuples)})"
        console.print(skipped_table)

    else:
        console.print(f"# Output test run saved in '{result_dir}'\n")


        if service_url:
            console.print(f"# Test instance '{service_url}'\n")



        console.print("# FAILED TEST CASES\n", style="red")
        console.print("\n".join(failed_cases), style="red")

        console.print("# SKIPPED TEST CASES\n", style="yellow")
        console.print("\n".join(skipped_cases), style="yellow")
    if failed_cases and exit_on_fail:
        exit(1)

if __name__ == "__main__":
    # result_dir: str = typer.Argument(..., help="Directory with the result to parse"),
    # exit_on_fail: bool = typer.Option(
    #     False, help="Force failing with exit code 1"
    # ),
    # service_url: str = typer.Option("", help="Optional service url to print to console"),
    # pretty_print: bool = typer.Option(False, help="Print with a better formatting"),
    parser = argparse.ArgumentParser(description="Parse OAF ETS results")
    parser.add_argument("result_dir", type=str, help="Directory with the result to parse")
    parser.add_argument('--service-url',  help='Optional service url to print to console')
    parser.add_argument('--pretty-print', action='store_true', help='Print with a better formatting')
    parser.add_argument('--exit-on-fail', action='store_true', help="Force failing with exit code 1 when failed tests cases in result")
    args = parser.parse_args()

    dir_path = Path(args.result_dir)
    if not dir_path.exists():
        err_console.print(f"test dir '{args.result_dir}' should exist")
        exit(1)

    main(args.result_dir, args.service_url, args.pretty_print, args.exit_on_fail)
