from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from legal_agent_benchmark.loaders import load_tasks
from legal_agent_benchmark.promote import decide
from legal_agent_benchmark.run import run


ROOT = Path(__file__).resolve().parents[1]


class BenchmarkTest(unittest.TestCase):
    def test_load_seed_tasks(self) -> None:
        tasks = load_tasks(ROOT / "seed_tasks" / "tasks.jsonl")
        self.assertEqual(len(tasks), 5)
        self.assertTrue(all(task.variants for task in tasks))
        self.assertTrue(any(variant.temperature > 0 for task in tasks for variant in task.variants))

    def test_workflow_beats_bare_drafter_on_seed_set(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            payload = run(str(ROOT / "seed_tasks" / "tasks.jsonl"), str(Path(tmp) / "out.json"))
        bare = payload["summary"]["bare_drafter"]
        workflow = payload["summary"]["workflow_agent"]
        self.assertGreater(workflow["acceptance_rate"], bare["acceptance_rate"])
        self.assertGreater(workflow["robustness"], bare["robustness"])
        self.assertGreater(workflow["avg_verifiability"], bare["avg_verifiability"])
        self.assertIsNotNone(workflow["cost_per_accepted_output"])

    def test_promotion_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out.json"
            run(str(ROOT / "seed_tasks" / "tasks.jsonl"), str(out))
            payload = decide(str(out))
        self.assertEqual(payload["decisions"]["workflow_agent"]["decision"], "promote")
        self.assertEqual(payload["decisions"]["bare_drafter"]["decision"], "reject")


if __name__ == "__main__":
    unittest.main()
