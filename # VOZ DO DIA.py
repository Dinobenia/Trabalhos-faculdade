#                                VOZ DO DIA

#Coleta notícias do site G1.
#Salva essas notícias em um banco de dados SQLite.
#Atribui um “peso” de popularidade simulada às notícias.
#Gera um gráfico de barras horizontais com esses dados.




#----------------------------Importando bibliotecas----------------------------
import requests #faz requisições HTTP
from bs4 import BeautifulSoup #extrai dados do HTML (estático)
import sqlite3 #cria e manipular banco de dados local.
import matplotlib.pyplot as plt #gerar gráfico




#----------------------------nome do arquivo do banco de dados----------------------------
DB_NAME = "noticias_g1.db"




#----------------------------Criação do banco de dados----------------------------
def criar_banco():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS noticias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT,
                link TEXT UNIQUE,
                peso INTEGER,
                data_coleta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
#Essa função cria um banco de dados chamado noticias_g1.db com uma tabela chamada noticias, contendo:
#titulo: título da notícia.
#link: URL da notícia (único).
#peso: um número que simula a popularidade.
#data_coleta: data e hora da coleta.




#----------------------------Salvar notícias no banco----------------------------
def salvar_noticias_no_banco(noticias):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.executemany('''
            INSERT OR IGNORE INTO noticias (titulo, link, peso) VALUES (?, ?, ?)
        ''', noticias) #insere as notícias, ignorando duplicatas (links repetidos)
        conn.commit()
    print("\n✅ Notícias salvas no banco de dados com sucesso!")
#Essa função recebe uma lista de tuplas com (titulo, link, peso) e salva no banco. 
#Usa INSERT OR IGNORE para evitar duplicatas (mesmo link).




#----------------------------Buscar notícias do G1----------------------------
#Essa função:
def buscar_noticias_g1(limit=10):
    url = "https://g1.globo.com/" #Acessa o site do G1.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        } #simula um navegador

    try:
        response = requests.get(url, headers=headers, timeout=10) #acessa a página
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Erro ao acessar o G1: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser') 
    noticias = soup.find_all('a', class_='feed-post-link', limit=limit) #extrai as informações
    noticias_com_peso = []
    
    #Extrai os títulos e links das últimas notícias (até o limite definido). Terminal.
    print("\n📰 Últimas notícias do G1:\n") 
    for i, noticia in enumerate(noticias, start=1):
        titulo = noticia.get_text(strip=True)
        link = noticia.get('href') #extrai link

        if not link:
            continue

        peso = limit - i + 1 #Atribui um peso decrescente (a primeira notícia tem peso maior).
        print(f"{i}. {titulo}\n 🔗 {link}\n")
        noticias_com_peso.append((titulo, link, peso)) #Adiciona na lista

    return noticias_com_peso #Retorna uma lista de tuplas com (titulo, link, peso).




#----------------------------Gerar gráfico----------------------------
def gerar_grafico_noticias(noticias): #Cria um gráfico de barras horizontais com os títulos e pesos.
    titulos = [t[0][:40] + ('...' if len(t[0]) > 40 else '') for t in noticias] 
    pesos = [t[2] for t in noticias]

    plt.figure(figsize=(13, 8)) #tamanho da figura
    bars = plt.barh(titulos[::-1], pesos[::-1], color='pink') #gráfico horizontais
    plt.xlabel("Popularidade simulada")
    plt.title("Popularidade simulada das últimas notícias do G1")
    plt.tight_layout()

    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.1, bar.get_y() + bar.get_height()/2, str(int(width)), va='center')

    plt.show()
#Usa matplotlib para exibir o gráfico.




#-------------------- EXECUÇÃO -----------------------
if __name__ == "__main__":
    criar_banco() #Cria o banco.
    noticias = buscar_noticias_g1(limit=10) #Busca as notícias.
    if noticias:
        salvar_noticias_no_banco(noticias) #Salva no banco.
        gerar_grafico_noticias(noticias) #Gera o gráfico.