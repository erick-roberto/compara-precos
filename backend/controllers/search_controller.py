from flask import jsonify, request
from models import product_model
import unicodedata
import re

def _normalize_search_term(term):
    if not term:
        return ""
    term = term.lower()
    term = ''.join(
        c for c in unicodedata.normalize('NFD', term)
        if unicodedata.category(c) != 'Mn'
    )
    term = re.sub(r'[^\w\s]', '', term)
    term = ' '.join(term.split())
    return term


def _validate_search_term(term):
    if not term or len(term.strip()) == 0:
        return False, None, "Termo de busca não pode estar vazio"

    normalized = _normalize_search_term(term)
    useful_chars = len(normalized.replace(' ', ''))

    if useful_chars < 2:
        return False, None, "Termo deve conter pelo menos 2 caracteres úteis"

    return True, normalized, None



def search_products():
    """
    Busca produtos por termo e/ou categoria
    """

    q = request.args.get("q")
    category = request.args.get("category")

    # ----------------------------
    # VALIDAR TERMO DE BUSCA
    # ----------------------------
    if q:
        ok, normalized_q, error = _validate_search_term(q)
        if not ok:
            return jsonify({"error": error}), 400
        q = normalized_q

    products = product_model.search_products(q, category)
    return jsonify(products), 200


# ---------------------------------------------------------
# CONTROLLER - CATEGORIAS
# ---------------------------------------------------------
def get_categories():
    """
    Retorna todas as categorias de produtos disponíveis
    """
    categories = product_model.get_all_categories()
    return jsonify(categories), 200
