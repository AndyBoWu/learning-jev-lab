from __future__ import annotations

STATE = {
    "incident_report": (
        "After today's deployment, users are getting 502 errors when uploading files. "
        "About 30% of upload requests are failing."
    )
}

ISSUE_TYPE_CRITERIA = {
    "bug": "Broken or incorrect product behavior.",
    "feature": "A request for new product behavior.",
    "documentation": "Missing, unclear, or incorrect documentation.",
    "question": "A request for information or explanation.",
    "security": "A vulnerability or security-sensitive problem.",
    "other": "None of the other categories fit well.",
}

SEVERITY_CRITERIA = [
    "No user-visible impact.",
    "Minor impact with an easy workaround.",
    "Noticeable degradation affecting some users or requests.",
    "Major impact affecting many users or a critical workflow.",
    "Critical outage or widespread inability to use the service.",
]
