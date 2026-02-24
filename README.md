# Agent Army — Project Context Handoff

## What This Project Is
A dockerizable, model-agnostic AI agent workforce for software development.
The user delegates software tasks to a team of specialized AI agents, each
powered by either Claude or GPT models via LiteLLM as the abstraction layer.

## Project Structure
```
/agent-army
  /agents
    architect.md      ← orchestrator agent, plans and delegates
    frontend.md       ← React/UI agent
    backend.md        ← API/DB/logic agent
    qa.md             ← code review and testing agent
    devops.md         ← Docker/CI/CD agent
  / [your-project]    ← agents work in any directory you specify
  orchestrate.py      ← main entry point and agent loop
  tools.py            ← write_file, read_file, run_command, list_files + schemas
  config.yaml         ← model assignments per agent
  requirements.txt    ← litellm, pyyaml, python-dotenv, rich
  Dockerfile          ← python:3.12-slim + git, curl, nodejs, npm
  docker-compose.yml  ← mounts project directories as volumes
  .env                ← API keys
  .env.example        ← committed template
```

## Key Technical Decisions
- **LiteLLM** is the model abstraction layer.
- **Flexible Workspace**: Agents can move into any directory to start building. They are no longer confined to a single `/workspace` folder.
- **Tool use loop** in `orchestrate.py` handles multi-step agentic tool calls.
- Agents communicate via context passing — architect plan is injected as context into every downstream agent
- **Volume Mounts**: Docker users should mount their target project directories into the container.

## Current Models Assigned
- architect → claude-sonnet-4-6
- backend → gpt-4o
- frontend → claude-sonnet-4-6
- qa → gpt-4o-mini
- devops → claude-haiku-4-5-20251001

## API Keys
- Sourced from `.env` via `python-dotenv`
- LiteLLM picks up `ANTHROPIC_API_KEY` and `OPENAI_API_KEY` automatically
- User has active Anthropic and OpenAI subscriptions with API access

## How the Workflow Runs
4. Selected agents run in sequence, each receiving the architect plan as context
5. Agents use tools (write_file, run_command, etc.) in an agentic loop until done
6. Optional QA pass reviews all output at the end

## Run Commands
- Local: `pip install -r requirements.txt` then `python orchestrate.py`
- Docker: `docker compose up --build`

## What Still Needs Doing / Likely Next Tasks
- Tailor agent system prompts in /agents/*.md to the user's specific stack
- Add auto-parsing of architect plan to auto-select agents (currently manual)
- Consider adding a memory layer (e.g. simple JSON or SQLite) for cross-session context
- Add a --task CLI flag so it can be run non-interactively in pipelines
- Potentially add more specialist agents (e.g. security, database migration, docs)
