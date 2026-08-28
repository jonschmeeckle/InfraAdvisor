import io
from contextlib import redirect_stdout
import json
from analyzer.cisco_analyzer import analyze_cisco_config

def load_eval_cases():
    with open("evals/eval_cases.json", "r") as eval_file:
        return json.load(eval_file)


def main():
    eval_cases = load_eval_cases()

    for case in eval_cases:
        print(f"Eval: {case['name']}")

        with redirect_stdout(io.StringIO()):
            ai_analysis = analyze_cisco_config(case["config_file"])

        actual_finding = None

        for finding in ai_analysis["findings"]:
            if finding["interface"] == case["interface"]:
                actual_finding = finding
                break

        if actual_finding is None:
            print("Result: FAIL")
            print("Reason: Expected interface was not found.")
            continue

        severity_pass = (
            actual_finding["severity"] == case["expected_severity"]
        )

        confidence_pass = (
            actual_finding["confidence"] == case["expected_confidence"]
        )

        if severity_pass and confidence_pass:
            print("Result: PASS")
        else:
            print("Result: FAIL")

        print(f"Expected Severity: {case['expected_severity']}")
        print(f"Actual Severity:   {actual_finding['severity']}")
        print(f"Expected Confidence: {case['expected_confidence']}")
        print(f"Actual Confidence:   {actual_finding['confidence']}")


if __name__ == "__main__":
    main()