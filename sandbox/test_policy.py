from pathlib import Path

from policy import SandboxPolicy


workspace = Path("my_workspace")
workspace.mkdir(exist_ok=True)

policy = SandboxPolicy(workspace)


inside = workspace / "test.txt"
outside = workspace / ".." / "secret.txt"


print("Inside allowed:", policy.is_path_allowed(inside))
print("Outside allowed:", policy.is_path_allowed(outside))
