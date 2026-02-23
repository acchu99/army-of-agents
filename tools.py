def google_search(query):
    """Perform a Google search."""
    print(f"Searching for: {query}")
    return "Search results for " + query

def write_file(path, content):
    """Write content to a file."""
    with open(path, "w") as f:
        f.write(content)
    print(f"File written to: {path}")

def read_file(path):
    """Read content from a file."""
    with open(path, "r") as f:
        return f.read()
