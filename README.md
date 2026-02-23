# Army of Agents

A collaborative multi-agent system for software development.

## Project Structure

```
/agent-army
  /agents            # Agent definitions (.md files)
    architect.md
    frontend.md
    backend.md
    qa.md
    devops.md
  /workspace          # Workspace for agents to write code
  orchestrate.py      # Core orchestration logic
  tools.py           # Tool definitions for agents
  config.yaml        # Project configuration
  requirements.txt   # Python dependencies
  Dockerfile         # Docker configuration
  docker-compose.yml # Docker Compose configuration
  .env               # Environment variables
  .env.example       # Example environment variables
  README.md          # Project documentation
```

## Getting Started

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Configure environment variables in `.env`.
4. Run the orchestrator: `python orchestrate.py`.

Alternatively, use Docker:
`docker-compose up`