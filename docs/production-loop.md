# Production Loop

The productive system is a loop, not a leaderboard.

```text
task -> route -> run -> score -> classify failure -> patch -> holdout -> promote/reject
```

## Runtime Unit

Optimize complete configurations:

```text
task family + skill + agent role + model + temperature + context/retrieval + verifier + cost cap
```

## Temperature Defaults

| Role | Temperature | Rationale |
|---|---:|---|
| Router/classifier | 0.0 | Deterministic task routing. |
| Extractor | 0.0-0.2 | Factual recall and field completeness. |
| Planner | 0.2-0.4 | Some judgment without excessive variance. |
| Drafter | 0.3-0.6 | Drafting quality with controlled creativity. |
| Brainstormer | 0.6-0.8 | Alternative arguments and strategy generation. |
| Verifier | 0.0-0.2 | Conservative checks and failure detection. |

Never use high temperature for final citation checks, extraction, legal authority, calculations, or compliance gates.

## Promotion Gate

Promote a configuration only if it passes:

- acceptance rate threshold;
- robustness threshold across induction variants;
- verifiability threshold;
- cost per accepted output threshold;
- no uncaught must-fail condition.

Run:

```bash
python3 -m legal_agent_benchmark.run --tasks seed_tasks/tasks.jsonl --out results/latest.json
python3 -m legal_agent_benchmark.promote results/latest.json --out results/promotion.json
```

## What Gets Updated

If the candidate passes, update:

- `config/skill_cards.json` with the best model/temperature/verifier settings;
- the relevant skill checklist;
- the model/router rule;
- the benchmark result record.

If it fails, update:

- failure taxonomy;
- rejected configuration notes;
- next experiment hypothesis.

## Productive MVP

1. Keep seed tasks synthetic and public.
2. Add private internal tasks locally, but do not commit them.
3. Add real model adapters only behind explicit budget and privacy gates.
4. Use the offline controls to verify benchmark code before paid runs.
5. Promote only changes that improve accepted output per unit cost.
