'''

Coração do BackEnd
- Inicia o servidor flask
- carrega variáveis do .env
- configura os bancos de dados JSON
- registra os controllers
- cria todas as rotas da API

flask - ferramenta para criar a API
CORS - permite que o frontend(react) acesse a API
dotenv - carrega as variáveis do ambiente 
controllers - funções que lidam com as requisições da API
database - inicializa o banco de dados JSON

'''

import os
from flask import Flask, jsonify, g
from flask_cors import CORS
from dotenv import load_dotenv
from controllers import (
    auth_controller, 
    product_controller, 
    search_controller, 
    comparison_controller, 
    details_controller,
    user_management_controller
)
from database import init_db as db_initializer, JSONDatabase
from middleware import require_admin, require_auth

# Carregar variáveis de ambiente
load_dotenv()

# Configuração
DATABASE_PATH = os.environ.get("DATABASE_PATH", "database.json")
PORT = int(os.environ.get("PORT", 3000))
SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-key")

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
CORS(app)  # Habilitar CORS para todas as rotas

# Inicializar Bcrypt com o app - usado para hashing de senhas
auth_controller.bcrypt.init_app(app)

# --- Funções de Banco de Dados ---
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = JSONDatabase()
    return db
'''
função para acessar o banco de dados em cada requisição.
ele cria um objeto global temporário 'g' para armazenar a conexão com o banco de dados

'''

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()
'''
após a requisição, essa função fecha a conexão com o banco de dados

'''

# --- Rotas da API --- Rota inicial
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API de Comparação de Preços (Python/Flask com JSON)"})

# --- Rotas de Autenticação ---
app.route("/api/auth/register", methods=["POST"])(auth_controller.register)
app.route("/api/auth/login", methods=["POST"])(auth_controller.login)

# --- Rotas de Gerenciamento de Usuários (GERENCIAR_USUÁRIO) ---
app.route("/api/users", methods=["GET"])(require_admin(user_management_controller.get_all_users))
app.route("/api/users", methods=["POST"])(require_admin(user_management_controller.create_user))
app.route("/api/users/<int:user_id>", methods=["GET"])(require_admin(user_management_controller.get_user_by_id))
app.route("/api/users/<int:user_id>", methods=["PUT"])(require_admin(user_management_controller.update_user))
app.route("/api/users/<int:user_id>", methods=["DELETE"])(require_admin(user_management_controller.delete_user))

# --- Rotas de Produtos (Listagem Geral) ---
app.route("/api/products", methods=["GET"])(product_controller.get_products)

# --- Rotas de Busca de Produtos (PESQUISAR_PRODUTO) ---
app.route("/api/products/search", methods=["GET"])(search_controller.search_products)
app.route("/api/categories", methods=["GET"])(search_controller.get_categories)

# --- Rotas de Detalhes de Produtos (VISUALIZAR_DETALHES_PRODUTO) ---
app.route("/api/products/<int:product_id>", methods=["GET"])(details_controller.get_product_details)
app.route("/api/products/<int:product_id>/prices", methods=["GET"])(details_controller.get_product_prices)

# --- Rotas de Comparação de Preços (VISUALIZAR_COMPARAÇÃO_PREÇOS) ---
app.route("/api/compare", methods=["POST"])(comparison_controller.compare_products)

'''
Os controllers lidam com a lógica de cada rota, como registrar usuários, buscar produtos, etc.

Aqui definimos qual URL chama qual função do controller.

'''


# --- Inicialização ---
if __name__ == "__main__":
    with app.app_context():
        db_initializer()
    app.run(host="0.0.0.0", port=PORT, debug=True)
