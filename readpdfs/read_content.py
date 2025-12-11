import pikepdf
from pikepdf import Dictionary, Array
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

# Etiquetas que queremos extraer
TAGS_INTERES = {"/H1", "/H2", "/H3", "/P"}

def extraer_mcids_por_pagina(ruta_pdf):
    """Extrae el texto asociado a cada MCID en cada página del PDF."""
    estructura = []

    for pagina in extract_pages(ruta_pdf):
        mcids = {}
        for elemento in pagina:
            if isinstance(elemento, LTTextContainer):
                for t in elemento:
                    if hasattr(t, "mcid") and t.mcid is not None:
                        mcids.setdefault(t.mcid, "")
                        mcids[t.mcid] += t.get_text()
        estructura.append(mcids)

    return estructura


def recorrer_tags(nodo, resultados, mcids_por_pagina):
    """Recorre la estructura lógica del PDF y extrae contenido de las etiquetas."""
    if not isinstance(nodo, (Dictionary, Array)):
        return

    tipo = nodo.get("/S")
    if tipo in TAGS_INTERES and "/K" in nodo:
        contenido = extraer_contenido_de_tag(nodo, mcids_por_pagina)
        resultados.append((tipo, contenido))

    hijos = nodo.get("/K")
    if isinstance(hijos, Array):
        for h in hijos:
            recorrer_tags(h, resultados, mcids_por_pagina)
    elif isinstance(hijos, Dictionary):
        recorrer_tags(hijos, resultados, mcids_por_pagina)


def extraer_contenido_de_tag(nodo, mcids_por_pagina):
    """Obtiene el texto asociado a un nodo estructural usando MCID."""
    k = nodo.get("/K")

    if isinstance(k, Dictionary):
        mcid = k.get("/MCID")
        pagina = k.get("/Pg")

        if mcid is not None and pagina is not None:
            # Número de página basado en el objeto
            num_pag = pagina.objgen[0] - 1
            if 0 <= num_pag < len(mcids_por_pagina):
                return mcids_por_pagina[num_pag].get(mcid, "")

    return ""


# ========== EJECUCIÓN ==========

archivo_entrada = "archivo.pdf"
archivo_salida = "read_output.txt"

pdf = pikepdf.Pdf.open(archivo_entrada)

with open(archivo_salida, "w", encoding="utf-8") as out:

    if "/StructTreeRoot" not in pdf.Root:
        out.write("El PDF no tiene etiquetas de accesibilidad (no es PDF/UA).\n")
        print("El PDF no tiene estructura etiquetada.")
        exit()

    out.write("=== Estructura etiquetada del PDF ===\n\n")

    # Texto por MCID
    mcids_por_pagina = extraer_mcids_por_pagina(archivo_entrada)

    # Extraer etiquetas y contenido
    resultados = []
    recorrer_tags(pdf.Root["/StructTreeRoot"], resultados, mcids_por_pagina)

    if not resultados:
        out.write("No se encontraron etiquetas relevantes.\n")
        print("No se encontraron etiquetas relevantes.")
    else:
        for tag, contenido in resultados:
            out.write(f"{tag}:\n{contenido.strip()}\n\n")

print("Output generado en read_output.txt")
