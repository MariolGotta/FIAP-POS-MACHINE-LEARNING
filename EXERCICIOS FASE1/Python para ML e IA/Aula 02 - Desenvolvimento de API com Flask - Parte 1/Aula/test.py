import requests
from bs4 import BeautifulSoup

url = "https://olhardigital.com.br/2025/04/11/ciencia-e-espaco/cadaver-estelar-revela-passado-de-buraco-negro/"

headers = {
    "User-Agent": "Mozilla/5.0"  # Alguns sites bloqueiam requests sem user-agent
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Tenta encontrar o conteúdo da matéria
artigo = soup.find('article')

if artigo:
    paragrafos = artigo.find_all('p')
    texto = '\n'.join(p.get_text(strip=True) for p in paragrafos)
    print(f"Conteúdo:\n{texto}")
else:
    print("Não foi possível encontrar o conteúdo do artigo.")
