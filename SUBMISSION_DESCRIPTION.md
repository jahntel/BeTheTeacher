# Mwangaza AI — submission description (under 300 words)

Mwangaza AI helps public-school teachers understand a learner’s progress across terms and years, rather than treating each quiz or school term in isolation. In many African public schools, evidence is scattered across assessment sheets, attendance registers, assignments, and teacher observations. When learners move between grades and teachers, important context can be lost and patterns may surface too late.

The prototype ingests source-linked evidence, retrieves a learner’s history, compares dated records, and builds a longitudinal profile with cited evidence IDs. It can flag potential patterns for teacher review and produce a plain-language draft. The system never ranks learners, diagnoses them, or assigns subject/career pathways. A named teacher must review a flagged pattern and record an approval or rejection before consequential use; the prototype does not send guardian messages automatically.

The architecture uses Pydantic AI for orchestration, a Qwen open-weights model served locally by Ollama, and a custom FastMCP server exposing tools to add evidence, build a learner profile, flag patterns for review, and retrieve a timeline. SQLite stores synthetic learner records, profile versions, review tasks, and audit logs. A community filesystem MCP server can be run separately with access restricted to the synthetic data directory.

The primary users are public-school teachers and school administrators. Learners and guardians benefit indirectly from earlier, better-informed conversations and support. The prototype prioritizes low cost, privacy, source citations, and human oversight. It currently uses synthetic records only and is not production-ready; school authentication, tamper-resistant audit storage, backups, and formal privacy review remain future work.

**Theme:** Longitudinal strength tracking, with plain-language reporting as a supporting capability.
