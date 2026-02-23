import yaml
import os

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def run_orchestrator():
    config = load_config()
    print(f"Starting orchestration for project: {config['project_name']}")
    # TODO: Implement agent execution logic

if __name__ == "__main__":
    run_orchestrator()
