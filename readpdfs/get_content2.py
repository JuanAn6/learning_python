import pikepdf

pdf = pikepdf.Pdf.open("archivo.pdf")
tree = pdf.Root.get("/StructTreeRoot")

content = []

def dump_tags_completo(nodo, out, nivel=0):
    indent = "  " * nivel

    if isinstance(nodo, pikepdf.Dictionary):
        s = nodo.get("/S")
        s_str = str(s) if s else "(sin etiqueta)"
        out.write(f"{indent}Etiqueta: {s_str}\n")
        k_obj = nodo.get("/K")
        #out.write(f"{indent}K = {str(k_obj)}\n")
        if isinstance(k_obj, pikepdf.Array):
            out.write(f"{indent}  Array:\n")
            tag_save = { "tag" : s_str }
            for i, child in enumerate(k_obj):
                out.write(f"{indent}    [{i}] {child}\n")
                tag_save["pos"] = child
            content.append(tag_save) 
        elif isinstance(k_obj, pikepdf.Dictionary):
            out.write(f"{indent}  Diccionario: {k_obj}\n")
        else:
            out.write(f"{indent}  Otro: {k_obj}\n")

        k = nodo.get("/K")
        if isinstance(k, pikepdf.Array):
            for child in k:
                dump_tags_completo(child, out, nivel + 1)
        elif isinstance(k, pikepdf.Dictionary):
            dump_tags_completo(k, out, nivel + 1)

with open("check_content_full.txt", "w", encoding="utf-8") as out:
    if tree is None:
        out.write("El PDF no tiene /StructTreeRoot.\n")
    else:
        out.write("=== DUMP COMPLETO DE ETIQUETAS ===\n\n")
        dump_tags_completo(tree, out)

print(content)
print("Salida guardada en check_content_full.txt")
