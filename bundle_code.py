import os

output_file = "codigo_completo.txt"
extensiones = (".py", ".bat", ".json", ".spec")  # Modifica según lo que quieras incluir

with open(output_file, "w", encoding="utf-8") as outfile:
    for root, dirs, files in os.walk("."):
        # Ignorar carpetas virtuales o temporales
        dirs[:] = [d for d in dirs if d not in ("venv", ".git", "__pycache__", "build", "dist")]
        for file in files:
            if file.endswith(extensiones) and file != output_file:
                path = os.path.join(root, file)
                outfile.write(f"\n{'='*40}\nARCHIVO: {path}\n{'='*40}\n\n")
                try:
                    with open(path, "r", encoding="utf-8") as infile:
                        outfile.write(infile.read())
                except Exception as e:
                    outfile.write(f"Error al leer archivo: {e}\n")

print(f"Código consolidado en {output_file}")