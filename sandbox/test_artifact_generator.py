from artifact_generator import ArtifactGenerator
from workspace import SandboxWorkspace


workspace_manager = SandboxWorkspace()
workspace_path = workspace_manager.create()

try:
    generator = ArtifactGenerator(
        workspace_path
    )

    # Test artifact generation
    result = generator.generate_text(
        "report.txt",
        "Sandbox artifact generation works!"
    )

    print("GENERATE:", result)

    # Verify the artifact exists
    artifact_path = workspace_path / "report.txt"

    print(
        "EXISTS:",
        artifact_path.exists()
    )

    # Verify the content
    print(
        "CONTENT:",
        artifact_path.read_text(
            encoding="utf-8"
        )
    )

    # Test path traversal protection
    try:
        generator.generate_text(
            "../escape.txt",
            "This should be blocked."
        )

        print("SECURITY TEST FAILED")

    except PermissionError as e:
        print(
            "SECURITY TEST PASSED:",
            e
        )

finally:
    workspace_manager.cleanup()