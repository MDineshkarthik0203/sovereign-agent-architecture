import subprocess
import sys
import tempfile
import os


def code_executor(files: dict) -> dict:
    """
    Execute a multi-file Python project in a temporary directory.

    Example:
        files = {
            "divide_by_zero.py": "...",
            "test_divide_by_zero.py": "..."
        }
    """

    temp_dir = tempfile.mkdtemp()

    try:
        # Create all files
        for filename, code in files.items():

            file_path = os.path.join(temp_dir, filename)

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(code)

        # Find the main/test Python file
        python_files = list(files.keys())

        if not python_files:
            return {
                "success": False,
                "output": "",
                "error": "No Python files were provided."
            }

        # Prefer test files
        test_file = next(
            (
                filename
                for filename in python_files
                if filename.startswith("test_")
            ),
            python_files[0]
        )

        file_path = os.path.join(temp_dir, test_file)

        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=temp_dir
        )

        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": "Execution timed out."
        }

    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e)
        }

    finally:
        # Remove temporary directory
        try:
            for root, dirs, files_list in os.walk(
                temp_dir,
                topdown=False
            ):
                for filename in files_list:
                    os.remove(os.path.join(root, filename))

                for dirname in dirs:
                    os.rmdir(os.path.join(root, dirname))

            os.rmdir(temp_dir)

        except Exception:
            pass