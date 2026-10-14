# Mwangaza AI

**Every learner has a story. Make the patterns visible.**

Mwangaza AI is a privacy-first prototype for helping public-school teachers connect learning evidence across terms and years. It uses synthetic learner records, a SQLite evidence store, an MCP server, and an optional local Qwen model through Ollama. It surfaces evidence-backed patterns for teacher review; it does not diagnose, rank learners, or automatically assign academic/career pathways.

## Status and honest scope

This repository is a runnable prototype scaffold. The local database, three custom MCP tools, Streamlit dashboard, audit trail, review queue, approval checks, seeded synthetic data, and evaluation cases are implemented. The AI workflow is implemented as an optional Pydantic AI + Ollama + MCP integration and requires local setup/testing on your machine. The borrowed filesystem MCP server is configured as an optional integration; it requires Node.js/npm and is not needed for the core demo. Do not claim a live model run or passing evaluations until you run them and record the results.

## Requirements

- Windows 10/11, Python 3.11 or 3.12
- Internet access for initial Python package installation
- Optional: [Ollama](https://ollama.com/) and a model such as `qwen2.5:3b` (download size and performance depend on model)
- Optional borrowed MCP server: Node.js LTS/npm, to run `@modelcontextprotocol/server-filesystem`
- No Docker and no paid API key required

## Quick start (PowerShell)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m mwangaza.store --seed
streamlit run app.py
```

Open the local URL printed by Streamlit. The dashboard uses synthetic data only. If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process Bypass` in that terminal, then activate again.

## Optional local AI setup

1. Install Ollama from https://ollama.com/.
2. In PowerShell run `ollama pull qwen2.5:3b` and ensure Ollama is running.
3. Install project requirements as above.
4. Run the agent workflow:

```powershell
python -m mwangaza.agent --learner K-104 --evidence-file data/sample_new_evidence.json
```

The agent connects to the custom MCP server over stdio and uses the local Ollama OpenAI-compatible endpoint. If your installed Pydantic AI version reports an API mismatch, see `docs/IMPLEMENTATION_STATUS.md`; the dashboard and MCP server can still be demonstrated independently. Model output is a draft for teacher review, not a verdict.

## MCP server

Run the custom server directly:

```powershell
python -m mwangaza.mcp_server
```

It exposes:
- `add_learning_evidence`: validate and persist a synthetic learning evidence item.
- `build_learner_profile`: compute descriptive patterns from longitudinal evidence and update a draft profile.
- `flag_pattern_for_review`: create an auditable review item.
- `get_learner_timeline`: retrieve chronological evidence.

The server stores data in `mwangaza.db` in the project directory by default. Set `MWANGAZA_DB` to use a different path.

## Borrowed MCP server

We reuse the community MCP filesystem server instead of rewriting general file access. With Node.js installed, launch it from the project root, restricted to the synthetic data folder:

```powershell
npx -y @modelcontextprotocol/server-filesystem .\data
```

This is an independent server process. The sample agent's core workflow does not depend on it; the filesystem integration is an optional evidence-import route. Never grant it access to folders containing real student records unless an authorized deployment has reviewed the privacy implications.

## Human approval and privacy

- Synthetic data only; do not import real children's records into this prototype.
- Profile patterns are provisional and source-linked.
- Guardian sharing/pathway recommendations are not automatic. A named teacher must approve a review item in the dashboard before it can be marked approved.
- Audit records include action, input/output summaries, timestamp, and actor. This demo's actor field is not production-grade authentication; do not expose it to the public internet.
- The prototype is not a production student information system and does not implement school identity-provider integration, encryption-at-rest policy, backups, or legal/compliance review.

## Evaluations

See `EVALS.md` and run:

```powershell
python -m unittest discover -s tests -v
```

Test results should be recorded from your actual run before submission. Do not report unrun tests as passing.

## Repository contents

- `app.py` — Streamlit teacher dashboard
- `mwangaza/store.py` — SQLite persistence, profile logic, audit log, review approvals
- `mwangaza/mcp_server.py` — custom FastMCP server
- `mwangaza/agent.py` — optional Pydantic AI agent connected to MCP + local Ollama
- `data/` — synthetic records only
- `ARCHITECTURE.md`, `EVALS.md`, `docs/` — submission documentation

## License

MIT. See `LICENSE`.
