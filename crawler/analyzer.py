import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def analisar_pagina(url):
    resposta = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "Security-Web-Crawler/1.0"
        }
    )

    resposta.raise_for_status()

    soup = BeautifulSoup(resposta.text, "html.parser")

    resultado = {
        "url": url,
        "forms": [],
        "inputs": [],
        "links": [],
        "scripts": []
    }

    # Analisa formulários
    for form in soup.find_all("form"):
        resultado["forms"].append({
            "action": urljoin(url, form.get("action", "")),
            "method": form.get("method", "GET").upper()
        })

    # Analisa campos de entrada
    for campo in soup.find_all(["input", "textarea", "select"]):
        resultado["inputs"].append({
            "tag": campo.name,
            "name": campo.get("name"),
            "type": campo.get("type", "text")
        })

    # Analisa links
    for link in soup.find_all("a", href=True):
        resultado["links"].append(
            urljoin(url, link["href"])
        )

    # Analisa JavaScript
    for script in soup.find_all("script"):
        resultado["scripts"].append({
            "src": script.get("src"),
            "inline": script.get("src") is None
        })

    return resultado


if __name__ == "__main__":
    url = input("Digite a URL ou IP: ")

    resultado = analisar_pagina(url)

    print(f"\n[+] URL: {resultado['url']}")

    print("\n[FORMULÁRIOS]")
    for form in resultado["forms"]:
        print(f"  Action: {form['action']}")
        print(f"  Method: {form['method']}")

    print("\n[INPUTS]")
    for campo in resultado["inputs"]:
        print(
            f"  {campo['tag']} | "
            f"name={campo['name']} | "
            f"type={campo['type']}"
        )

    print("\n[LINKS]")
    for link in resultado["links"]:
        print(f"  -> {link}")

    print("\n[SCRIPTS]")
    for script in resultado["scripts"]:
        print(
            f"  src={script['src']} | "
            f"inline={script['inline']}"
        )