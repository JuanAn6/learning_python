import pikepdf

pdf = pikepdf.Pdf.open("archivo.pdf")

tree = pdf.Root.get("/StructTreeRoot")

def dump_tags(nodo, out, nivel=0):
    indent = "  " * nivel

    if isinstance(nodo, pikepdf.Dictionary):
        s = nodo.get("/S")

        if s:
            out.write(f"{indent}Etiqueta: {s}\n")
            out.write(f"{indent}K = {nodo.get('/K')}\n")

        k = nodo.get("/K")

        if isinstance(k, pikepdf.Array):
            for child in k:
                dump_tags(child, out, nivel + 1)

        elif isinstance(k, pikepdf.Dictionary):
            dump_tags(k, out, nivel + 1)


# === Guardar salida en archivo ===
with open("check_content.txt", "w", encoding="utf-8") as out:

    if tree is None:
        out.write("El PDF no tiene /StructTreeRoot (no está etiquetado).\n")
    else:
        out.write("=== DUMP DE ETIQUETAS ===\n\n")
        dump_tags(tree, out)

print("Salida guardada en check_content.txt")
