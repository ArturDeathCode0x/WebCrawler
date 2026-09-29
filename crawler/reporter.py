import json
import os
from datetime import datetime


def gerar_json(resultado, arquivo="data/results.json"):
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)

    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(
            resultado,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"[+] JSON criado: {arquivo}")


def gerar_html(resultado, arquivo="reports/report.html"):
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)

    indicadores = resultado.get("xss", {}).get("indicadores", [])

    html = f"""
<!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <title>Security Web Crawler - Report</title>

    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background: #f4f4f4;
        }}

        .container {{
            max-width: 1000px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
        }}

        h1 {{
            margin-bottom: 5px;
        }}

        .box {{
            padding: 15px;
            margin: 15px 0;
            border: 1px solid #ddd;
            border-radius: 8px;
        }}

        .indicator {{
            padding: 10px;
            margin: 8px 0;
            background: #f5f5f5;
            border-radius: 5px;
        }}

        code {{
            background: #eee;
            padding: 3px 5px;
        }}
    </style>
</head>

<body>

<div class="container">

<h1>Security Web Crawler</h1>

<p>
<strong>Data:</strong>
{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
</p>

<div class="box">
<h2>Alvo</h2>
<p>{resultado.get("url", "N/A")}</p>
</div>

<div class="box">
<h2>Resumo</h2>

<p>
<strong>Formulários:</strong>
{resultado.get("forms", {}).get("quantidade", 0)}
</p>

<p>
<strong>Parâmetros:</strong>
{resultado.get("parameters", {}).get("quantidade", 0)}
</p>

<p>
<strong>Indicadores XSS:</strong>
{len(indicadores)}
</p>

<p>
<strong>Nível:</strong>
{resultado.get("xss", {}).get("nivel", "N/A")}
</p>

</div>

<div class="box">

<h2>Indicadores de XSS</h2>
"""

    if not indicadores:
        html += """
<p>Nenhum indicador encontrado.</p>
"""

    else:
        for indicador in indicadores:

            html += '<div class="indicator">'

            for chave, valor in indicador.items():

                html += (
                    f"<p><strong>{chave}:</strong> "
                    f"<code>{valor}</code></p>"
                )

            html += "</div>"

    html += """
</div>

<div class="box">

<h2>Observação</h2>

<p>
Os resultados deste relatório representam indicadores
encontrados durante a análise automatizada e não constituem,
isoladamente, confirmação de vulnerabilidade.
</p>

</div>

</div>

</body>
</html>
"""

    with open(arquivo, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[+] Relatório HTML criado: {arquivo}")


def gerar_relatorio(resultado):
    gerar_json(resultado)
    gerar_html(resultado)


if __name__ == "__main__":

    exemplo = {
        "url": "http://127.0.0.1:5000",

        "forms": {
            "quantidade": 1
        },

        "parameters": {
            "quantidade": 2
        },

        "xss": {
            "nivel": "médio",
            "indicadores": [
                {
                    "tipo": "INPUT",
                    "parametro": "q",
                    "descricao": "Campo de entrada encontrado."
                }
            ]
        }
    }

    gerar_relatorio(exemplo)