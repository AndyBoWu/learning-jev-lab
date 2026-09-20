from __future__ import annotations

from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

from shared import ISSUE_TYPE_CRITERIA, SEVERITY_CRITERIA, STATE

QUESTIONS = {
    "issue_type": Choice(
        instructions="What is the primary issue type described in `incident_report`?",
        criteria=ISSUE_TYPE_CRITERIA,
    ),
    "production_impact": Noul(
        instructions=(
            "Does `incident_report` indicate that production users are currently impacted?"
        ),
    ),
    "severity": Score(
        instructions="How severe is the user impact described in `incident_report`?",
        criteria=SEVERITY_CRITERIA,
    ),
}


def run():
    with TypeSafeClient() as client:
        return client.system_one(state=STATE, questions=QUESTIONS)


def main() -> None:
    response = run()

    issue_type = response.choices["issue_type"]
    production_impact = response.nouls["production_impact"]
    severity = response.scores["severity"]

    print("Backend: Jev")
    print("\nIssue type")
    print(f"  choice: {issue_type.choice}")
    print(f"  confidence: {issue_type.confidence:.3f}")
    print("  probabilities:")
    for label, probability in sorted(
        issue_type.probabilities.items(), key=lambda item: item[1], reverse=True
    ):
        print(f"    {label}: {probability:.3f}")

    print("\nProduction impact")
    print(f"  noul (P[yes]): {production_impact.noul:.3f}")

    print("\nSeverity")
    print(f"  score: {severity.score:.3f}")
    print(f"  confidence: {severity.confidence:.3f}")
    print("  probabilities:")
    for level, probability in sorted(severity.probabilities.items()):
        print(f"    {level}: {probability:.3f}")
    print("  legend:")
    for level, description in severity.legend.items():
        print(f"    {level}: {description}")


if __name__ == "__main__":
    main()
