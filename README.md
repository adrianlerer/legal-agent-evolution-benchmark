# Legal Agent Evolution Benchmark

Experimental harness for evaluating legal AI as **induced workflows**, not isolated models.

The benchmark asks:

> Which workflow produces legally acceptable work at the lowest sustainable cost, under realistic perturbations, with failures that can be detected before a lawyer relies on them?

It is intentionally offline by default. The seed tasks are synthetic and non-confidential, so anyone can run the methodology without API keys or paid model calls.

## What This Tests

- Reliability: did the output satisfy all legal/task criteria?
- Usefulness: is it clear, structured, concise, and editable?
- Robustness: does performance survive prompt, role, and pressure variants?
- Verifiability: does the workflow expose checks and residual risks?
- Cost/workflow fit: what is the estimated cost per accepted output?
- Promotion readiness: should this skill/model/temperature/workflow be adopted?

## Quick Start

```bash
python3 -m legal_agent_benchmark.run \
  --tasks seed_tasks/tasks.jsonl \
  --out results/latest.json

python3 -m legal_agent_benchmark.report results/latest.json

python3 -m legal_agent_benchmark.promote \
  results/latest.json \
  --out results/promotion.json
```

Run tests:

```bash
python3 -m unittest discover -s tests -v
```

## Systems Included

- `bare_drafter`: simulates a raw model/wrapper that writes plausible drafts without explicit legal verification.
- `workflow_agent`: simulates a planning -> drafting -> verification workflow with checklist gates and residual-risk reporting.

These are not meant to be competitive models. They are executable controls that validate the benchmark logic before plugging in real APIs or apps.

## Extending

Add tasks to `seed_tasks/tasks.jsonl`. Each task includes:

- task family;
- prompt;
- induction variants;
- required criteria;
- must-fail conditions;
- cost estimates per system.

Future adapters can call Claude, OpenAI, Gemini, local models, or app wrappers, but paid or sensitive-data runs should be opt-in and budget-capped.

See [docs/production-loop.md](docs/production-loop.md) for the continuous-improvement loop and temperature defaults.

## License

MIT.
