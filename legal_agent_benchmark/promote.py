from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_THRESHOLDS = {
    "min_acceptance_rate": 0.8,
    "min_robustness": 0.8,
    "min_verifiability": 0.75,
    "max_cost_per_accepted_output": 0.02,
}


def decide(result_path: str, thresholds: dict | None = None) -> dict:
    payload = json.loads(Path(result_path).read_text(encoding="utf-8"))
    thresholds = thresholds or DEFAULT_THRESHOLDS
    decisions = {}
    for system, stats in payload["summary"].items():
        reasons: list[str] = []
        cost = stats["cost_per_accepted_output"]
        if stats["acceptance_rate"] < thresholds["min_acceptance_rate"]:
            reasons.append("acceptance_rate_below_threshold")
        if stats["robustness"] < thresholds["min_robustness"]:
            reasons.append("robustness_below_threshold")
        if stats["avg_verifiability"] < thresholds["min_verifiability"]:
            reasons.append("verifiability_below_threshold")
        if cost is None or cost > thresholds["max_cost_per_accepted_output"]:
            reasons.append("cost_per_accepted_output_above_threshold")
        decisions[system] = {
            "decision": "promote" if not reasons else "reject",
            "reasons": reasons,
            "stats": stats,
        }
    return {"thresholds": thresholds, "decisions": decisions}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("result_path")
    parser.add_argument("--out", default="results/promotion.json")
    args = parser.parse_args()
    payload = decide(args.result_path)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
