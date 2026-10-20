# Project Surgeon team workflow — task handoff and simplicity standard

This is an **instructional workflow**, not an external job queue or automatic enforcement engine. The main Codex session is Tech Lead. All subagents report to it. Respect the parent session's available tools and approval permissions.

## 1. Choose the smallest correct solution

In order of preference:
1. Reuse an existing tested function, component or package if it already solves the problem.
2. Make the smallest localized change that meets acceptance criteria and preserves current contracts.
3. Extract a shared helper **only** when multiple call sites truly share behavior and it reduces complexity.
4. Add a new abstraction, dependency, background job or subsystem **only** with a clear demonstrated benefit.

Avoid speculative frameworks, needless configuration, one-use wrappers, premature generalization, unnecessary migrations, and "just in case" branches. Favor readable names, simple control flow, type safety, maintainable tests and minimal code churn. Correctness, safety and measurable performance take priority over brevity. Never remove needed validation or safeguards to make code shorter.

Before writing code, state the chosen approach in 1–3 sentences and why simpler alternatives are insufficient, if relevant. For performance claims, measure before and after.

## 2. Delegate substantial tasks by default

A task is **substantial** if it crosses layers/packages, has 3+ independently checkable subtasks, involves several workflows or contracts, or needs meaningful implementation **plus** separate test/security work.

When native subagent delegation is available, Tech Lead **must use at least one appropriate specialist subagent** for every substantial task; delegate independent investigation/implementation/test work to multiple specialists when useful. Start with 2–3 specialists including a reviewer, not all eight. For a large task split into independently owned modules with concrete acceptance criteria. Parallelize read-only work and disjoint writes; never assign conflicting file ownership. Small tasks stay with the main agent to avoid overhead.

If delegation isn't supported, explain that actual subagents are unavailable and do the work sequentially in the main session with the same review checkpoints. **Never claim subagents ran if they didn't.**

## 3. Tech Lead task ledger

Keep a compact ledger in the session for multi-step tasks; write a project file only if requested and safe. Each task has:
- ID, goal, dependencies, owner, **allowed file paths**, prohibited paths and contract boundaries
- definition of done: acceptance cases and tests to be executed
- status: `QUEUED`, `ASSIGNED`, `SUBMITTED`, `ACCEPTED`, `REWORK`, `BLOCKED` or `UNVERIFIED`
- evidence: changed files, checks, risks and the reviewing Tech Lead's decision

No subagent may self-assign `ACCEPTED`. A subagent completes its assignment by submitting a **handoff**, not by authorizing the next dependent task.

## 4. Mandatory specialist handoff

Every delegated assignment MUST return to Tech Lead with:
- Task ID and scope; **DONE / PARTIAL / BLOCKED** from specialist's perspective
- concise implementation or investigation summary and why this is the simplest maintainable approach
- exact files changed / not changed and confirmation of ownership boundaries
- tests/checks actually run with **PASS / FAIL / SKIPPED** and relevant commands or evidence
- acceptance criteria met / unmet, potential regressions, protected-code issues and unresolved questions
- recommended next action (**review, rework, or blocked**)

Do not merely say "done", assume the parent can inspect private thoughts, or claim a test passed without running it. Report newly discovered work to Tech Lead; do not silently expand scope or start the next dependent milestone.

## 5. Tech Lead acceptance gate — required for every task

After each subagent handoff, before a dependent task advances, Tech Lead must:
1. Inspect the delivered changes and compare them against scoped acceptance criteria. Confirm no unauthorized files, secrets, migrations, production systems or existing user changes were touched.
2. Verify the proposed approach is the simplest correct one. Reject needless complexity, duplicate abstractions, unjustified dependencies and avoidable extra code.
3. Examine exact diff, contracts, test evidence and results. Run or request additional safe checks when needed. Verify behavior, not only test count.
4. Seek QA's independent review for substantive implementation, and Security's independent review for meaningful trust-boundary changes; invoke Financial Integrity Guardian for financial workflows. Reviewer conclusions are evidence, **not a substitute for Tech Lead acceptance**.
5. Mark exactly one decision:
   - `ACCEPTED`: scoped requirements and required available checks met; unblock dependents.
   - `REWORK`: concrete gaps found; return bounded corrections to the same owner, then review the new handoff.
   - `BLOCKED`: approval, external access, missing dependencies or protected-change authorization is needed; stop affected work.
   - `UNVERIFIED`: checks could not be completed; do not treat as accepted or claim a verified fix.

**Never advance a dependent milestone on SUBMITTED, REWORK, BLOCKED or UNVERIFIED.** Other truly independent tasks may proceed with isolated ownership. Stop retry loops after two unsuccessful review cycles; report the blocker, don't paper over failures.

## 6. End-to-end completion

Tech Lead finishes only when every in-scope task is `ACCEPTED` or explicitly reported `BLOCKED/UNVERIFIED` with clear remaining work; no silent omissions. Verify integrated behavior across boundaries after all task-level gates; report `GO`, `NO-GO` or `UNVERIFIED` honestly. Do not equate a completed subagent handoff, clean lint or successful build with a verified release.

A task can be fully completed in one Codex request through internal handoffs; this workflow does **not** require user approval between safe substeps. Existing requirements for separate explicit approval for protected finance/auth/database work, hosted data and deployment remain in force.
