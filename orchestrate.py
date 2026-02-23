import json
import yaml
import os
from litellm import completion
from tools import TOOLS_SCHEMA, TOOL_MAP
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

load_dotenv()
console = Console()

with open("config.yaml") as f:
    CONFIG = yaml.safe_load(f)

def load_prompt(path: str) -> str:
    with open(path) as f:
        return f.read()

def run_agent(agent_name: str, task: str, context: str = "") -> str:
    agent_cfg = CONFIG["agents"][agent_name]
    model = agent_cfg["model"]
    system = load_prompt(agent_cfg["system_prompt"])
    full_task = f"{context}\n\nTask: {task}".strip()

    console.print(Panel(f"[bold cyan]{agent_name.upper()}[/] [{model}]\n{task[:120]}..."))

    messages = [{"role": "user", "content": full_task}]

    while True:
        response = completion(
            model=model,
            messages=messages,
            tools=TOOLS_SCHEMA,
            tool_choice="auto",
            system=system,
        )

        msg = response.choices[0].message
        messages.append(msg)

        if not msg.tool_calls:
            return msg.content or ""

        for tool_call in msg.tool_calls:
            fn_name = tool_call.function.name
            fn_args = json.loads(tool_call.function.arguments)
            console.print(f"  🔧 [yellow]{fn_name}[/] → {list(fn_args.keys())}")

            result = TOOL_MAP[fn_name](**fn_args)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

def main():
    console.print(Panel("[bold green]🤖 Agent Army — Software Dev Workflow[/]"))
    goal = Prompt.ask("\n[bold]What do you want to build?[/]")

    # 1. Architect plans
    plan = run_agent("architect", goal)
    console.print(Panel(plan, title="📋 Architect Plan"))

    if not Confirm.ask("\nProceed with this plan?"):
        console.print("Aborted.")
        return

    # 2. Run agents based on what's in the plan
    available = list(CONFIG["agents"].keys())
    available.remove("architect")

    console.print(f"\nAvailable agents: {', '.join(available)}")
    selected = Prompt.ask("Which agents to run? (comma-separated, or 'all')")

    if selected.strip().lower() == "all":
        agents_to_run = available
    else:
        agents_to_run = [a.strip() for a in selected.split(",") if a.strip() in available]

    # 3. Run each agent with the plan as context
    results = {}
    for agent in agents_to_run:
        result = run_agent(
            agent,
            f"Implement your portion of the plan below.",
            context=f"## Architect Plan\n{plan}"
        )
        results[agent] = result
        console.print(Panel(result, title=f"✅ {agent.upper()} done"))

    # 4. QA reviews everything if not already run
    if "qa" not in agents_to_run and Confirm.ask("\nRun QA review on all output?"):
        all_context = f"## Architect Plan\n{plan}\n\n"
        for agent, result in results.items():
            all_context += f"## {agent.upper()} Output\n{result}\n\n"
        qa_result = run_agent("qa", "Review all code written by the other agents.", context=all_context)
        console.print(Panel(qa_result, title="🔍 QA Report"))

    console.print("\n[bold green]✅ Workflow complete. Check /workspace for output files.[/]")

if __name__ == "__main__":
    main()