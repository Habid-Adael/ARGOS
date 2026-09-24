import os
import re
from ai.brain import ask

TOOLS_DIR = os.path.dirname(__file__)

TOOL_CREATOR_PROMPT = """
You are the Tool Generation Module for A.R.G.O.S.
Your task is to write a production-ready Python script to satisfy the requested user capability.

STRICT PYTHON CODE RULES:
1. ALWAYS import all necessary Python standard library modules at the VERY TOP of the file (e.g., `import os`, `import sys`, `import subprocess`, `import urllib`, `import json`, `import webrowser`).
2. The code MUST define an entry-point function called `run(user_input)`.
3. The `run(user_input)` function MUST return a string describing the outcome or output.
4. Keep the code self-contained, robust, and clean. Wrap execution logic in try-except blocks where appropriate.
5. Do NOT wrap your output in markdown explanations, conversational text, or preamble. Output ONLY valid Python code inside ```python ``` blocks or directly as code.

User request: {user_input}
"""

def clean_python_code(raw_text):
    """
    Extracts pure Python code from LLM output, stripping markdown formatting.
    """
    # Look for code wrapped in ```python ... ```
    match = re.search(r"```python\s*(.*?)\s*```", raw_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # Fallback for generic code blocks ``` ... ```
    match = re.search(r"```\s*(.*?)\s*```", raw_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    return raw_text.strip()


def run(user_input):
    """
    Generates a new tool file based on user request and saves it to the tools directory.
    """
    print(f"\n[Tool Creator] Generating code for: '{user_input}'")
    
    prompt = TOOL_CREATOR_PROMPT.format(user_input=user_input)
    raw_code = ask(prompt)
    
    code = clean_python_code(raw_code)
    
    if not code or "def run(" not in code:
        print("[Tool Creator Error] Generated code was invalid or missing run() function.")
        return "Failed to generate valid tool code."

    # Extract or infer a clean tool name (e.g., openspotify)
    clean_name = re.sub(r"[^a-zA-Z0-9]", "", user_input.lower().replace("create tool", "").replace("open", "open_").strip())
    if not clean_name:
        clean_name = "generated_tool"
    
    # Format filename
    file_name = f"{clean_name}.py"
    file_path = os.path.join(TOOLS_DIR, file_name)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"[Tool Creator] New tool saved at: {file_path}")
        return clean_name
    except Exception as e:
        print(f"[Tool Creator Error] Failed to write tool file: {e}")
        return "Error saving tool file."