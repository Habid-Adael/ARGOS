from ai.brain import ask


class Debugger:

    def fix(self, candidate, result):

        prompt = f"""
The following Python program failed.

Return ONLY corrected Python code.

Error:

{result.stderr}

Code:

{candidate["code"]}
"""

        repaired = ask(prompt)

        candidate["code"] = repaired

        return candidate