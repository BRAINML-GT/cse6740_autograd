import json
import os
import pytest


def run_pytest():
    """
    Run pytest with the pytest-json-report plugin enabled.
    The report will be saved as 'report.json' in the current directory.
    """
    # The options below instruct pytest to:
    #   - run tests in the "tests" directory
    #   - generate a JSON report stored in report.json
    pytest_args = [
        "tests",  # directory with test files
        "--json-report",  # enable JSON report generation
        "--json-report-file=report.json",  # specify the output file name
    ]
    return pytest.main(pytest_args)


def process_report():
    """
    Process the JSON report from pytest and generate a Gradescope results.json.
    This example computes a simple score: start from 100 points and subtract
    10 points for each failed or error test.
    """
    report_file = "report.json"
    if not os.path.exists(report_file):
        raise FileNotFoundError(
            f"{report_file} not found. Make sure pytest generated it."
        )

    with open(report_file, "r") as f:
        report = json.load(f)

    summary = report.get("summary", {})
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    errors = summary.get("errors", 0)
    skipped = summary.get("skipped", 0)
    total_tests = passed + failed + errors + skipped

    # Define scoring: deduct 10 points for each failed or error test.
    penalty_per_fail = 10
    deductions = penalty_per_fail * (failed + errors)
    score = max(0, 100 - deductions)

    # Build test details list.
    tests_detail = []

    # Loop through all tests in the report for details on failures/errors.
    for test in report.get("tests", []):
        nodeid = test.get("nodeid", "unknown test")
        outcome = test.get("outcome", "")
        if outcome in ["failed", "error"]:
            # For failed/error tests, include the detailed longrepr output.
            longrepr = test.get("longrepr", "No traceback available")
            tests_detail.append(
                {
                    "name": nodeid,
                    "score": 0,
                    "max_score": penalty_per_fail,
                    "output": f"{outcome.capitalize()}:\n{longrepr}",
                }
            )

    # Optionally, add a summary entry.
    tests_detail.append(
        {
            "name": "Summary",
            "score": score,
            "max_score": 100,
            "output": f"{passed} tests passed out of {total_tests} total tests.",
        }
    )

    results = {
        "score": score,
        "max_score": 100,
        "tests": tests_detail,
    }
    return results


if __name__ == "__main__":
    print("Starting pytest execution...")
    run_pytest()
    print("Processing pytest report...")
    results = process_report()
    with open("results.json", "w") as f:
        json.dump(results, f)
    print("Finished. Results written to results.json")
