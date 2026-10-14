# EVALS.md — Evaluation plan and result log

**Important:** The test cases below are defined. Results are not pre-claimed. Run `python -m unittest discover -s tests -v` and fill in the actual result column before submission. The agent/model test must be run separately on a machine with Ollama and the selected model installed.

| ID | Task | Expected pass condition | Result (fill after run) |
|---|---|---|---|
| E1 | Seed synthetic learners and records | At least two synthetic learner IDs and dated evidence records exist | NOT RUN |
| E2 | Add valid evidence | New record is persisted and source reference retained | NOT RUN |
| E3 | Reject unknown learner | Evidence is not stored; clear validation error returned | NOT RUN |
| E4 | Reject invalid score | Score greater than maximum is rejected | NOT RUN |
| E5 | Build profile with multi-term records | Draft profile created with evidence IDs and descriptive patterns | NOT RUN |
| E6 | Reject review with evidence from another learner | Review task is not created | NOT RUN |
| E7 | Require named human reviewer | Approval without reviewer name is rejected | NOT RUN |
| E8 | Prevent a second decision overwrite | Decided task cannot be changed through the decision function | NOT RUN |
| E9 | Audit evidence mutation | Audit row records action, actor, timestamp, inputs, outputs | NOT RUN |
| E10 | Local open-weights full task | Qwen via Ollama runs Pydantic AI workflow, calls custom MCP timeline/profile tools, and returns evidence IDs | NOT RUN |
| E11 | Borrowed filesystem MCP server | Server starts scoped to `./data` and can list/read only permitted demo files | NOT RUN |

## Failure not yet fixed / next experiment
**Known risk to test:** Pydantic AI and MCP APIs evolve quickly, and the local agent integration may need a small compatibility adjustment for the exact installed package versions. If E10 fails, capture the traceback, pin a compatible Pydantic AI release, and verify the `MCPServerStdio`/`toolsets` API against that installed version. Do not substitute a hosted closed model and call it an open-weights run.

## Safety evaluation notes
- No automated pathway assignment is implemented.
- Profile patterns are descriptive thresholds, not validated psychometric measurements.
- Teacher review is required before consequential use; the prototype does not send guardian messages.
- All provided records are synthetic.
