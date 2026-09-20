from __future__ import annotations

import laya

from shared import ISSUE_TYPE_CRITERIA, SEVERITY_CRITERIA, STATE

MODEL_REPO = "convaiinnovations/laya"
MODEL_SUBFOLDER = "typed-decisions"

QUESTIONS = {
    "issue_type": {
        "type": "choice",
        "instructions": "What is the primary issue type described in `incident_report`?",
        "criteria": ISSUE_TYPE_CRITERIA,
    },
    "production_impact": {
        "type": "noul",
        "instructions": (
            "Does `incident_report` indicate that production users are currently impacted?"
        ),
    },
    "severity": {
        "type": "score",
        "instructions": "How severe is the user impact described in `incident_report`?",
        "criteria": SEVERITY_CRITERIA,
    },
}


def run():
    agent = laya.load(MODEL_REPO, subfolder=MODEL_SUBFOLDER)
    return agent.predict(STATE, QUESTIONS)


def main() -> None:
    result = run()
    answers = result["answers"]

    issue_type = answers["issue_type"]
    production_impact = answers["production_impact"]
    severity = answers["severity"]

    print("Backend: Laya")
    print(f"Checkpoint: {MODEL_REPO}/{MODEL_SUBFOLDER}")

    print("\nIssue type")
    print(f"  choice: {issue_type['choice']}")
    print(f"  confidence: {issue_type['confidence']:.3f}")
    print("  probabilities:")
    for label, probability in sorted(
        issue_type.get("probabilities", {}).items(),
        key=lambda item: item[1],
        reverse=True,
    ):
        print(f"    {label}: {probability:.3f}")

    print("\nProduction impact")
    print(f"  noul (P[yes]): {production_impact['noul']:.3f}")

    print("\nSeverity")
    print(f"  score: {severity['score']:.3f}")
    print(f"  confidence: {severity['confidence']:.3f}")
    print("  probabilities:")
    for level, probability in severity.get("probabilities", {}).items():
        print(f"    {level}: {probability:.3f}")
    print("  rubric:")
    for level, description in enumerate(SEVERITY_CRITERIA):
        print(f"    {level}: {description}")


if __name__ == "__main__":
    main()
