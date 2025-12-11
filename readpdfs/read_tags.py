import pikepdf

def recorrer(elemento, nivel=0, archivo=None, visitados=None):
    if visitados is None:
        visitados = set()

    # Evitar ciclos infinitos por referencia circular
    oid = id(elemento)
    if oid in visitados:
        archivo.write("  " * nivel + "(referencia repetida)\n")
        return
    visitados.add(oid)

    if nivel == 10: 
        archivo.write("  " * nivel + "(nivel máximo alcanzado)\n")
        return

    indent = "  " * nivel
    archivo.write(f"{indent}{elemento}\n")

    if isinstance(elemento, pikepdf.Dictionary):
        for k, v in elemento.items():
            archivo.write(f"{indent}- {k}:\n")
            recorrer(v, nivel + 1, archivo, visitados)

    elif isinstance(elemento, pikepdf.Array):
        for v in elemento:
            recorrer(v, nivel + 1, archivo, visitados)


pdf = pikepdf.Pdf.open("archivo.pdf")

with open("estructura_pdf.txt", "w", encoding="utf-8") as f:
    if "/StructTreeRoot" in pdf.Root:
        struct_tree = pdf.Root["/StructTreeRoot"]
        f.write("=== StructTreeRoot ===\n")
        recorrer(struct_tree, archivo=f)
    else:
        f.write("El PDF no tiene estructura etiquetada (no es PDF/UA).\n")
