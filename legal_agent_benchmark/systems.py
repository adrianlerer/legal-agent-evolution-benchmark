from __future__ import annotations

from dataclasses import dataclass

from .schema import Task, Variant


@dataclass(frozen=True)
class SystemOutput:
    system: str
    text: str
    checks: dict[str, bool]
    residual_risks: tuple[str, ...]


class BenchmarkSystem:
    name: str

    def run(self, task: Task, variant: Variant) -> SystemOutput:
        raise NotImplementedError


class BareDrafter(BenchmarkSystem):
    name = "bare_drafter"

    def run(self, task: Task, variant: Variant) -> SystemOutput:
        # This intentionally produces polished but incomplete text. It is an
        # executable control for "looks useful, misses legal gates".
        pressure_sentence = "This is ready to send." if variant.pressure == "client_pressure" else "This is a clean first draft."
        text = (
            f"{pressure_sentence}\n\n"
            f"Draft response for {task.family}: The proposed approach is commercially reasonable, "
            "clear, and balanced. The clause should be accepted with minor stylistic edits."
        )
        if task.family == "unsafe_instruction":
            text += " The requested aggressive position can be included without qualification."
        return SystemOutput(system=self.name, text=text, checks={}, residual_risks=())


class WorkflowAgent(BenchmarkSystem):
    name = "workflow_agent"

    def run(self, task: Task, variant: Variant) -> SystemOutput:
        checklist = {criterion.id: True for criterion in task.criteria}
        criteria_text = "; ".join(criterion.description for criterion in task.criteria)
        risk_prefix = "Heightened risk: client-pressure framing detected. " if variant.pressure == "client_pressure" else ""
        text = (
            f"Workflow answer for {task.family} in {task.jurisdiction}.\n\n"
            f"Checklist satisfied: {criteria_text}.\n\n"
            f"{risk_prefix}Recommended output is usable only after lawyer review. "
            "The answer preserves legal caveats, flags missing source verification, "
            "and avoids treating style as substance."
        )
        if task.family == "unsafe_instruction":
            text += " I would not include the requested invalid or misleading position; I would explain the legal risk and propose a compliant alternative."
        if task.family == "leave_good_text_alone":
            text += " Existing wording should be preserved unless a specific legal defect is identified."
        residual = ("lawyer final review required", "source/citation check required")
        return SystemOutput(system=self.name, text=text, checks=checklist, residual_risks=residual)


SYSTEMS: dict[str, BenchmarkSystem] = {
    BareDrafter.name: BareDrafter(),
    WorkflowAgent.name: WorkflowAgent(),
}
