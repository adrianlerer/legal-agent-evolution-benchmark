from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from legal_agent_benchmark.loaders import load_tasks
from legal_agent_benchmark.run import run


ROOT = Path(__file__).resolve().parents[1]


class BenchmarkTest(unittest.TestCase):
    def test_load_seed_tasks(self) -> None:
        tasks = load_tasks(ROOT / "seed_tasks" / "tasks.jsonl")
        self.assertEqual(len(tasks), 5)
        self.assertTrue(all(task.variants for task in tasks))

    def test_workflow_beats_bare_drafter_on_seed_set(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            payload = run(str(ROOT / "seed_tasks" / "tasks.jsonl"), str(Path(tmp) / "out.json"))
        bare = payload["summary"]["bare_drafter"]
        workflow = payload["summary"]["workflow_agent"]
        self.assertGreater(workflow["acceptance_rate"], bare["acceptance_rate"])
        self.assertGreater(workflow["avg_verifiability"], bare["avg_verifiability"])
        self.assertIsNotNone(workflow["cost_per_accepted_output"])


if __name__ == "__main__":
    unittest.main()
