from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

# Configuração do Flask
app = Flask(__name__)

# ID de afiliado (modifique com o seu ID real)
AFILIADO_ID = "seu-id-afiliado"

# Função para adicionar o ID de afiliado ao link
def adicionar_afiliado(link_original):
    return f"{link_original}?tag={AFILIADO_ID}"

@app.route('/buscar', methods=['GET'])
def buscar():
    termo = request.args.get('termo')  # Termo de busca enviado pelo cliente
    url = f"https://www.amazon.com.br/s?k={termo.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    # Verifica se o request foi bem-sucedido
    if response.status_code != 200:
        return jsonify({"error": "Erro ao acessar o site da Amazon"}), 500
    
    soup = BeautifulSoup(response.text, "html.parser")

    # Lista para armazenar os produtos
    produtos = []
    for item in soup.select(".s-result-item"):
        titulo = item.select_one("h2 .a-link-normal")
        preco = item.select_one(".a-price .a-offscreen")
        imagem = item.select_one(".s-image")
        link = item.select_one("h2 .a-link-normal")

        # Verifica se todos os campos estão presentes
        if titulo and preco and imagem and link:
            produto = {
                "title": titulo.text.strip(),
                "price": preco.text.strip(),
                "image": imagem["src"],
                "link": adicionar_afiliado("https://www.amazon.com.br" + link["href"])  # Adiciona o ID de afiliado
            }
            produtos.append(produto)

    return jsonify(produtos)

if __name__ == "__main__":
    app.run(debug=True)
