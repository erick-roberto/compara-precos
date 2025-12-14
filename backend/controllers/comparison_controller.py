from flask import jsonify, request
from models import product_model


def compare_products():

    data = request.get_json() # extração dos dados da requisição
    product_ids = data.get("product_ids") # extração dos IDs dos produtos
    if not product_ids or not isinstance(product_ids, list) or not all(isinstance(i, int) for i in product_ids):
        return jsonify({"error": "IDs de produtos são obrigatórios e devem ser uma lista de inteiros"}), 400
    
    # chama função do model para comparar produtos
    comparison = product_model.compare_products(product_ids) 
    # envia para o model a lista de IDs dos produtos para comparação
    return jsonify(comparison)
    # retorna o objeto retornado pelo model para um JSON válido

