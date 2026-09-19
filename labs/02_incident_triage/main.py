from __future__ import annotations

import argparse

from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

SCENARIOS = {
    "clear": {
        "incident": {
            "summary": "Checkout latency and errors spiked immediately after deployment",
            "details": (
                "Five minutes after deploy 8f72c1, checkout API p99 latency increased "
                "from 220 ms to 4.2 s and the error rate reached 18%. Three regions are "
                "affected. Database metrics are normal. Rolling back the same build in "
                "staging restored normal latency."
            ),
        }
    },
    "ambiguous": {
        "incident": {
            "summary": "Checkout may be slower than usual",
            "details": (
                "A few users mentioned intermittent timeouts today. There was a deployment "
                "earlier, but we do not know whether the timing lines up. The metrics dashboard "
                "has gaps, and we do not yet know how many regions or users are affected."
            ),
        }
    },
}

QUESTIONS = {
    "incident_type": Choice(
        instructions=(
            "What is the primary incident type described by `incident.summary` and "
            "`incident.details`?"
        ),
        criteria={
            "application": "A problem in application behavior or application code.",
            "infrastructure": "A compute, orchestration, capacity, host, or platform problem.",
            "database": "A database availability, performance, or correctness problem.",
            "network": "A network, connectivity, routing, or DNS problem.",
            "dependency": "A third-party or downstream dependency problem.",
            "unknown": "The evidence is insufficient to identify a primary type.",
        },
    ),
    "customer_impact": Noul(
        instructions=(
            "Do `incident.summary` and `incident.details` indicate that customers are "
            "currently experiencing a real service impact?"
        ),
    ),
    "deployment_related": Noul(
        instructions=(
            "Do `incident.summary` and `incident.details` indicate that the current incident "
            "is causally related to a recent deployment?"
        ),
    ),
    "rollback_candidate": Noul(
        instructions=(
            "Based only on `incident.summary` and `incident.details`, is rollback a plausible "
            "remediation candidate for this incident?"
        ),
        criteria={
            "yes": (
                "Evidence links the incident to a recent change and rollback could reasonably "
                "restore service."
            ),
            "no": "The evidence does not support rollback as a useful remediation candidate.",
        },
    ),
    "severity": Score(
        instructions=(
            "How severe is the current customer impact described by `incident.summary` and "
            "`incident.details`?"
        ),
        criteria=[
            "No confirmed customer impact.",
            "Minor or isolated impact with service mostly healthy.",
            "Meaningful degradation affecting a subset of customers or requests.",
            "Major degradation affecting many customers or a critical workflow.",
            "Widespread outage, severe data risk, or similarly critical impact.",
        ],
    ),
    "security_sensitive": Noul(
        instructions=(
            "Do `incident.summary` and `incident.details` contain evidence that this incident "
            "may involve a security-sensitive condition requiring specialized review?"
        ),
    ),
}

# Teaching thresholds only. Lab 05 will evaluate and tune thresholds with labeled data.
LOW_RISK_CLASSIFICATION_CONFIDENCE = 0.55
HIGH_RISK_SEVERITY_CONFIDENCE = 0.80
CUSTOMER_IMPACT_THRESHOLD = 0.80
HIGH_SEVERITY_THRESHOLD = 2.50
DEPLOYMENT_RELATED_THRESHOLD = 0.70
ROLLBACK_CANDIDATE_THRESHOLD = 0.80
SECURITY_REVIEW_THRESHOLD = 0.60


def decide_actions(
    *,
    incident_type: str,
    incident_type_confidence: float,
    customer_impact: float,
    deployment_related: float,
    rollback_candidate: float,
    severity: float,
    severity_confidence: float,
    security_sensitive: float,
) -> list[str]:
    """Apply risk-aware deterministic policy to Jev judgments."""

    actions: list[str] = []

    # Low-risk action: applying a descriptive type label is recoverable.
    if incident_type_confidence >= LOW_RISK_CLASSIFICATION_CONFIDENCE:
        actions.append(f"label:type:{incident_type}")
    else:
        actions.append("route:human-triage (incident type is uncertain)")

    # Security-sensitive cases are always made human-visible.
    if security_sensitive >= SECURITY_REVIEW_THRESHOLD:
        actions.append("route:security-review")

    # Higher-risk action: paging on-call requires both evidence of impact and
    # sufficiently confident severity.
    if customer_impact >= CUSTOMER_IMPACT_THRESHOLD and severity >= HIGH_SEVERITY_THRESHOLD:
        if severity_confidence >= HIGH_RISK_SEVERITY_CONFIDENCE:
            actions.append("notify:on-call")
        else:
            actions.append("review:on-call-decision (severity confidence too low)")

    # rollback_candidate is speculative: it is useful only when the incident also
    # looks deployment-related. We still asked it in the same Jev request.
    if (
        deployment_related >= DEPLOYMENT_RELATED_THRESHOLD
        and rollback_candidate >= ROLLBACK_CANDIDATE_THRESHOLD
    ):
        actions.append("recommend:rollback")
        actions.append("require:human-confirmation-before-rollback")

    if not actions:
        actions.append("monitor:no-automatic-action")

    return actions


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scenario",
        choices=SCENARIOS,
        default="clear",
        help="Run either a clear or intentionally ambiguous incident.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    state = SCENARIOS[args.scenario]

    with TypeSafeClient() as client:
        response = client.system_one(state=state, questions=QUESTIONS)

    incident_type = response.choices["incident_type"]
    customer_impact = response.nouls["customer_impact"]
    deployment_related = response.nouls["deployment_related"]
    rollback_candidate = response.nouls["rollback_candidate"]
    severity = response.scores["severity"]
    security_sensitive = response.nouls["security_sensitive"]

    print(f"Scenario: {args.scenario}")
    print("\nSemantic judgments from Jev")
    print(
        f"  incident type: {incident_type.choice} "
        f"(confidence={incident_type.confidence:.3f})"
    )
    print(f"  customer impact P[yes]: {customer_impact.noul:.3f}")
    print(f"  deployment related P[yes]: {deployment_related.noul:.3f}")
    print(f"  rollback candidate P[yes]: {rollback_candidate.noul:.3f}")
    print(f"  severity: {severity.score:.3f} (confidence={severity.confidence:.3f})")
    print(f"  security sensitive P[yes]: {security_sensitive.noul:.3f}")

    actions = decide_actions(
        incident_type=incident_type.choice,
        incident_type_confidence=incident_type.confidence,
        customer_impact=customer_impact.noul,
        deployment_related=deployment_related.noul,
        rollback_candidate=rollback_candidate.noul,
        severity=severity.score,
        severity_confidence=severity.confidence,
        security_sensitive=security_sensitive.noul,
    )

    print("\nRisk-aware deterministic policy")
    for action in actions:
        print(f"  - {action}")


if __name__ == "__main__":
    main()
