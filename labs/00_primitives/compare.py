from __future__ import annotations

from jev import run as run_jev
from laya_backend import run as run_laya


def main() -> None:
    jev = run_jev()
    laya = run_laya()["answers"]

    jev_issue = jev.choices["issue_type"]
    jev_impact = jev.nouls["production_impact"]
    jev_severity = jev.scores["severity"]

    laya_issue = laya["issue_type"]
    laya_impact = laya["production_impact"]
    laya_severity = laya["severity"]

    print("Lab 00 — Jev vs Laya")
    print()
    print(f"{'Decision':<22} {'Jev':<28} {'Laya'}")
    print("-" * 82)
    print(
        f"{'issue_type':<22} "
        f"{jev_issue.choice + f' (conf={jev_issue.confidence:.3f})':<28} "
        f"{laya_issue['choice']} (conf={laya_issue['confidence']:.3f})"
    )
    print(
        f"{'production_impact':<22} "
        f"{f'P[yes]={jev_impact.noul:.3f}':<28} "
        f"P[yes]={laya_impact['noul']:.3f}"
    )
    print(
        f"{'severity':<22} "
        f"{f'{jev_severity.score:.3f} (conf={jev_severity.confidence:.3f})':<28} "
        f"{laya_severity['score']:.3f} (conf={laya_severity['confidence']:.3f})"
    )

    print(
        "\nDo not treat Jev and Laya confidence values as interchangeable. "
        "They come from different models and calibration procedures; Lab 05 will evaluate "
        "thresholds empirically on shared labeled data."
    )


if __name__ == "__main__":
    main()
