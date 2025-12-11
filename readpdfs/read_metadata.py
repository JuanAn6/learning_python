from pypdf import PdfReader

reader = PdfReader("archivo.pdf")
metadata = reader.metadata

for clave, valor in metadata.items():
    print(f"{clave}: {valor}")
