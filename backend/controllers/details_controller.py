from flask import jsonify
from models import product_model


def get_product_details(product_id):
    product = product_model.get_product_by_id(product_id) 
    # acessa o banco e retorna o produto
    if product is None:
        return jsonify({"error": "Produto não encontrado"}), 404
    return jsonify(product)


def get_product_prices(product_id):
    # chama função do model para obter preços do produto
    prices = product_model.get_product_prices(product_id)
    return jsonify(prices)
