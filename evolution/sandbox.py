import os
import subprocess
import tempfile
from dataclasses import dataclass


@dataclass
class SandboxResult:

    success: bool

    stdout: str

    stderr: str

    return_code: int


class Sandbox:

    def test(self, candidate):

        code = candidate["code"]

        with tempfile.TemporaryDirectory() as temp:

            file = os.path.join(temp, "candidate.py")

            with open(file, "w", encoding="utf-8") as f:
                f.write(code)

            result = subprocess.run(
                ["python", file],
                capture_output=True,
                text=True,
                timeout=20
            )

            return SandboxResult(
                success=result.returncode == 0,
                stdout=result.stdout,
                stderr=result.stderr,
                return_code=result.returncode
            )
        