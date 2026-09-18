from workspace import SandboxWorkspace


workspace = SandboxWorkspace()

path = workspace.create()

print("Workspace created:")
print(path)

print("Exists:", path.exists())

workspace.cleanup()

print("Exists after cleanup:", path.exists())