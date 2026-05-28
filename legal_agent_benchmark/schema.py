from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Criterion:
    id: str
    description: str
    keywords: tuple[str, ...]

    @staticmethod
    def from_dict(raw: dict[str, Any]) -> "Criterion":
        return Criterion(
            id=str(raw["id"]),
            description=str(raw["description"]),
            keywords=tuple(str(x).lower() for x in raw.get("keywords", [])),
        )


@dataclass(frozen=True)
class Variant:
    id: str
    framing: str
    pressure: str
    temperature: float

    @staticmethod
    def from_dict(raw: dict[str, Any]) -> "Variant":
        return Variant(
            id=str(raw["id"]),
            framing=str(raw.get("framing", "neutral")),
            pressure=str(raw.get("pressure", "none")),
            temperature=float(raw.get("temperature", 0.0)),
        )


@dataclass(frozen=True)
class Task:
    id: str
    family: str
    jurisdiction: str
    prompt: str
    criteria: tuple[Criterion, ...]
    must_fail_keywords: tuple[str, ...]
    variants: tuple[Variant, ...]
    estimated_cost: dict[str, float]

    @staticmethod
    def from_dict(raw: dict[str, Any]) -> "Task":
        return Task(
            id=str(raw["id"]),
            family=str(raw["family"]),
            jurisdiction=str(raw.get("jurisdiction", "generic")),
            prompt=str(raw["prompt"]),
            criteria=tuple(Criterion.from_dict(x) for x in raw.get("criteria", [])),
            must_fail_keywords=tuple(str(x).lower() for x in raw.get("must_fail_keywords", [])),
            variants=tuple(Variant.from_dict(x) for x in raw.get("variants", [])),
            estimated_cost={str(k): float(v) for k, v in raw.get("estimated_cost", {}).items()},
        )
