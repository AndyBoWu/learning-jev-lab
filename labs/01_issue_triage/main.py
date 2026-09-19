from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

STATE = {
    "issue": {
        "title": "Upload API returns 502 after v2.4.0",
        "body": (
            "After upgrading to v2.4.0, POST /uploads returns 502 for about 30% "
            "of requests in production. Rolling back to v2.3.7 restores normal "
            "behavior. We reproduced this in us-west-2 and us-east-1. Logs show "
            "upstream connection reset errors."
        ),
    }
}

QUESTIONS = {
    "issue_type": Choice(
        instructions=(
            "What is the primary type of issue described by `issue.title` and "
            "`issue.body`?"
        ),
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
            "Do `issue.title` and `issue.body` indicate that production users "
            "are currently affected?"
        ),
    ),
    "severity": Score(
        instructions=(
            "How severe is the current user impact described by `issue.title` "
            "and `issue.body`?"
        ),
        criteria=[
            "No user-visible impact.",
            "Minor impact with an easy workaround.",
            "Partial degradation affecting some users or requests.",
            "Major impact affecting many users or a critical workflow.",
            "Widespread outage, data loss, or similarly critical impact.",
        ],
    ),
    "actionable": Noul(
        instructions=(
            "Does `issue.body` provide enough concrete evidence for an engineer "
            "to begin investigation without first asking what happened?"
        ),
        criteria={
            "yes": (
                "The report includes useful evidence such as symptoms, versions, "
                "environment, reproduction details, rollback observations, or logs."
            ),
            "no": "The report is too vague to begin a useful investigation.",
        },
    ),
}


def build_triage_plan(
    *,
    issue_type: str,
    production_impact: float,
    severity: float,
    actionable: float,
) -> tuple[list[str], str]:
    """Convert semantic judgments into deterministic workflow decisions."""

    labels = [f"type:{issue_type}"]

    if production_impact >= 0.5:
        labels.append("impact:production")

    if severity >= 3.5:
        labels.append("priority:critical")
    elif severity >= 2.5:
        labels.append("priority:high")
    elif severity >= 1.5:
        labels.append("priority:medium")
    else:
        labels.append("priority:low")

    if actionable < 0.5:
        labels.append("needs-info")

    if issue_type == "security":
        route = "security-review"
    elif production_impact >= 0.5 and severity >= 2.5:
        route = "on-call"
    elif actionable < 0.5:
        route = "needs-triage"
    else:
        route = "engineering-backlog"

    return labels, route


def main() -> None:
    with TypeSafeClient() as client:
        response = client.system_one(state=STATE, questions=QUESTIONS)

    issue_type = response.choices["issue_type"]
    production_impact = response.nouls["production_impact"]
    severity = response.scores["severity"]
    actionable = response.nouls["actionable"]

    print("Semantic judgments from Jev")
    print(f"  issue type: {issue_type.choice} (confidence={issue_type.confidence:.3f})")
    print(f"  production impact P[yes]: {production_impact.noul:.3f}")
    print(f"  severity: {severity.score:.3f} (confidence={severity.confidence:.3f})")
    print(f"  actionable P[yes]: {actionable.noul:.3f}")

    labels, route = build_triage_plan(
        issue_type=issue_type.choice,
        production_impact=production_impact.noul,
        severity=severity.score,
        actionable=actionable.noul,
    )

    print("\nDeterministic policy")
    print(f"  labels: {', '.join(labels)}")
    print(f"  route: {route}")


if __name__ == "__main__":
    main()
