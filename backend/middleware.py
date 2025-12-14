"""
Middleware de Autenticação e Autorização

Responsabilidades:
- Validar tokens JWT
- Verificar tipos de usuário
- Proteger rotas que requerem autenticação
- Implementar controle de acesso baseado em papéis (RBAC)
"""

from functools import wraps
from flask import request, jsonify
import jwt
from datetime import datetime, timedelta
import os


SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-key")


def generate_token(user_id, user_type, email, name, expires_in=24):
    """
    Gera um token JWT para o usuário
    
    Args:
        user_id (int): ID do usuário
        user_type (str): Tipo de usuário ('admin' ou 'cliente')
        email (str): Email do usuário
        name (str): Nome do usuário
        expires_in (int): Tempo de expiração em horas
        
    Returns:
        str: Token JWT
    """
    payload = {
        'user_id': user_id,
        'user_type': user_type,
        'email': email,
        'name': name,
        'exp': datetime.utcnow() + timedelta(hours=expires_in),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def verify_token(token):
    """
    Verifica e decodifica um token JWT
    
    Args:
        token (str): Token JWT a verificar
        
    Returns:
        dict: Dados decodificados do token ou None se inválido
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expirado
    except jwt.InvalidTokenError:
        return None  # Token inválido


def require_auth(f):
    """
    Decorator para requerer autenticação
    
    Valida o token JWT no header Authorization
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({"error": "Token de autenticação obrigatório"}), 401
        
        try:
            token = auth_header.split(' ')[1] if ' ' in auth_header else auth_header
            payload = verify_token(token)
            
            if payload is None:
                return jsonify({"error": "Token inválido ou expirado"}), 401
            
            # Adicionar dados do usuário ao contexto da requisição
            request.user = payload
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": "Erro ao validar token"}), 401
    
    return decorated_function


def require_admin(f):
    """
    Decorator para requerer autenticação e tipo admin
    
    Valida o token JWT e verifica se o usuário é administrador
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({"error": "Token de autenticação obrigatório"}), 401
        
        try:
            token = auth_header.split(' ')[1] if ' ' in auth_header else auth_header
            payload = verify_token(token)
            
            if payload is None:
                return jsonify({"error": "Token inválido ou expirado"}), 401
            
            if payload.get('user_type') != 'admin':
                return jsonify({"error": "Acesso negado. Apenas administradores podem acessar este recurso"}), 403
            
            # Adicionar dados do usuário ao contexto da requisição
            request.user = payload
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": "Erro ao validar autenticação"}), 401
    
    return decorated_function


def require_client(f):
    """
    Decorator para requerer autenticação e tipo cliente
    
    Valida o token JWT e verifica se o usuário é cliente
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({"error": "Token de autenticação obrigatório"}), 401
        
        try:
            token = auth_header.split(' ')[1] if ' ' in auth_header else auth_header
            payload = verify_token(token)
            
            if payload is None:
                return jsonify({"error": "Token inválido ou expirado"}), 401
            
            if payload.get('user_type') != 'cliente':
                return jsonify({"error": "Acesso negado. Apenas clientes podem acessar este recurso"}), 403
            
            # Adicionar dados do usuário ao contexto da requisição
            request.user = payload
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": "Erro ao validar autenticação"}), 401
    
    return decorated_function
