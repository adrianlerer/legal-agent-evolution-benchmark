from __future__ import annotations

import json
from pathlib import Path

from .schema import Task


def load_tasks(path: str | Path) -> list[Task]:
    tasks: list[Task] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                tasks.append(Task.from_dict(json.loads(stripped)))
            except Exception as exc:  # pragma: no cover - error path includes context
                raise ValueError(f"Invalid task JSONL at line {line_no}: {exc}") from exc
    return tasks
