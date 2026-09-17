class ToolSchema:

    def __init__(self, required_args=None, optional_args=None):
        self.required_args = set(required_args or [])
        self.optional_args = set(optional_args or [])

    def validate(self, args):
        if not isinstance(args, dict):
            raise TypeError(
                "Tool arguments must be a dictionary"
            )

        allowed_args = (
            self.required_args |
            self.optional_args
        )

        # Check required arguments
        missing_args = (
            self.required_args - args.keys()
        )

        if missing_args:
            raise ValueError(
                f"Missing required arguments: "
                f"{sorted(missing_args)}"
            )

        # Check unexpected arguments
        unexpected_args = (
            set(args.keys()) - allowed_args
        )

        if unexpected_args:
            raise ValueError(
                f"Unexpected arguments: "
                f"{sorted(unexpected_args)}"
            )

        return True