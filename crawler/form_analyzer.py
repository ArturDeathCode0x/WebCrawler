from bs4 import BeautifulSoup
from urllib.parse import urljoin


def analisar_formularios(url, html):

    soup = BeautifulSoup(html, "html.parser")

    resultado = {
        "url": url,
        "formularios": [],
        "quantidade": 0
    }

    for numero, form in enumerate(soup.find_all("form"), start=1):

        action = form.get("action", "")
        method = form.get("method", "GET").upper()

        action_url = urljoin(url, action)

        campos = []

        # INPUT
        for campo in form.find_all("input"):

            campos.append({
                "tag": "input",
                "name": campo.get("name"),
                "type": campo.get("type", "text"),
                "value": campo.get("value")
            })

        # TEXTAREA
        for campo in form.find_all("textarea"):

            campos.append({
                "tag": "textarea",
                "name": campo.get("name"),
                "type": "textarea",
                "value": campo.text.strip()
            })

        # SELECT
        for campo in form.find_all("select"):

            opcoes = []

            for option in campo.find_all("option"):
                opcoes.append({
                    "value": option.get("value"),
                    "text": option.text.strip()
                })

            campos.append({
                "tag": "select",
                "name": campo.get("name"),
                "type": "select",
                "options": opcoes
            })

        formulario = {
            "id": numero,
            "action": action_url,
            "method": method,
            "campos": campos
        }

        resultado["formularios"].append(formulario)

    resultado["quantidade"] = len(resultado["formularios"])

    return resultado


def exibir_resultado(resultado):

    print("\n=== FORM ANALYZER ===")
    print(f"URL: {resultado['url']}")
    print(f"Formulários encontrados: {resultado['quantidade']}")

    if not resultado["formularios"]:
        print("\n[-] Nenhum formulário encontrado.")
        return

    for formulario in resultado["formularios"]:

        print(f"\n[FORM #{formulario['id']}]")
        print(f"Action: {formulario['action']}")
        print(f"Method: {formulario['method']}")

        print("\nCampos:")

        for campo in formulario["campos"]:

            print(
                f"  {campo['tag']} | "
                f"name={campo['name']} | "
                f"type={campo['type']}"
            )


if __name__ == "__main__":

    import requests

    url = input("Digite a URL ou IP: ")

    resposta = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "Security-Web-Crawler/1.0"
        }
    )

    resultado = analisar_formularios(
        url,
        resposta.text
    )

    exibir_resultado(resultado)