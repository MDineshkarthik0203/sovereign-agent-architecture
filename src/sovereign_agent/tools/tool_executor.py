import re
from pathlib import Path

from sovereign_agent.state import AgentState
from sovereign_agent.tools.calculator import calculator
from sandbox.sandbox import Sandbox


def tool_executor(state: AgentState):

    question = state["question"]
    agent_result = state["agent_result"]

    tool_results = []
    observations = []

    execution_history = state["execution_history"].copy()

    question_lower = question.lower()


    # ============================================================
    # 1. CODE EXECUTION
    # ============================================================

    if any(
        phrase in question_lower
        for phrase in [
            "execute",
            "run the code",
            "run this code",
            "test the code",
            "test this program",
            "execute the code",
            "execute this program"
        ]
    ):

        code_blocks = re.findall(
            r"```(?:python)?\s*(.*?)```",
            agent_result,
            re.DOTALL
        )

        if not code_blocks:

            observations.append(
                "Coding task detected, but no executable Python code block was found."
            )

        else:

            sandbox = Sandbox()

            try:

                code = code_blocks[0].strip()

                print("\n[Sandbox] Executing Python code...")

                result = sandbox.call_tool(
                    "execute_code",
                    {
                        "code": code,
                        "timeout": 5
                    }
                )

                tool_results += [
                    "Sandbox Executor:",
                    f"Status: {result.get('status')}",
                    f"Output: {result.get('stdout', '')}",
                    f"Error: {result.get('stderr', '')}",
                    f"Exit Code: {result.get('exit_code')}",
                    f"Execution Time: {result.get('execution_time')}"
                ]

                if result.get("status") == "success":

                    observations.append(
                        "Python code executed successfully inside the Sandbox."
                    )

                elif result.get("status") == "timeout":

                    observations.append(
                        "Sandbox execution timed out."
                    )

                else:

                    observations.append(
                        "Sandbox execution failed."
                    )

            except Exception as e:

                tool_results.append(
                    f"Sandbox Error: {str(e)}"
                )

                observations.append(
                    "Sandbox execution raised an exception."
                )

            finally:

                sandbox.cleanup()


    # ============================================================
    # 2. FILE READING
    # ============================================================

    elif (
        ("read" in question_lower and "file" in question_lower)
        or
        ("open" in question_lower and "file" in question_lower)
        or
        ("read" in question_lower and "document" in question_lower)
    ):

        file_match = re.search(
            r"[\w./\\-]+\.(?:txt|md|pdf)",
            question,
            re.IGNORECASE
        )

        if not file_match:

            observations.append(
                "File reading was requested, but no supported file path was found."
            )

        else:

            file_path = file_match.group().strip()

            sandbox = Sandbox()

            try:

                print("\n[Sandbox] Staging input file...")

                staged = sandbox.stage_file(file_path)

                tool_results += [
                    "Sandbox File Staging:",
                    f"Status: {staged.get('status')}",
                    f"Source: {staged.get('source')}",
                    f"Sandbox Path: {staged.get('sandbox_path')}"
                ]

                print("[Sandbox] Reading file...")

                content = sandbox.call_tool(
                    "read_file",
                    {
                        "path": Path(file_path).name
                    }
                )

                document_content = content

                tool_results += [
                    "File Reader:",
                    f"File: {file_path}",
                    f"File Content:\n{document_content}"
                ]

                observations.append(
                    f"Sandbox successfully read {file_path}."
                )

                execution_history.append(
                    "Tool Executor staged and read the file using Sandbox."
                )

                return {
                    "tool_results": tool_results,
                    "document_content": document_content,
                    "observations": state["observations"] + observations,
                    "execution_history": execution_history
                }

            except Exception as e:

                tool_results.append(
                    f"Sandbox File Reader Error: {str(e)}"
                )

                observations.append(
                    "Sandbox file reading raised an exception."
                )

            finally:

                sandbox.cleanup()


    # ============================================================
    # 3. FILE WRITING + READ-BACK VERIFICATION
    # ============================================================

    elif (
        ("write" in question_lower and "file" in question_lower)
        or
        ("save" in question_lower and "file" in question_lower)
        or
        ("create" in question_lower and "file" in question_lower)
        or
        ("generate" in question_lower and "file" in question_lower)
    ):

        filename_match = re.search(
            r"[\w.-]+\.(?:txt|md|py)",
            question,
            re.IGNORECASE
        )

        filename = (
            filename_match.group().strip()
            if filename_match
            else "output.txt"
        )

        sandbox = Sandbox()

        try:

            # ----------------------------------------------------
            # WRITE
            # ----------------------------------------------------

            print("\n[Sandbox] Writing file...")

            write_result = sandbox.call_tool(
                "write_file",
                {
                    "path": filename,
                    "content": agent_result
                }
            )

            tool_results += [
                "Sandbox File Writer:",
                f"Status: {write_result.get('status')}",
                f"File: {filename}",
                f"Sandbox Result: {write_result}"
            ]

            if write_result.get("status") != "success":

                observations.append(
                    f"Sandbox failed to write {filename}."
                )

            else:

                observations.append(
                    f"Sandbox successfully wrote {filename}."
                )


                # ------------------------------------------------
                # READ BACK THE FILE
                # ------------------------------------------------

                print("[Sandbox] Reading written file back...")

                written_content = sandbox.call_tool(
                    "read_file",
                    {
                        "path": filename
                    }
                )

                tool_results += [
                    "File Reader:",
                    f"File: {filename}",
                    f"File Content:\n{written_content}"
                ]

                observations.append(
                    f"Sandbox successfully read {filename} after writing."
                )


                # ------------------------------------------------
                # CONTENT COMPARISON
                # ------------------------------------------------

                expected_content = agent_result.strip()
                actual_content = written_content.strip()

                if expected_content == actual_content:

                    tool_results.append(
                        "File Content Verification: PASS"
                    )

                    observations.append(
                        "Written file content exactly matches the generated content."
                    )

                else:

                    tool_results.append(
                        "File Content Verification: FAIL"
                    )

                    observations.append(
                        "Written file content does not match the generated content."
                    )


            execution_history.append(
                "Tool Executor wrote the file and read it back using Sandbox."
            )

        except Exception as e:

            tool_results.append(
                f"Sandbox File Writer Error: {str(e)}"
            )

            observations.append(
                "Sandbox file writing or read-back verification raised an exception."
            )

        finally:

            sandbox.cleanup()


    # ============================================================
    # 4. ARTIFACT GENERATION
    # ============================================================

    elif (
        "artifact" in question_lower
        or
        ("generate" in question_lower and "report" in question_lower)
        or
        ("create" in question_lower and "report" in question_lower)
        or
        ("generate" in question_lower and "note" in question_lower)
        or
        ("create" in question_lower and "note" in question_lower)
    ):

        sandbox = Sandbox()

        try:

            print("\n[Sandbox] Generating artifact...")

            result = sandbox.call_tool(
                "generate_artifact",
                {
                    "filename": "generated_artifact.md",
                    "content": agent_result
                }
            )

            tool_results += [
                "Sandbox Artifact Generator:",
                f"Status: {result.get('status')}",
                f"Result: {result}"
            ]

            if result.get("status") == "success":

                observations.append(
                    "Sandbox successfully generated the artifact."
                )

            else:

                observations.append(
                    "Sandbox artifact generation failed."
                )

        except Exception as e:

            tool_results.append(
                f"Sandbox Artifact Error: {str(e)}"
            )

            observations.append(
                "Sandbox artifact generation raised an exception."
            )

        finally:

            sandbox.cleanup()


    # ============================================================
    # 5. CALCULATOR
    # ============================================================

    elif any(
        word in question_lower
        for word in [
            "calculate",
            "calculation",
            "percentage",
            "average",
            "formula",
            "equation"
        ]
    ):

        expression_match = re.search(
            r"\d+(?:\s*[\+\-\*/%]\s*\d+)+",
            question
        )

        if expression_match:

            expression = expression_match.group().strip()

            result = calculator(expression)

            tool_results += [
                f"Calculator expression: {expression}",
                f"Calculator result: {result}"
            ]

            if result.startswith("Calculation error:"):

                observations.append(
                    "Calculator execution failed."
                )

            else:

                observations.append(
                    "Calculator tool executed successfully."
                )

        else:

            observations.append(
                "Calculation was requested, but no arithmetic expression was found."
            )


    # ============================================================
    # 6. DEFAULT
    # ============================================================

    else:

        observations.append(
            "No tool was required."
        )


    execution_history.append(
        "Tool Executor executed the required tool."
    )

    return {
        "tool_results": tool_results,
        "observations": state["observations"] + observations,
        "execution_history": execution_history
    }