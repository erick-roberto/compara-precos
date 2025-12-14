"""
Controller GERENCIAR_USUÁRIO - Controle de Gerenciamento de Usuários

Responsabilidades:
- Processar requisições CRUD de usuários (Criar, Ler, Atualizar, Deletar)
- Validar dados de entrada
- Verificar autorização (apenas admin pode gerenciar usuários)
- Retornar lista de usuários e dados de usuários específicos

Casos de Uso:
- Gerenciar Usuários (Administrador): Operações CRUD em contas de usuários

Relacionamentos:
- Interage com o Model USUÁRIO para operações de CRUD
- Requer autenticação e verificação de tipo de usuário (admin)
"""

from flask import jsonify, request
from models import user_model
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def get_all_users():
    try:
        users = user_model.get_all_users()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": "Erro ao carregar usuários"}), 500


def get_user_by_id(user_id):
    """
    Retorna dados de um usuário específico
    
    Requisição:
        GET /api/users/<user_id>
        Headers:
            Authorization: Bearer <token>
    
    Parâmetros:
        user_id (int): ID do usuário a buscar
    
    Respostas:
        200: Dados do usuário
        404: Usuário não encontrado
        401: Não autenticado
        403: Não autorizado
    """
    try:
        user = user_model.find_user_by_id(user_id)
        if user is None:
            return jsonify({"error": "Usuário não encontrado"}), 404
        return jsonify(user), 200
    except Exception as e:
        return jsonify({"error": "Erro ao buscar usuário"}), 500


def create_user():
    """
    Cria um novo usuário no sistema
    
    Requisição:
        POST /api/users
        Headers:
            Authorization: Bearer <token>
        Body:
            {
                "name": "Nome do Usuário",
                "email": "email@example.com",
                "password": "senha123",
                "user_type": "cliente" ou "admin"
            }
    
    Respostas:
        201: Usuário criado com sucesso
        400: Dados inválidos ou usuário já existe
        401: Não autenticado
        403: Não autorizado
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados são obrigatórios"}), 400
        
        # Validar dados obrigatórios
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        user_type = data.get('user_type', 'cliente')
        
        # Validações
        if not name or len(name) < 2:
            return jsonify({"error": "Nome deve ter pelo menos 2 caracteres"}), 400
        
        if not email or '@' not in email:
            return jsonify({"error": "Email inválido"}), 400
        
        if not password or len(password) < 6:
            return jsonify({"error": "Senha deve ter pelo menos 6 caracteres"}), 400
        
        if user_type not in ['admin', 'cliente']:
            return jsonify({"error": "Tipo de usuário inválido. Deve ser 'admin' ou 'cliente'"}), 400
        
        # Verificar se usuário já existe
        if user_model.find_user_by_email(email):
            return jsonify({"error": "Usuário com este email já existe"}), 409
        
        # Hash da senha
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Criar usuário
        new_user = user_model.create_user(name, email, password_hash, user_type)
        
        if new_user is None:
            return jsonify({"error": "Falha ao criar usuário"}), 500
        
        return jsonify(new_user), 201
    except Exception as e:
        print(f"Erro ao criar usuário: {str(e)}")
        return jsonify({"error": "Erro ao criar usuário"}), 500


def update_user(user_id):
    """
    Atualiza dados de um usuário
    
    Requisição:
        PUT /api/users/<user_id>
        Headers:
            Authorization: Bearer <token>
        Body:
            {
                "name": "Novo Nome",
                "user_type": "admin" ou "cliente"
            }
    
    Parâmetros:
        user_id (int): ID do usuário a atualizar
    
    Respostas:
        200: Usuário atualizado com sucesso
        400: Dados inválidos
        404: Usuário não encontrado
        401: Não autenticado
        403: Não autorizado
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados para atualização são obrigatórios"}), 400
        
        name = data.get('name', '').strip() if data.get('name') else None
        user_type = data.get('user_type')
        
        # Validações
        if name and len(name) < 2:
            return jsonify({"error": "Nome deve ter pelo menos 2 caracteres"}), 400
        
        if user_type and user_type not in ['admin', 'cliente']:
            return jsonify({"error": "Tipo de usuário inválido"}), 400
        
        # Atualizar usuário
        updated_user = user_model.update_user(user_id, name, None, user_type)
        
        if updated_user is None:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        return jsonify(updated_user), 200
    except Exception as e:
        print(f"Erro ao atualizar usuário: {str(e)}")
        return jsonify({"error": "Erro ao atualizar usuário"}), 500


def delete_user(user_id):
    """
    Deleta um usuário do sistema
    
    Requisição:
        DELETE /api/users/<user_id>
        Headers:
            Authorization: Bearer <token>
    
    Parâmetros:
        user_id (int): ID do usuário a deletar
    
    Respostas:
        200: Usuário deletado com sucesso
        404: Usuário não encontrado
        401: Não autenticado
        403: Não autorizado
    """
    try:
        success = user_model.delete_user(user_id)
        
        if not success:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        return jsonify({"message": "Usuário deletado com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao deletar usuário: {str(e)}")
        return jsonify({"error": "Erro ao deletar usuário"}), 500
