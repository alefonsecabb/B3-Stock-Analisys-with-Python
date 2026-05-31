import markdown
import re
import os
from xhtml2pdf import pisa

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MD_FILE  = os.path.join(BASE_DIR, "trabalho_mongodb_clinica_vet.md")
PDF_FILE = os.path.join(BASE_DIR, "trabalho_mongodb_clinica_vet.pdf")

with open(MD_FILE, encoding="utf-8") as f:
    md_content = f.read()

html_body = markdown.markdown(
    md_content,
    extensions=["tables", "fenced_code"],
)

# Remove H1 e bloco de metadados — substituídos pela capa
html_body = re.sub(r'<h1[^>]*>.*?</h1>', '', html_body, count=1, flags=re.DOTALL)
html_body = re.sub(
    r'<p>\s*<strong>(?:Alunos?|Curso|Disciplina|Professor):</strong>.*?</p>\s*',
    '', html_body, flags=re.DOTALL
)
# Remove h2 "Sistema de Gestão..." que vinha logo após o H1
html_body = re.sub(
    r'<h2[^>]*>Sistema de Gest[^<]*</h2>\s*',
    '', html_body, count=1, flags=re.DOTALL
)

# Adiciona classe "even" em linhas pares de cada tabela (xhtml2pdf não suporta nth-child)
def add_even_class(match):
    tbody = match.group(0)
    rows = re.split(r'(?=<tr)', tbody)
    result = []
    row_idx = 0
    for part in rows:
        if part.startswith('<tr'):
            if row_idx % 2 == 1:
                part = part.replace('<tr>', '<tr class="even">', 1)
            row_idx += 1
        result.append(part)
    return ''.join(result)

html_body = re.sub(r'<tbody>.*?</tbody>', add_even_class, html_body, flags=re.DOTALL)

CSS = """
@page {
    size: A4;
    margin: 2.8cm 2.5cm 3.0cm 2.5cm;
    @frame footer {
        -pdf-frame-content: footer_content;
        bottom: 1.0cm;
        margin-left: 2.5cm;
        margin-right: 2.5cm;
        height: 0.8cm;
    }
}

body {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.65;
    color: #1a1a1a;
}

/* ── CAPA ── */
.capa {
    text-align: center;
}
.capa-barra-topo {
    background-color: #1e3a5f;
    height: 10pt;
    margin-bottom: 60pt;
}
.capa-titulo {
    font-size: 18pt;
    font-weight: bold;
    color: #1e3a5f;
    line-height: 1.35;
    margin-bottom: 10pt;
}
.capa-subtitulo {
    font-size: 13pt;
    font-weight: bold;
    color: #2d6a9f;
    margin-bottom: 50pt;
}
.capa-separador {
    border-top: 1px solid #ccd3e0;
    margin: 0 0 0 0;
}
.capa-meta {
    font-size: 10.5pt;
    color: #333;
    line-height: 2.3;
    padding: 14pt 0;
    border-top: 1px solid #ccd3e0;
    border-bottom: 1px solid #ccd3e0;
}
.capa-barra-base {
    background-color: #1e3a5f;
    height: 10pt;
    margin-top: 60pt;
}

/* ── HEADINGS ── */
h2 {
    font-size: 13pt;
    font-weight: bold;
    color: #1e3a5f;
    margin-top: 24pt;
    margin-bottom: 9pt;
    padding-bottom: 5pt;
    border-bottom: 2px solid #1e3a5f;
    -pdf-keep-with-next: true;
}
h3 {
    font-size: 11pt;
    font-weight: bold;
    color: #2d6a9f;
    margin-top: 16pt;
    margin-bottom: 7pt;
    -pdf-keep-with-next: true;
}
h4 {
    font-size: 10.5pt;
    font-weight: bold;
    color: #2a5080;
    margin-top: 12pt;
    margin-bottom: 5pt;
    -pdf-keep-with-next: true;
}

/* ── PARÁGRAFOS ── */
p {
    margin-bottom: 8pt;
    text-align: justify;
}

/* ── CÓDIGO INLINE ── */
code {
    font-family: Courier, "Courier New", monospace;
    font-size: 8.5pt;
    background-color: #eef1f7;
    color: #1a3a5c;
    padding: 1pt 3pt;
}

/* ── BLOCOS DE CÓDIGO ── */
pre {
    background-color: #f4f6f9;
    border: 1px solid #ccd3e0;
    border-left: 4px solid #2d6a9f;
    padding: 10pt 12pt;
    margin: 8pt 0 14pt 0;
    font-size: 8pt;
    font-family: Courier, "Courier New", monospace;
    line-height: 1.5;
    overflow: hidden;
}
pre code {
    background-color: transparent;
    padding: 0;
    font-size: 8pt;
    color: #1a2a3a;
}

/* ── TABELAS ── */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 10pt 0 16pt 0;
    font-size: 9pt;
}
th {
    background-color: #1e3a5f;
    color: #ffffff;
    padding: 7pt 9pt;
    text-align: left;
    font-weight: bold;
}
td {
    padding: 6pt 9pt;
    border-bottom: 1px solid #ccd3e0;
    vertical-align: top;
}
tr.even td { background-color: #f0f4fa; }

/* ── LISTAS ── */
ul, ol {
    margin: 5pt 0 9pt 18pt;
}
li { margin-bottom: 3pt; }

/* ── BLOCKQUOTE ── */
blockquote {
    background-color: #fff8e1;
    border-left: 4px solid #f0b429;
    padding: 8pt 12pt;
    margin: 8pt 0 12pt 0;
    font-size: 9.5pt;
    color: #5a4000;
}

/* ── HR ── */
hr {
    border: none;
    border-top: 1px solid #ccd3e0;
    margin: 18pt 0;
}

/* ── RODAPÉ ── */
#footer_content {
    text-align: center;
    font-size: 8pt;
    color: #888;
    border-top: 1px solid #ccd3e0;
    padding-top: 3pt;
}
"""

