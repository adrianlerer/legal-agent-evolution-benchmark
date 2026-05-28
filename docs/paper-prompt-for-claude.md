# Prompt For Claude: Paper And Article Draft

Use this prompt in Claude after giving it the repo, the benchmark output, and any personal writing samples you want it to imitate.

```text
You are helping me draft a serious but readable paper/article in my voice.

Context:
- I am a lawyer working on legal AI, agent workflows, model routing, skills, verification, and cost governance.
- I do not want a generic "AI will transform law" piece.
- The thesis is that legal AI should be benchmarked as induced workflows, not isolated models.
- An induced workflow means: model + wrapper/app + prompt + role + examples + context + retrieval + sampling/settings + tools + verifier + human handoff.
- The trigger is a contrast between useful legal AI benchmarks that separate reliability/usefulness and a satirical MikeOSS post mocking benchmark theater.
- I want to be fair to existing benchmarks, not dismissive. They are useful, but incomplete.
- My contribution is a framework that adds robustness, verifiability, and cost per legally acceptable output.

Write in my style:
- precise, legally grounded, intellectually ambitious;
- practical rather than hype-driven;
- skeptical of benchmark theater but not anti-benchmark;
- comfortable with systems language: agents, workflows, skills, routing, verification, cost governance;
- avoid marketing language and inflated claims;
- write as a lawyer-builder, not as an academic outsider.

Core claims:
1. The right unit of legal AI evaluation is not the model, but the induced workflow.
2. Reliability and usefulness are distinct, but robustness is part of reliability in law.
3. Wrappers/apps matter and should be benchmarked as separate systems.
4. Cost should be measured as cost per legally acceptable output, not cost per API call.
5. Benchmarks should feed an evolution loop: run -> score -> classify failure -> patch skill/router/verifier -> rerun holdout -> promote or reject.
6. Cheap or local models can be valuable for classification, redaction, extraction, prompt variants, and synthetic fixtures, but not as final legal authority.
7. The goal is not to crown a model; it is to build legal AI systems that improve under evidence.

Use this structure:
1. Hook: why model leaderboards are useful but insufficient.
2. Benchmark theater: what goes wrong when rankings become marketing.
3. The induced-workflow unit of analysis.
4. Five evaluation dimensions: reliability, usefulness, robustness, verifiability, cost/workflow fit.
5. Induction robustness: prompt variants, role framing, app/API wrapper, temperature, repeated runs, retrieval on/off.
6. Failure taxonomy for legal AI.
7. Evolution loop for agents and skills.
8. Practical architecture: planner, executor, verifier, human handoff.
9. Implications for legal teams, vendors, and researchers.
10. Conclusion.

Include a short note suitable to send privately to Anna before publication:
- respectful;
- mentions that her reliability/usefulness distinction and wrapper finding helped trigger the thought;
- says I am drafting a short article/paper about evaluating legal AI as induced workflows;
- offers to share a draft before I publish independently or locally;
- asks whether she would welcome comments or a short exchange.

Deliver:
1. A 150-200 word DM to Anna.
2. A 900-1200 word article draft.
3. A more academic paper outline with abstract, research questions, method, metrics, limitations, and next empirical steps.
4. A sharper title list.
```
