import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def buscar_pagina(url):
    resposta = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "security-web-Crawler/1.0"
        }
    )

    resposta.raise_for_status()

    return resposta.text


def encontra_links(url, html):
    soup = BeautifulSoup(html, "html.parser")

    links = set()

    for tag in soup.find_all("a", href=True):
        link = urljoin(url, tag["href"])
        links.add(link)

    return links


if __name__ == "__main__":
    
    url = input("Digite a URL ou IP: ")

    html = buscar_pagina(url)
    links = encontra_links(url, html)

    print(f"[+] Página analisada: {url}")
    print(f"[+] Links encontrados: {len(links)}")

    for link in links:
        print(f"-> {link}")