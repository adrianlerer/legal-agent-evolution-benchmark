from __future__ import annotations

import argparse
import json
from pathlib import Path

from .evaluator import evaluate
from .loaders import load_tasks
from .systems import SYSTEMS


def run(tasks_path: str, out_path: str, systems: list[str] | None = None) -> dict:
    selected = systems or list(SYSTEMS)
    tasks = load_tasks(tasks_path)
    results = []
    for task in tasks:
        variants = task.variants
        if not variants:
            raise ValueError(f"Task {task.id} has no induction variants")
        for variant in variants:
            for system_name in selected:
                system = SYSTEMS[system_name]
                output = system.run(task, variant)
                evaluated = evaluate(task, variant, output).to_dict()
                evaluated["output_preview"] = output.text[:260]
                results.append(evaluated)

    summary = summarize(results)
    payload = {"summary": summary, "results": results}
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def summarize(results: list[dict]) -> dict:
    by_system: dict[str, list[dict]] = {}
    for row in results:
        by_system.setdefault(row["system"], []).append(row)
    summary = {}
    for system, rows in by_system.items():
        accepted = [row for row in rows if row["passed"]]
        total_cost = sum(float(row["cost"]) for row in rows)
        summary[system] = {
            "runs": len(rows),
            "accepted": len(accepted),
            "acceptance_rate": round(len(accepted) / len(rows), 4) if rows else 0.0,
            "robustness": robustness_score(rows),
            "avg_reliability": round(sum(row["reliability"] for row in rows) / len(rows), 4),
            "avg_usefulness": round(sum(row["usefulness"] for row in rows) / len(rows), 4),
            "avg_verifiability": round(sum(row["verifiability"] for row in rows) / len(rows), 4),
            "total_estimated_cost": round(total_cost, 6),
            "cost_per_accepted_output": round(total_cost / len(accepted), 6) if accepted else None,
        }
    return summary


def robustness_score(rows: list[dict]) -> float:
    """Score stability across induction variants for each task."""
    by_task: dict[str, list[dict]] = {}
    for row in rows:
        by_task.setdefault(row["task_id"], []).append(row)
    if not by_task:
        return 0.0
    task_scores = []
    for task_rows in by_task.values():
        pass_values = [1.0 if row["passed"] else 0.0 for row in task_rows]
        task_scores.append(1.0 if all(pass_values) else 0.0 if not any(pass_values) else 0.5)
    return round(sum(task_scores) / len(task_scores), 4)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", default="seed_tasks/tasks.jsonl")
    parser.add_argument("--out", default="results/latest.json")
    parser.add_argument("--systems", nargs="*", choices=sorted(SYSTEMS))
    args = parser.parse_args()
    payload = run(args.tasks, args.out, args.systems)
    print(json.dumps(payload["summary"], indent=2))


if __name__ == "__main__":
    main()
