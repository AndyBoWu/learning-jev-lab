from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

STATE = {
    "incident_report": (
        "After today's deployment, users are getting 502 errors when uploading files. "
        "About 30% of upload requests are failing."
    )
}

QUESTIONS = {
    "issue_type": Choice(
        instructions="What is the primary issue type described in `incident_report`?",
        criteria={
            "bug": "Broken or incorrect product behavior.",
            "feature": "A request for new product behavior.",
            "documentation": "Missing, unclear, or incorrect documentation.",
            "question": "A request for information or explanation.",
            "security": "A vulnerability or security-sensitive problem.",
            "other": "None of the other categories fit well.",
        },
    ),
    "production_impact": Noul(
        instructions=(
            "Does `incident_report` indicate that production users are currently impacted?"
        ),
    ),
    "severity": Score(
        instructions="How severe is the user impact described in `incident_report`?",
        criteria=[
            "No user-visible impact.",
            "Minor impact with an easy workaround.",
            "Noticeable degradation affecting some users or requests.",
            "Major impact affecting many users or a critical workflow.",
            "Critical outage or widespread inability to use the service.",
        ],
    ),
}


def main() -> None:
    with TypeSafeClient() as client:
        response = client.system_one(state=STATE, questions=QUESTIONS)

    issue_type = response.choices["issue_type"]
    production_impact = response.nouls["production_impact"]
    severity = response.scores["severity"]

    print("Issue type")
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
