import pdfkit
from io import BytesIO

html = "<html><body><h1>Test Resume</h1><p>PDF works!</p><style>body { background: linear-gradient(to right, #667eea, #764ba2); color: white; }</style></body></html>"

options = {'page-size': 'A4', 'print-media-type': None}
pdf_bytes = pdfkit.from_string(html, False, options=options)

if pdf_bytes:
    with open("test.pdf", "wb") as f:
        f.write(pdf_bytes)
    print("✅ PDF generated successfully! Check test.pdf")
else:
    print("❌ Failed—check wkhtmltopdf installation.")