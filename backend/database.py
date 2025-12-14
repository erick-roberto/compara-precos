import json
import os
from datetime import datetime
from threading import Lock

DATABASE_PATH = os.environ.get('DATABASE_PATH', 'database.json')

# Lock para garantir thread-safety ao acessar o JSON
_db_lock = Lock()

def load_db():
    """Carrega o banco de dados JSON"""
    if not os.path.exists(DATABASE_PATH):
        return get_default_db()
    
    try:
        with open(DATABASE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return get_default_db()

def save_db(data):
    """Salva o banco de dados JSON"""
    with _db_lock:
        with open(DATABASE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

def get_default_db():
    """Retorna a estrutura padrão do banco de dados"""
    return {
        "users": [],
        "products": [],
        "prices": [],
        "partner_stores": [],
        "clicks": [],
        "_metadata": {
            "next_user_id": 1,
            "next_product_id": 1,
            "next_price_id": 1,
            "next_partner_id": 1,
            "next_click_id": 1
        }
    }

def init_db():
    """Inicializa o banco de dados com dados de exemplo"""
    db = load_db()
    
    # Se o banco está vazio, adiciona dados de exemplo
    if len(db['products']) == 0:
        products = [
            ('Notebook Dell Inspiron 15', 'Notebook com Intel Core i5, 8GB RAM, 256GB SSD', 'Eletrônicos', 'https://via.placeholder.com/300x200?text=Dell+Inspiron'),
            ('iPhone 15 Pro 128GB', 'Smartphone Apple com câmera profissional', 'Celulares', 'https://via.placeholder.com/300x200?text=iPhone+15'),
            ('Smart TV Samsung 55"', 'TV 4K UHD com HDR e Smart Hub', 'Eletrônicos', 'https://via.placeholder.com/300x200?text=Samsung+TV'),
            ('Fone JBL Tune 510BT', 'Fone de ouvido Bluetooth com microfone', 'Áudio', 'https://via.placeholder.com/300x200?text=JBL+Fone'),
            ('Console PlayStation 5', 'Console de videogame de última geração', 'Games', 'https://via.placeholder.com/300x200?text=PS5'),
            ('Kindle Paperwhite', 'E-reader com tela de 6.8 polegadas', 'Livros', 'https://via.placeholder.com/300x200?text=Kindle')
        ]
        
        now = datetime.utcnow().isoformat()
        for name, description, category, image_url in products:
            product_id = db['_metadata']['next_product_id']
            db['products'].append({
                'id': product_id,
                'name': name,
                'description': description,
                'category': category,
                'image_url': image_url,
                'created_at': now
            })
            db['_metadata']['next_product_id'] += 1
        
        # Adicionar preços de exemplo
        prices_data = [
            (1, 'Amazon', 2899.90, 'https://amazon.com.br/notebook-dell'),
            (1, 'Magazine Luiza', 3099.00, 'https://magazineluiza.com.br/notebook-dell'),
            (1, 'Mercado Livre', 2799.99, 'https://mercadolivre.com.br/notebook-dell'),
            (2, 'Apple Store', 7299.00, 'https://apple.com/br/iphone'),
            (2, 'Fast Shop', 7199.90, 'https://fastshop.com.br/iphone15'),
            (2, 'Amazon', 6999.00, 'https://amazon.com.br/iphone15'),
            (3, 'Casas Bahia', 2499.00, 'https://casasbahia.com.br/tv-samsung'),
            (3, 'Extra', 2599.90, 'https://extra.com.br/tv-samsung'),
            (3, 'Amazon', 2399.99, 'https://amazon.com.br/tv-samsung'),
            (4, 'Amazon', 189.90, 'https://amazon.com.br/jbl-tune'),
            (4, 'Americanas', 199.00, 'https://americanas.com.br/jbl-tune'),
            (4, 'Submarino', 179.99, 'https://submarino.com.br/jbl-tune'),
            (5, 'Amazon', 3999.00, 'https://amazon.com.br/ps5'),
            (5, 'Magazine Luiza', 4199.90, 'https://magazineluiza.com.br/ps5'),
            (5, 'Fast Shop', 3899.99, 'https://fastshop.com.br/ps5'),
            (6, 'Amazon', 549.00, 'https://amazon.com.br/kindle'),
            (6, 'Magazine Luiza', 599.90, 'https://magazineluiza.com.br/kindle'),
            (6, 'Americanas', 579.00, 'https://americanas.com.br/kindle')
        ]
        
        for product_id, store_name, price, url in prices_data:
            price_id = db['_metadata']['next_price_id']
            db['prices'].append({
                'id': price_id,
                'product_id': product_id,
                'store_name': store_name,
                'price': price,
                'url': url,
                'last_updated': now
            })
            db['_metadata']['next_price_id'] += 1
        
        print("Dados de exemplo inseridos com sucesso!")
    
    # Adicionar usuário de exemplo se não existir
    if not any(user['email'] == 'teste@exemplo.com' for user in db['users']):
        from flask_bcrypt import generate_password_hash
        password_hash = generate_password_hash('password').decode('utf-8')
        user_id = db['_metadata']['next_user_id']
        db['users'].append({
            'id': user_id,
            'email': 'teste@exemplo.com',
            'password_hash': password_hash,
            'created_at': datetime.utcnow().isoformat()
        })
        db['_metadata']['next_user_id'] += 1
        print("Usuário de exemplo 'teste@exemplo.com' inserido com sucesso!")
    
    save_db(db)
    return db

class JSONDatabase:
    """Classe para simular uma conexão com banco de dados JSON"""
    
    def __init__(self):
        self.data = load_db()
    
    def close(self):
        """Fecha a conexão (salva dados)"""
        save_db(self.data)
    
    def get_data(self):
        """Retorna os dados do banco"""
        return self.data

def get_db_connection():
    """Retorna uma conexão com o banco de dados JSON"""
    return JSONDatabase()

if __name__ == '__main__':
    init_db()
    print(f"Banco de dados inicializado em: {DATABASE_PATH}")
