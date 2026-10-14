# Under-3-minute demo run sheet

Record an unedited run with tool calls visible. Use synthetic records only.

1. **0:00–0:20 — Problem and data:** Show the app and say learner evidence is fragmented across terms. Point out the synthetic-data warning.
2. **0:20–0:45 — Timeline:** Select `K-104` and show source IDs, terms, scores, and observations.
3. **0:45–1:10 — Add evidence:** Add the synthetic example from `data/sample_new_evidence.json` through the form. Show validation and the source reference.
4. **1:10–1:35 — Agent/MCP:** In a separate terminal, run `python -m mwangaza.agent --learner K-104` with Ollama running. Show tool calls and the returned cited profile. If this fails, do not fake the result; fix it or clearly demonstrate the MCP server directly and state the AI integration is pending verification.
5. **1:35–2:05 — Profile:** Build/refresh the profile and open source evidence for a pattern. Explain that the thresholds are prototype heuristics, not a diagnosis.
6. **2:05–2:35 — Human approval:** Flag a pattern, enter a named demo reviewer, and approve/reject with a note. Show that the decision is logged and guardian sharing is not automatic.
7. **2:35–2:55 — Audit and close:** Show audit log and summarize open-source local model, custom MCP tools, borrowed filesystem server, and human-in-the-loop safeguards.
