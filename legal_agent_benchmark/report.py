from __future__ import annotations

import argparse
import json
from pathlib import Path


def render(path: str) -> str:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    lines = ["# Benchmark Report", ""]
    for system, stats in payload["summary"].items():
        lines.append(f"## {system}")
        lines.append(f"- Runs: {stats['runs']}")
        lines.append(f"- Accepted: {stats['accepted']}")
        lines.append(f"- Acceptance rate: {stats['acceptance_rate']}")
        lines.append(f"- Avg reliability: {stats['avg_reliability']}")
        lines.append(f"- Avg usefulness: {stats['avg_usefulness']}")
        lines.append(f"- Avg verifiability: {stats['avg_verifiability']}")
        lines.append(f"- Total estimated cost: {stats['total_estimated_cost']}")
        lines.append(f"- Cost per accepted output: {stats['cost_per_accepted_output']}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    print(render(args.path))


if __name__ == "__main__":
    main()
