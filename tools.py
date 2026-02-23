import subprocess
import os

def write_file(path: str, content: str) -> str:
    dir_path = os.path.dirname(path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    return f"✅ Written: {path}"

def read_file(path: str) -> str:
    if not os.path.exists(path):
        return f"❌ File not found: {path}"
    with open(path) as f:
        return f.read()

def run_command(command: str) -> str:
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True,
            text=True, timeout=60
        )
        output = result.stdout + result.stderr
        return output if output else "Command ran with no output."
    except subprocess.TimeoutExpired:
        return "❌ Command timed out after 60s"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def list_files(directory: str = ".") -> str:
    result = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.venv']]
        for file in files:
            result.append(os.path.join(root, file))
    return "\n".join(result) if result else "No files found."

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write or overwrite a file with the given content",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative file path"},
                    "content": {"type": "string", "description": "Full file content"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Execute a shell command and return output",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string"}
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List all files in a directory recursively",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {"type": "string", "default": "."}
                },
                "required": []
            }
        }
    }
]

TOOL_MAP = {
    "write_file": write_file,
    "read_file": read_file,
    "run_command": run_command,
    "list_files": list_files
}