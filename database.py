from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

# tabela de usuários
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    # relacionamento com as transações
    transacoes = db.relationship("Transacao", backref="usuario", lazy=True)

    def definir_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha, senha)

    def __repr__(self):
        return f"<Usuario {self.nome}>"

# tabela de transações
class Transacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(10), nullable=False)  # "receita" ou "despesa"
    categoria = db.Column(db.String(50), nullable=False)
    data = db.Column(db.DateTime, default=datetime.now)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    def __repr__(self):
        return f"<Transacao {self.descricao}>"