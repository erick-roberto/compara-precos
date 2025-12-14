"""
Controller PRODUTO - Controle de Funções Comuns de Produtos

Responsabilidades:
- Processar requisições de listagem geral de produtos
- Processar requisições de busca externa (simulada)
- Fornecer funções comuns para outros controllers

Relacionamentos:
- Interage com o Model PRODUTO para recuperação de dados
- Interage com o Model OFERTA para informações de preços
"""

from flask import jsonify, request
from models import product_model
import random
from datetime import datetime

# listagem de todos os produtos
def get_products():
    """
    Retorna todos os produtos do sistema
    
    Requisição:
        GET /api/products
    
    Respostas:
        200: Lista de todos os produtos
    """
    products = product_model.get_all_products()
    return jsonify(products)

"""
Controller PRODUTO - Controle de Funções Comuns de Produtos

Responsabilidades:
- Processar requisições de listagem geral de produtos
- Processar requisições de busca externa (simulada)
- Fornecer funções comuns para outros controllers

Relacionamentos:
- Interage com o Model PRODUTO para recuperação de dados
- Interage com o Model OFERTA para informações de preços
"""

from flask import jsonify, request
from models import product_model
import random
from datetime import datetime


def get_products():
    """
    Retorna todos os produtos do sistema
    
    Requisição:
        GET /api/products
    
    Respostas:
        200: Lista de todos os produtos
    """
    products = product_model.get_all_products()
    return jsonify(products)



'''
def external_search():
    """
    Busca produtos em lojas externas (simulada)
    
    Requisição:
        GET /api/external-search?q=termo
    
    Parâmetros:
        q (str): Termo de busca
    
    Respostas:
        200: Lista de resultados de busca externa
        400: Parâmetro de busca obrigatório
    """
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "O parâmetro de busca (q) é obrigatório"}), 400
    results = []
    stores = ["Amazon", "Magazine Luiza"]
    for store in stores:
        for _ in range(random.randint(1, 3)):
            base_price = random.uniform(50.0, 5000.0)
            price = round(base_price + random.uniform(-100.0, 100.0), 2)
            if price < 0:
                price = round(base_price, 2)
            product_name = f"{query.title()} - Modelo {random.randint(100, 999)}"
            product_url = f"https://www.{store.lower().replace(' ', '')}.com.br/search?q={query.replace(' ', '+')}"
            results.append({
                "id": f"{store.lower()}-{random.randint(1000, 9999)}",
                "product_name": product_name,
                "store_name": store,
                "price": price,
                "url": product_url,
                "last_updated": datetime.utcnow().isoformat() + "Z",
            })
    results.sort(key=lambda x: x["price"])
    return jsonify(results)
    
'''