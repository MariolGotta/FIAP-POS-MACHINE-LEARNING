import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

class BookScrapper:
    def __init__(self):
        self.urlbase = 'http://books.toscrape.com/'
        self.catalogue_base = self.urlbase + 'catalogue/'
        self.dados_livros = []

    def get_categorias(self):
        """Coleta os links de todas as categorias disponíveis no site."""
        response = requests.get(self.urlbase)
        soup = BeautifulSoup(response.text, "html.parser")
        categorias = soup.select("ul.nav.nav-list ul li a")
        links = {cat.text.strip(): self.urlbase + cat['href'] for cat in categorias}
        return links

    def get_total_paginas(self, soup):
        """Retorna o número total de páginas de uma categoria."""
        paginacao = soup.select_one("li.current")
        if paginacao:
            match = re.search(r'Page \d+ of (\d+)', paginacao.text.strip())
            return int(match.group(1)) if match else 1
        return 1

    def extrair_livros_pagina(self, soup, categoria):
        """Extrai os dados de cada livro em uma página."""
        livros = soup.select("article.product_pod")
        for livro in livros:
            nome = livro.h3.a["title"]
            preco = livro.select_one(".price_color").text.strip()
            estrelas = livro.select_one("p.star-rating")["class"][1]  # ex: "Three"
            self.dados_livros.append({
                "nome": nome,
                "preco": preco,
                "estrelas": estrelas,
                "categoria": categoria
            })

    def processar_categoria(self, categoria_nome, categoria_url):
        """Processa todas as páginas de uma categoria."""
        response = requests.get(categoria_url)
        soup = BeautifulSoup(response.text, "html.parser")
        total_paginas = self.get_total_paginas(soup)

        for pagina in range(1, total_paginas + 1):
            if pagina == 1:
                url_pagina = categoria_url
            else:
                # Substitui "index.html" por "page-X.html" na URL da categoria
                url_pagina = re.sub(r'index\.html$', f'page-{pagina}.html', categoria_url)

            print(f"Baixando: {url_pagina}")
            response = requests.get(url_pagina)
            soup = BeautifulSoup(response.text, "html.parser")
            self.extrair_livros_pagina(soup, categoria_nome)

    def rodar(self):
        """Executa o scraper para todas as categorias."""
        categorias = self.get_categorias()
        for nome, url in categorias.items():
            self.processar_categoria(nome, url)

    def montar_dataframe(self):
        """Monta o DataFrame final com os dados extraídos."""
        df = pd.DataFrame(self.dados_livros)
        return df

# ----------------------------
# EXECUÇÃO
# ----------------------------

if __name__ == "__main__":
    scraper = BookScrapper()
    scraper.rodar()
    df = scraper.montar_dataframe()

    print(df.head())  # Mostra os 5 primeiros livros
    print("\nLivros por categoria:")
    print(df['categoria'].value_counts())

    # Se quiser salvar o DataFrame:
    # df.to_csv("livros_scrapeados.csv", index=False)
