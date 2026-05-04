from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# cria o objeto do banco de dados
db = SQLAlchemy()

# tabela de usuários
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)  # senha sempre criptografada

    # salva a senha já criptografada
    def definir_senha(self, senha):
        self.senha = generate_password_hash(senha)

    # verifica se a senha digitada bate com a criptografada
    def verificar_senha(self, senha):
        return check_password_hash(self.senha, senha)

    def __repr__(self):
        return f"<Usuario {self.nome}>"