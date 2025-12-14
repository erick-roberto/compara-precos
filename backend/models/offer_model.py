"""
Model OFERTA - Entidade de Dados para Ofertas de Produtos

Responsabilidades:
- Gerenciar ofertas de produtos em lojas parceiras
- Persistência e recuperação de dados de ofertas
- Cálculos relacionados a preços e comparações

Atributos da Entidade OFERTA:
- ID: Identificador único da oferta
- product_id: Referência ao produto
- store_name: Nome da loja parceira
- Preço: Valor do produto na loja
- URL_Redirecionamento: Link para a loja parceira
- last_updated: Última atualização da oferta

Relacionamentos:
- Uma oferta pertence a um PRODUTO
- Uma oferta está associada a uma loja (representada pelo store_name)

Casos de Uso:
- Visualizar Comparação de Preços (Cliente): Comparação de preços entre lojas
- Visualizar Detalhes do Produto (Cliente): Exibição de detalhes e ofertas
"""

from .base_model import get_db


def get_offer_by_id(offer_id):
    """
    Retorna uma oferta específica pelo ID
    
    Args:
        offer_id (int): ID da oferta
        
    Returns:
        dict: Dados da oferta ou None se não encontrada
    """
    db = get_db()
    data = db.get_data()
    
    for price in data['prices']:
        if price['id'] == offer_id:
            return {
                'id': price['id'],
                'product_id': price['product_id'],
                'store_name': price['store_name'],
                'price': price['price'],
                'url': price['url'],
                'last_updated': price['last_updated']
            }
    return None


def get_offers_by_product(product_id):
    """
    Retorna todas as ofertas de um produto específico
    
    Args:
        product_id (int): ID do produto
        
    Returns:
        list: Lista de ofertas ordenadas por preço (menor para maior)
    """
    db = get_db()
    data = db.get_data()
    
    offers = []
    for price in data['prices']:
        if price['product_id'] == product_id:
            offers.append({
                'id': price['id'],
                'product_id': price['product_id'],
                'store_name': price['store_name'],
                'price': price['price'],
                'url': price['url'],
                'last_updated': price['last_updated']
            })
    
    # Ordenar por preço (menor para maior) // aparece no front
    offers.sort(key=lambda x: x['price'])
    return offers


def get_offers_by_store(store_name):
    """
    Retorna todas as ofertas de uma loja específica
    
    Args:
        store_name (str): Nome da loja
        
    Returns:
        list: Lista de ofertas da loja
    """
    db = get_db()
    data = db.get_data()
    
    offers = []
    for price in data['prices']:
        if price['store_name'] == store_name:
            offers.append({
                'id': price['id'],
                'product_id': price['product_id'],
                'store_name': price['store_name'],
                'price': price['price'],
                'url': price['url'],
                'last_updated': price['last_updated']
            })
    
    return offers


def get_cheapest_offer(product_id):
    """
    Retorna a oferta mais barata de um produto
    
    Args:
        product_id (int): ID do produto
        
    Returns:
        dict: Oferta com menor preço ou None se não houver ofertas
    """
    offers = get_offers_by_product(product_id)
    return offers[0] if offers else None


def get_most_expensive_offer(product_id):
    """
    Retorna a oferta mais cara de um produto
    
    Args:
        product_id (int): ID do produto
        
    Returns:
        dict: Oferta com maior preço ou None se não houver ofertas
    """
    offers = get_offers_by_product(product_id)
    return offers[-1] if offers else None


def calculate_price_range(product_id):
    """
    Calcula a faixa de preço de um produto
    
    Args:
        product_id (int): ID do produto
        
    Returns:
        dict: Dicionário com min_price, max_price e store_count
    """
    offers = get_offers_by_product(product_id)
    
    if not offers:
        return {
            'min_price': None,
            'max_price': None,
            'store_count': 0
        }
    
    prices = [offer['price'] for offer in offers]
    return {
        'min_price': min(prices),
        'max_price': max(prices),
        'store_count': len(offers)
    }


def get_all_offers():
    """
    Retorna todas as ofertas do sistema
    
    Returns:
        list: Lista de todas as ofertas
    """
    db = get_db()
    data = db.get_data()
    
    offers = []
    for price in data['prices']:
        offers.append({
            'id': price['id'],
            'product_id': price['product_id'],
            'store_name': price['store_name'],
            'price': price['price'],
            'url': price['url'],
            'last_updated': price['last_updated']
        })
    
    return offers


def get_all_stores():
    """
    Retorna lista de todas as lojas que possuem ofertas
    
    Returns:
        list: Lista de nomes de lojas ordenados alfabeticamente
    """
    db = get_db()
    data = db.get_data()
    
    stores = set()
    for price in data['prices']:
        if price['store_name']:
            stores.add(price['store_name'])
    
    return sorted(list(stores))
