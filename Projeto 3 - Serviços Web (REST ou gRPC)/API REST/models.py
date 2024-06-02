from flask_sqlalchemy import SQLAlchemy

# Criando a instância do SQLAlchemy
db = SQLAlchemy()

# Definindo o modelo da tabela 'livros'
class Livro(db.Model):
    __tablename__ = 'livros'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), nullable=False)
    autor = db.Column(db.String(30), nullable=False)
    editora = db.Column(db.String(30), nullable=False)

# Definindo o modelo da tabela 'usuarios'
class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)