CAPA_HTML = """
<div class="capa">
  <div class="capa-barra-topo"></div>
  <p class="capa-titulo">Trabalho Pr&aacute;tico<br/>Banco de Dados N&atilde;o Relacional com MongoDB</p>
  <p class="capa-subtitulo">Sistema de Gest&atilde;o de Cl&iacute;nica Veterin&aacute;ria</p>
  <div class="capa-meta">
    <strong>Alunos:</strong>&nbsp; Alexandre da Fonseca &nbsp;/&nbsp; Riquelmy Henrique Silva &nbsp;/&nbsp; Carlos Eduardo Pereira de Rezende<br/>
    <strong>Curso:</strong>&nbsp; Ci&ecirc;ncia de Dados &ndash; FATEC<br/>
    <strong>Disciplina:</strong>&nbsp; Banco de Dados N&atilde;o Relacionais<br/>
    <strong>Professor:</strong>&nbsp; Higor Antonio Delsoto
  </div>
  <div class="capa-barra-base"></div>
</div>
<pdf:nextpage/>
"""

FOOTER_HTML = """
<div id="footer_content">
  Trabalho Pr&aacute;tico &ndash; BD N&atilde;o Relacional &ndash; FATEC
  &nbsp;|&nbsp;
  P&aacute;gina <pdf:pagenumber/> de <pdf:pagecount/>
</div>
"""

FULL_HTML = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"/>
<title>Trabalho – MongoDB Clínica Veterinária</title>
<style>{CSS}</style>
</head>
<body>
{FOOTER_HTML}
{CAPA_HTML}
{html_body}
</body>
</html>"""

print("Gerando PDF…")
with open(PDF_FILE, "wb") as out_f:
    result = pisa.CreatePDF(FULL_HTML.encode("utf-8"), dest=out_f)

if result.err:
    print(f"Erros durante geração: {result.err}")
else:
    size_kb = os.path.getsize(PDF_FILE) // 1024
    print(f"PDF salvo: {PDF_FILE}  ({size_kb} KB)")
