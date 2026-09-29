from urllib.parse import urlparse, parse_qs


def analisar_parametros(url):
    resultado = {
        "url": url,
        "parametros": [],
        "quantidade": 0
    }

    parsed_url = urlparse(url)
    parametros = parse_qs(parsed_url.query)

    for nome, valores in parametros.items():

        for valor in valores:
            resultado["parametros"].append({
                "nome": nome,
                "valor": valor,
                "tipo": "GET"
            })

    resultado["quantidade"] = len(resultado["parametros"])

    return resultado


def exibir_resultado(resultado):

    print("\n=== PARAMETER ANALYZER ===")
    print(f"URL: {resultado['url']}")
    print(f"Parâmetros encontrados: {resultado['quantidade']}")

    if not resultado["parametros"]:
        print("\n[-] Nenhum parâmetro encontrado.")
        return

    print("\n[PARÂMETROS]")

    for parametro in resultado["parametros"]:
        print(
            f"  Nome: {parametro['nome']} | "
            f"Valor: {parametro['valor']} | "
            f"Tipo: {parametro['tipo']}"
        )


if __name__ == "__main__":
    xss= "search?q=teste&page=1"
    url = input("Url:",xss) 
    

    resultado = analisar_parametros(url)

    exibir_resultado(resultado)