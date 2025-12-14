from flask import g
from database import load_db, save_db
import os

DATABASE_PATH = os.environ.get('DATABASE_PATH', 'database.json')

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

def get_db():
    """Retorna uma conexão com o banco de dados JSON"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = JSONDatabase()
    return db
