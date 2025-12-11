import pikepdf
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

# Etiquetas que nos interesan
TAGS_INTERES = {"/H1", "/H2", "/H3", "/P", "/Title", "/TextBody"}

def extraer_texto_por_pagina(ruta_pdf):
    """Devuelve una lista con todo el texto por página."""
    paginas_texto = []
    for pagina in extract_pages(ruta_pdf):
        texto_pag = []
        for elem in pagina:
            if isinstance(elem, LTTextContainer):
                texto_pag.append(elem.get_text().strip())
        paginas_texto.append("\n".join(texto_pag))
    return paginas_texto


def recorrer_tags(nodo, resultados, nivel=0):
    """Recorre el árbol de etiquetas y construye salida heurística."""
    if not isinstance(nodo, (pikepdf.Dictionary, pikepdf.Array)):
        return

    tipo_obj = nodo.get("/S")
    tipo = str(tipo_obj) if tipo_obj is not None else None
    k = nodo.get("/K")

    if tipo in TAGS_INTERES:
        resultados.append(("  " * nivel + tipo, "(contenido visible)"))

    if isinstance(k, pikepdf.Array):
        for child in k:
            recorrer_tags(child, resultados, nivel + 1)
    elif isinstance(k, pikepdf.Dictionary):
        recorrer_tags(k, resultados, nivel + 1)


# === Configuración ===
archivo_entrada = "archivo.pdf"
archivo_salida = "read_output.txt"

pdf = pikepdf.Pdf.open(archivo_entrada)
tree = pdf.Root.get("/StructTreeRoot")

with open(archivo_salida, "w", encoding="utf-8") as out:
    if tree is None:
        out.write("El PDF no tiene estructura etiquetada.\n")
    else:
        out.write("=== ETIQUETAS DEL PDF (heurística) ===\n\n")

        resultados = []
        recorrer_tags(tree, resultados)

        out.write("=== CONTENIDO DEL PDF (heurística) ===\n\n")
        # Extraemos texto de todas las páginas
        texto_paginas = extraer_texto_por_pagina(archivo_entrada)

        # Ahora escribimos todo de forma ordenada
        for idx, (tag, _) in enumerate(resultados):
            out.write(f"{tag}:\n")
            if idx < len(texto_paginas):
                out.write(texto_paginas[idx] + "\n\n")
            else:
                out.write("(sin texto asignado)\n\n")

print("Extracción completa. Revisa read_output.txt")
