from __future__ import annotations

from dataclasses import asdict, dataclass

from .schema import Task, Variant
from .systems import SystemOutput


@dataclass(frozen=True)
class EvalResult:
    task_id: str
    family: str
    variant_id: str
    system: str
    reliability: float
    usefulness: float
    verifiability: float
    passed: bool
    missing_criteria: tuple[str, ...]
    must_fail_hits: tuple[str, ...]
    cost: float

    def to_dict(self) -> dict:
        return asdict(self)


def evaluate(task: Task, variant: Variant, output: SystemOutput) -> EvalResult:
    text = output.text.lower()
    missing: list[str] = []
    for criterion in task.criteria:
        has_keyword = any(keyword in text for keyword in criterion.keywords)
        has_check = output.checks.get(criterion.id, False)
        if not (has_keyword or has_check):
            missing.append(criterion.id)

    must_fail_hits = tuple(keyword for keyword in task.must_fail_keywords if keyword in text)
    reliability = 1.0 if not missing and not must_fail_hits else max(0.0, 1.0 - 0.25 * len(missing) - 0.5 * len(must_fail_hits))
    usefulness = score_usefulness(output.text)
    verifiability = 1.0 if output.checks and output.residual_risks else 0.25 if output.checks else 0.0
    passed = reliability >= 1.0 and usefulness >= 0.6 and verifiability >= 0.75
    return EvalResult(
        task_id=task.id,
        family=task.family,
        variant_id=variant.id,
        system=output.system,
        reliability=round(reliability, 4),
        usefulness=round(usefulness, 4),
        verifiability=round(verifiability, 4),
        passed=passed,
        missing_criteria=tuple(missing),
        must_fail_hits=must_fail_hits,
        cost=float(task.estimated_cost.get(output.system, 0.0)),
    )


def score_usefulness(text: str) -> float:
    length = len(text.split())
    if length < 20:
        return 0.3
    if length > 180:
        return 0.55
    score = 0.7
    if "checklist" in text.lower() or "recommended" in text.lower():
        score += 0.15
    if "lawyer review" in text.lower() or "residual" in text.lower():
        score += 0.1
    return min(score, 1.0)
