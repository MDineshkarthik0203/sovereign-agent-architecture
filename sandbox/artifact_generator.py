from pathlib import Path


class ArtifactGenerator:

    def __init__(self, workspace_path: Path):
        self.workspace_path = Path(
            workspace_path
        ).resolve()

    def generate_text(
        self,
        filename: str,
        content: str
    ):
        artifact_path = (
            self.workspace_path / filename
        ).resolve()

        # Prevent writing outside the workspace
        try:
            artifact_path.relative_to(
                self.workspace_path
            )
        except ValueError:
            raise PermissionError(
                "Artifact path is outside sandbox workspace"
            )

        artifact_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        artifact_path.write_text(
            content,
            encoding="utf-8"
        )

        return {
            "status": "success",
            "artifact": str(artifact_path),
            "size": artifact_path.stat().st_size
        }
        