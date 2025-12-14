"""
Model USUÁRIO - Entidade de Dados para Usuários do Sistema

Responsabilidades:
- Gerenciar dados de usuários (administradores e clientes)
- Persistência e recuperação de dados de usuários
- Validação de existência de usuários
- Operações CRUD para gerenciamento de usuários

Atributos da Entidade USUÁRIO:
- id: Identificador único do usuário
- name: Nome do usuário
- email: Email do usuário
- password_hash: Senha criptografada
- user_type: Tipo de usuário ('admin' ou 'cliente')
- created_at: Data de criação do usuário

Casos de Uso:
- Gerenciar Usuários (Administrador): Operações CRUD em contas de usuários
"""

from .base_model import get_db
from datetime import datetime


def find_user_by_email(email):
    """
    Será utilizado para Login
    Encontra um usuário pelo email
    
    Args:
        email (str): Email do usuário a buscar
        
    Returns:
        dict: Dados do usuário ou None se não encontrado
    """
    db = get_db()
    data = db.get_data()
    
    for user in data['users']:
        if user['email'] == email:
            return {
                'id': user['id'],
                'name': user.get('name', ''),
                'email': user['email'],
                'password_hash': user['password_hash'],
                'user_type': user.get('user_type', 'cliente'),
                'created_at': user.get('created_at', '')
            }
    return None


def find_user_by_id(user_id):
    """
    Encontra um usuário pelo ID
    
    Args:
        user_id (int): ID do usuário a buscar
        
    Returns:
        dict: Dados do usuário ou None se não encontrado
    """
    db = get_db()
    data = db.get_data()
    
    for user in data['users']:
        if user['id'] == user_id:
            return {
                'id': user['id'],
                'name': user.get('name', ''),
                'email': user['email'],
                'password_hash': user['password_hash'],
                'user_type': user.get('user_type', 'cliente'),
                'created_at': user.get('created_at', '')
            }
    return None


def create_user(name, email, password_hash, user_type='cliente'):
    """
    Cria um novo usuário no sistema
    
    Args:
        name (str): Nome do usuário
        email (str): Email do novo usuário
        password_hash (str): Senha criptografada do usuário
        user_type (str): Tipo de usuário ('admin' ou 'cliente'), padrão 'cliente'
        
    Returns:
        dict: Dados do novo usuário ou None se falhar
    """
    db = get_db() # abre o banco de dados
    data = db.get_data() # ler os dados em formato Python (dicionário)
    
    # Verificar se usuário já existe
    # Já verificado no controller, mas aqui garante consistência
    if any(user['email'] == email for user in data['users']):
        return None
    
    try:
        user_id = data['_metadata']['next_user_id'] # cria o ID 
        new_user = { # criação do dicionário do novo usuário
            'id': user_id,
            'name': name,
            'email': email,
            'password_hash': password_hash,
            'user_type': user_type,
            'created_at': datetime.utcnow().isoformat()
        }
        data['users'].append(new_user) # adiciona o usuário no banco
        data['_metadata']['next_user_id'] += 1 # incrementa o ID

        # salva as atualizações e fecha o banco
        db.close()
        
        return {
            # retorno do usuário para o controller (Sem a senha)
            'id': new_user['id'],
            'name': new_user['name'],
            'email': new_user['email'],
            'user_type': new_user['user_type'],
            'created_at': new_user['created_at']
        }
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
        return None


def get_all_users():
    """
    Retorna todos os usuários do sistema (sem senhas)
    
    Returns:
        list: Lista de usuários
    """
    db = get_db() # abre o banco de dados
    data = db.get_data() # retorna o conteúdo do banco em dicionário (Python)
    
    # cria uma lista de usuários sem os dados sensíveis
    users = []
    for user in data['users']:
        users.append({
            'id': user['id'],
            'name': user.get('name', ''),
            'email': user['email'],
            'user_type': user.get('user_type', 'cliente'),
            'created_at': user.get('created_at', '')
        })
    
    # retorno da lista de usuários seguros
    return users 


def update_user(user_id, name=None, email=None, user_type=None):
    """
    Atualiza dados de um usuário
    
    Args:
        user_id (int): ID do usuário a atualizar
        name (str): Novo nome (opcional)
        email (str): Novo email (opcional)
        user_type (str): Novo tipo de usuário (opcional)
        
    Returns:
        dict: Dados do usuário atualizado ou None se falhar
    """
    db = get_db() # abre o banco de dados
    data = db.get_data() # cria um dicionário python com o conteúdo do banco
    
    user_found = False
    for user in data['users']:
        if user['id'] == user_id:
            user_found = True
            
            # Validar novo email se fornecido
            if email and email != user['email']:
                if any(u['email'] == email for u in data['users']):
                    return None  # Email já existe
                user['email'] = email
            
            # atualização do nome
            if name:
                user['name'] = name
            
            # atualização do tipo de usuário
            if user_type and user_type in ['admin', 'cliente']:
                user['user_type'] = user_type
            
            # fecha o banco de dados
            db.close()
            
            return { # retorna dados do usuário (sem senha)
                'id': user['id'],
                'name': user.get('name', ''),
                'email': user['email'],
                'user_type': user.get('user_type', 'cliente'),
                'created_at': user.get('created_at', '')
            }
    
    return None # retorna se o usuário não for encontrado


def delete_user(user_id):
    """
    Deleta um usuário do sistema
    
    Args:
        user_id (int): ID do usuário a deletar
        
    Returns:
        bool: True se deletado com sucesso, False caso contrário
    """
    db = get_db() # abre banco da dados
    data = db.get_data() # retorna um dicionário em python com os dados
    
    try:
        initial_length = len(data['users']) # tamanho da lista
        # criação de uma lista sem o usuário deletado
        data['users'] = [user for user in data['users'] if user['id'] != user_id]
        
        # verifica o tamanho da lista resultante
        if len(data['users']) < initial_length:
            db.close()
            return True
        
        return False # se algúem não for deletado
    
    except Exception as e:
        print(f"Erro ao deletar usuário: {e}")
        return False


# função não utilizada (caso de uso de alterar senha)

def change_password(user_id, new_password_hash):
    """
    Altera a senha de um usuário
    
    Args:
        user_id (int): ID do usuário
        new_password_hash (str): Nova senha criptografada
        
    Returns:
        bool: True se alterado com sucesso, False caso contrário
    """
    db = get_db() # abre o banco de dados
    data = db.get_data() # cria o dicionário python
    
    try:
        for user in data['users']:
            if user['id'] == user_id:
                user['password_hash'] = new_password_hash
                db.close()
                return True
        return False
    except Exception as e:
        print(f"Erro ao alterar senha: {e}")
        return False
