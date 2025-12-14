"""
Model PRODUTO - Entidade de Dados para Produtos do Sistema

Responsabilidades:
- Gerenciar dados de produtos
- Persistência e recuperação de dados de produtos
- Busca e filtragem de produtos
- Comparação de produtos

Atributos da Entidade PRODUTO:
- ID: Identificador único do produto
- Nome: Nome do produto
- Descrição: Descrição detalhada do produto
- categoria: Categoria do produto
- data de criação: Quando o produto foi criado
- imagem_URL: URL da imagem do produto

Relacionamentos:
- Um produto pode ter múltiplas ofertas (OFERTA)
- Um produto pertence a uma categoria

Casos de Uso:
- Pesquisar Produto (Cliente): Busca de produtos por termo e/ou categoria
- Visualizar Comparação de Preços (Cliente): Comparação de preços entre lojas
- Visualizar Detalhes do Produto (Cliente): Exibição de detalhes e ofertas
"""

from .base_model import get_db
from .offer_model import (
    get_offers_by_product,
    calculate_price_range
)


def get_all_products():
    """
    Retorna todos os produtos com preços agregados
    """
    db = get_db()
    data = db.get_data()
    
    products = []
    for product in data['products']:
        price_range = calculate_price_range(product['id'])
        
        products.append({
            'id': product['id'],
            'name': product['name'],
            'description': product['description'],
            'category': product['category'],
            'image_url': product['image_url'],
            'created_at': product['created_at'],
            'min_price': price_range['min_price'],
            'max_price': price_range['max_price'],
            'store_count': price_range['store_count']
        })
    
    return products


def search_products(q=None, category=None):
    """
    Busca produtos por termo e/ou categoria
    """
    db = get_db()
    data = db.get_data()
    
    results = []
    for product in data['products']:
        # Filtrar por termo de busca
        if q:
            q_lower = q.lower()
            if not (q_lower in product['name'].lower() or q_lower in product['description'].lower()):
                continue
        
        # Filtrar por categoria
        if category and product['category'] != category:
            continue
        
        price_range = calculate_price_range(product['id'])
        
        results.append({
            'id': product['id'],
            'name': product['name'],
            'description': product['description'],
            'category': product['category'],
            'image_url': product['image_url'],
            'created_at': product['created_at'],
            'min_price': price_range['min_price'],
            'max_price': price_range['max_price'],
            'store_count': price_range['store_count']
        })
    
    return results


def get_product_by_id(product_id):
    """
    Retorna um produto específico pelo ID
    """
    db = get_db()
    data = db.get_data()
    
    for product in data['products']:
        if product['id'] == product_id:
            return {
                'id': product['id'],
                'name': product['name'],
                'description': product['description'],
                'category': product['category'],
                'image_url': product['image_url'],
                'created_at': product['created_at']
            }
    return None


def get_product_prices(product_id):
    """
    Retorna todas as ofertas de um produto usando o OfferModel
    """
    return get_offers_by_product(product_id)


def get_all_categories():
    """
    Retorna todas as categorias únicas de produtos
    """
    db = get_db()
    data = db.get_data()
    
    categories = {product['category'] for product in data['products'] if product['category']}
    return sorted(list(categories))


def compare_products(product_ids):
    """
    Compara múltiplos produtos com todas as suas ofertas
    """
    comparison = []
    
    for product_id in product_ids:
        product = get_product_by_id(product_id)
        if not product:
            continue
        
        offers = get_offers_by_product(product_id)
        
        comparison.append({
            **product,
            'prices': offers
        })
    
    return comparison
