import os
import sys
import importlib.util
from ai.tool_loader import get_tools, reload_tools
from ai.brain import ask
from speech.speak import speak

# Intentar importar la función de selección desde ai.tool_selector
try:
    from ai.tool_selector import select_tool
except ImportError:
    try:
        from ai.tool_selector import select_tool_with_ai as select_tool
    except ImportError:
        try:
            from ai.tool_selector import choose_tool as select_tool
        except ImportError:
            def select_tool(user_input, available_tools):
                prompt = f"""
You are the Tool Selection Module for A.R.G.O.S.
Analyze the user command and select the appropriate tool.

Available tools: {list(available_tools.keys())}
User command: "{user_input}"

Rules:
1. Return ONLY the exact tool name if an existing tool fits.
2. Return 'NEED_SELF_CREATION' if no existing tool can perform the task.
3. Return 'CONVERSATION' for casual chat.
"""
                try:
                    res = ask(prompt)
                    if res:
                        return res.strip().replace("`", "").replace("'", "").replace('"', '')
                except Exception:
                    pass
                return "NEED_SELF_CREATION"


def load_and_run_module(tool_name, user_input):
    """
    Carga e importa dinámicamente el archivo .py recién creado desde el disco
    y ejecuta su función run(user_input) sin reiniciar el programa.
    """
    tools_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tools")
    file_path = os.path.join(tools_dir, f"{tool_name}.py")

    if not os.path.exists(file_path):
        print(f"[A.R.G.O.S. Error] File not found: {file_path}")
        return None

    try:
        # Cargar el módulo dinámicamente
        spec = importlib.util.spec_from_file_location(tool_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "run"):
            print(f"[A.R.G.O.S.] Executing newly created module '{tool_name}'...")
            return module.run(user_input)
        else:
            print(f"[A.R.G.O.S. Error] Module '{tool_name}' has no run() function.")
    except Exception as e:
        print(f"[A.R.G.O.S. Error] Failed to execute module '{tool_name}': {e}")
    return None


def process(user_input):
    if not user_input:
        return ""

    cleaned_input = str(user_input).strip()

    print("\n" + "=" * 55)
    print(f"[A.R.G.O.S.] Processing command: '{cleaned_input}'")

    # 1. Cargar herramientas instaladas
    tools = get_tools()
    print("[A.R.G.O.S.] Searching installed tools via ai.tool_loader...")
    print(f"[A.R.G.O.S.] Loaded tools: {list(tools.keys())}")

    # 2. Seleccionar la herramienta
    print("[A.R.G.O.S.] Evaluating command with tool selector...")
    try:
        selected_tool_name = select_tool(cleaned_input, tools)
    except Exception as e:
        print(f"[A.R.G.O.S. Error] Tool selection exception: {e}")
        selected_tool_name = "NEED_SELF_CREATION"

    print(f"[A.R.G.O.S.] Tool chosen: '{selected_tool_name}'")

    # 3. Intentar ejecutar la herramienta si ya existe
    if selected_tool_name in tools:
        tool = tools[selected_tool_name]
        if hasattr(tool, "run"):
            try:
                print(f"[A.R.G.O.S.] Executing existing tool '{selected_tool_name}'...")
                result = tool.run(cleaned_input)
                if result:
                    return result
            except Exception as e:
                print(f"[A.R.G.O.S. Error] Failed executing '{selected_tool_name}': {e}")

    # 4. PROTOCOLO DE AUTOCREACIÓN Y EJECUCIÓN EN CALIENTE (Sin Reinicio)
    if selected_tool_name not in tools and selected_tool_name not in ["CONVERSATION", "CHAT"]:
        print(f"[A.R.G.O.S.] Tool '{selected_tool_name}' not found. Initiating Automatic Self-Creation...")

        tool_creator = tools.get("tool_creator")
        if tool_creator and hasattr(tool_creator, "run"):
            print("[A.R.G.O.S.] Invoking 'tool_creator' module...")
            created_tool_name = tool_creator.run(cleaned_input)

            if created_tool_name and "Failed" not in created_tool_name and "Error" not in created_tool_name:
                tools_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tools")
                file_path = os.path.join(tools_dir, f"{created_tool_name}.py")

                # Mostrar el código generado en consola
                if os.path.exists(file_path):
                    print(f"\n--- [File {created_tool_name}.py Created] ---")
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            print(f.read())
                    except Exception as e:
                        print(f"Could not read generated file: {e}")
                    print("-" * 45 + "\n")

                # Actualizar el diccionario de herramientas en memoria
                reload_tools()

                # Ejecutar la nueva herramienta inmediatamente sin reiniciar
                print(f"[A.R.G.O.S.] Executing '{created_tool_name}' instantly...")
                speak(f"Created {created_tool_name}. Executing now.")
                
                result = load_and_run_module(created_tool_name, cleaned_input)
                if result:
                    return result
                return f"Successfully created and executed {created_tool_name}."
            else:
                print("[A.R.G.O.S. Error] Self-creation protocol failed.")

    # 5. Fallback a conversación general con ai.brain (Ollama)
    print("[A.R.G.O.S.] Redirecting query to ai.brain (Ollama)...")
    try:
        response = ask(cleaned_input)
        if response:
            return response
    except Exception as e:
        print(f"[A.R.G.O.S. Error] Brain execution error: {e}")

    return "Could not process the request."