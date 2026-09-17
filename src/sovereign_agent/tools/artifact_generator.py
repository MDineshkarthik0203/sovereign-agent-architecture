import os


def generate_markdown_artifact(
    filename: str,
    content: str
) -> str:
    """
    Create a Markdown artifact in the current workspace.
    """

    if not filename.endswith(".md"):
        filename += ".md"

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)

        return f"Artifact created successfully: {os.path.abspath(filename)}"

    except Exception as e:
        return f"Artifact creation failed: {str(e)}"