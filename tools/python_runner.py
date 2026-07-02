import os
import sys
import time
import tempfile
import subprocess

from langchain.tools import tool

from config import WORKSPACE


@tool
def check_syntax(code: str) -> dict:
    """
    Check whether Python code is syntactically valid.
    """

    try:
        compile(code, "<agent>", "exec")

        return {
            "success": True,
            "message": "Syntax OK"
        }

    except SyntaxError as e:

        return {
            "success": False,
            "message": str(e)
        }


@tool
def run_python(
    code: str,
    timeout: int = 30
) -> dict:
    """
    Execute Python code inside a temporary script.

    Returns:
        success
        stdout
        stderr
        return_code
        execution_time
    """

    start = time.perf_counter()

    temp_file = None

    try:

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8"
        ) as f:

            f.write(code)
            temp_file = f.name

        result = subprocess.run(
            [sys.executable, temp_file],
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        end = time.perf_counter()

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode,
            "execution_time": round(end - start, 3),
        }

    except subprocess.TimeoutExpired:

        end = time.perf_counter()

        return {
            "success": False,
            "stdout": "",
            "stderr": f"Execution timed out after {timeout} seconds.",
            "return_code": -1,
            "execution_time": round(end - start, 3),
        }

    except Exception as e:

        end = time.perf_counter()

        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "return_code": -1,
            "execution_time": round(end - start, 3),
        }

    finally:

        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)