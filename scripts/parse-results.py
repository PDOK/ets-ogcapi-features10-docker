#!/bin/env python3
import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table

from junitparser import JUnitXml


app = typer.Typer()
err_console = Console(stderr=True)
console = Console()
table = Table(title="Compliance Error result", show_lines=True)


@app.command()
def parse(
    result_dir: str = typer.Option(
        ...,
        help="Directory with the result to parse"),
    exit_on_fail: bool = typer.Option(
        False,
        help="Force failing with exit code 1 for CI pipeline"),
    pretty_print: bool = typer.Option(
        False,
        help="Print with a better formatting")
    ):
    """
    Parse junit result.
    """
    dir_path = Path(result_dir)
    if not dir_path.exists():
        err_console.print(f"test dir '{result_dir}' should exist")
        raise typer.Exit()

    failed_cases = []
    failed_tuples = []

    for junit_test in dir_path.glob("**/**/TEST-org.opengis.cite.*.xml"):
        test_xml = JUnitXml.fromfile(str(junit_test))
        failed = [case.message for suite in test_xml for case in suite if case.type == "java.lang.Throwable"]
        failed_tuples += [
            (
                junit_test.name,
                test_xml.name,
                case.message
            ) for suite in test_xml for case in suite if case.type == "java.lang.Throwable"]
        if failed:
            failed_cases += [f"### {test_xml.name}"] + failed + [""]

    if pretty_print:
        table.add_column("Case Name", justify="right", style="cyan", no_wrap=False)
        table.add_column("Error", justify="right", style="red", no_wrap=False)
        table.add_column("File", justify="right", style="magenta", no_wrap=False)
        # case_iter = iter(failed_cases)
        # cases = zip(case_iter, case_iter, case_iter)
        for case in failed_tuples:
            table.add_row(case[1], case[2], str(case[0]))
        console.print(table)
    else:
        typer.secho("\n".join(failed_cases), fg=typer.colors.RED)
    if failed_cases and exit_on_fail:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
