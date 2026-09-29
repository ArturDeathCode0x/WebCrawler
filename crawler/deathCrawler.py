from analyzer import  analisar_pagina
from crawler import buscar_pagina
from form_analyzer import analisar_formularios , exibir_resultado
from parameter_analyzer import analisar_parametros
from xss_detector import detectar_xss
import sys
import time
menu = """
\033[91m

████  █████  ███  █████ █   █     ███  ████   ███  █   █ █     █████ ████  
█   █ █     █   █   █   █   █    █     █   █ █   █ █   █ █     █     █   █ 
█   █ ████  █████   █   █████    █     ████  █████ █ █ █ █     ████  ████  
█   █ █     █   █   █   █   █    █     █  █  █   █ ██ ██ █     █     █  █  
████  █████ █   █   █   █   █     ███  █   █ █   █ █   █ █████ █████ █   █ 



-----------------------------------------------------
[1] Analisar página
[2] Buscar página
[3] Analisar formulários
[4] Analisar parâmetros
[5] Detectar XSS
[0] Sair

"""

print(menu)

entrada = input("Digite sua opção: ")

match entrada:

    case "1":
        url = input("URL: ")

        resultado = analisar_pagina(url)

        print(resultado)


    case "2":
        url = input("URL: ")

        html = buscar_pagina(url)

        print(html)


    case "3":
        url = input("URL: ")

        html = buscar_pagina(url)

        resultado = analisar_formularios(url, html)

        exibir_resultado(resultado)


    case "4":
        url = input("URL: ")

        resultado = analisar_parametros(url)

        exibir_resultado(resultado)


    case "5":
        url = input("URL: ")

        html = buscar_pagina(url)

        resultado = detectar_xss(url, html)

        print("\n=== XSS DETECTOR ===")
        print(f"URL: {resultado['url']}")
        print(f"Nível: {resultado['nivel']}")

        print("\nIndicadores encontrados:")

        for item in resultado["indicadores"]:
            print(f"\n[{item['tipo']}]")

            for chave, valor in item.items():
                if chave != "tipo":
                    print(f"{chave}: {valor}")


    case "0":
        print("Saindo...")


    case _:
        print("Opção inválida!")
