from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs


def detectar_xss(url, html):
    soup = BeautifulSoup(html, "html.parser")

    resultados = {
        "url": url,
        "nivel": "baixo",
        "indicadores": []
    }

    # 1. Analisa parâmetros presentes na URL
    parsed_url = urlparse(url)
    parametros = parse_qs(parsed_url.query)

    for parametro in parametros:
        resultados["indicadores"].append({
            "tipo": "URL_PARAMETER",
            "parametro": parametro,
            "descricao": "Parâmetro encontrado na URL."
        })

    # 2. Procura campos de entrada
    for campo in soup.find_all(["input", "textarea"]):
        nome = campo.get("name")

        if nome:
            resultados["indicadores"].append({
                "tipo": "INPUT",
                "parametro": nome,
                "descricao": "Campo de entrada encontrado."
            })

    # 3. Procura formulários
    for form in soup.find_all("form"):
        action = form.get("action", "")
        method = form.get("method", "GET").upper()

        resultados["indicadores"].append({
            "tipo": "FORM",
            "action": action,
            "method": method,
            "descricao": "Formulário encontrado. Pode receber entrada controlada pelo usuário."
        })

    # 4. Procura sinks JavaScript comuns
    sinks = [
        "innerHTML",
        "outerHTML",
        "document.write",
        "eval("
    ]

    scripts = soup.find_all("script")

    for script in scripts:
        if not script.string:
            continue

        codigo = script.string

        for sink in sinks:
            if sink in codigo:
                resultados["indicadores"].append({
                    "tipo": "JAVASCRIPT_SINK",
                    "sink": sink,
                    "descricao": "Uso de um sink JavaScript que merece análise."
                })

    # Define nível baseado na quantidade de indicadores
    quantidade = len(resultados["indicadores"])

    if quantidade >= 5:
        resultados["nivel"] = "alto"
    elif quantidade >= 2:
        resultados["nivel"] = "médio"

    return resultados


if __name__ == "__main__":

    url = input("DIGITE URL  OU  IP:")

    import requests

    resposta = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "Security-Web-Crawler/1.0"
        }
    )

    resultado = detectar_xss(url, resposta.text)

    print("\n=== XSS DETECTOR ===")
    print(f"URL: {resultado['url']}")
    print(f"Nível: {resultado['nivel']}")

    print("\nIndicadores encontrados:")

    for item in resultado["indicadores"]:
        print(f"\n[{item['tipo']}]")

        for chave, valor in item.items():
            if chave != "tipo":
                print(f"{chave}: {valor}")