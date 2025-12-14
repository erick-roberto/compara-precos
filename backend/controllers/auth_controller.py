from flask import request, jsonify, current_app
from flask_bcrypt import Bcrypt
import jwt
import re
from models import user_model
from datetime import datetime, timedelta

bcrypt = Bcrypt()


# ---------------------------------------------------------
# FUNÇÕES DE VALIDAÇÃO INTERNAS AO CONTROLLER
# ---------------------------------------------------------

def _validate_email(email):
    if not email:
        return False, "Email é obrigatório"

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True, None
    return False, "Email inválido"


def _validate_password(password):
    if not password:
        return False, "Senha não pode estar vazia"
    if len(password) > 8:
        return False, "Senha deve ter no máximo 8 caracteres"
    if len(password) < 6:
        return False, "Senha deve ter pelo menos 6 caracteres"
    if not any(c.isdigit() for c in password):
        return False, "Senha deve conter pelo menos um número"
    if not any(c.isalpha() for c in password):
        return False, "Senha deve conter pelo menos uma letra"
    return True, None


# ---------------------------------------------------------
#   CONTROLLER - REGISTRO
# ---------------------------------------------------------
def register():

    data = request.get_json() or {}

    name = data.get("name", "").strip()
    email = data.get("email")
    password = data.get("password")
    user_type = data.get("user_type", "cliente")

    # ----------------------------
    # VALIDAR CAMPOS OBRIGATÓRIOS
    # ----------------------------
    if not email or not password:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400

    # nome padrão
    if not name:
        name = email.split("@")[0]

    if len(name) < 2:
        return jsonify({"error": "Nome deve ter pelo menos 2 caracteres"}), 400

    # ----------------------------
    # VALIDAR EMAIL
    # ----------------------------
    ok, error = _validate_email(email)
    if not ok:
        return jsonify({"error": error}), 400

    # ----------------------------
    # VALIDAR SENHA
    # ----------------------------
    ok, error = _validate_password(password)
    if not ok:
        return jsonify({"error": error}), 400

    # ----------------------------
    # VALIDAR TIPO DE USUÁRIO
    # ----------------------------
    if user_type not in ["admin", "cliente"]:
        return jsonify({"error": "Tipo de usuário inválido. Deve ser 'admin' ou 'cliente'"}), 400

    # ----------------------------
    # VERIFICAR SE USUÁRIO EXISTE
    # ----------------------------
    if user_model.find_user_by_email(email):
        return jsonify({"error": "Usuário já existe"}), 409

    # ----------------------------
    # CRIAR USUÁRIO
    # ----------------------------
    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = user_model.create_user(name, email, password_hash, user_type)

    if not new_user:
        return jsonify({"error": "Erro ao registrar usuário"}), 500

    return jsonify({
        "message": "Usuário registrado com sucesso",
        "user": new_user
    }), 201



# ---------------------------------------------------------
#   CONTROLLER - LOGIN
# ---------------------------------------------------------
def login():

    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    # ----------------------------
    # VALIDAR CAMPOS
    # ----------------------------
    if not email or not password:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400

    ok, error = _validate_email(email)
    if not ok:
        return jsonify({"error": error}), 400

    # ----------------------------
    # VERIFICAR USUÁRIO
    # ----------------------------
    user = user_model.find_user_by_email(email)
    if not user:
        return jsonify({"error": "Credenciais inválidas"}), 401

    # ----------------------------
    # VERIFICAR SENHA
    # ----------------------------
    if not bcrypt.check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Credenciais inválidas"}), 401

    # ----------------------------
    # GERAR TOKEN
    # ----------------------------
    payload = {
        "user_id": user["id"],
        "name": user.get("name", ""),
        "email": user["email"],
        "user_type": user.get("user_type", "cliente"),
        "exp": datetime.utcnow() + timedelta(hours=24),
        "iat": datetime.utcnow(),
    }

    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

    return jsonify({
        "message": "Login bem-sucedido",
        "token": token,
        "user": {
            "id": user["id"],
            "name": user.get("name", ""),
            "email": user["email"],
            "user_type": user.get("user_type", "cliente"),
        }
    }), 200
