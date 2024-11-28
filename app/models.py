from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

produto_fornecedor = db.Table(
    'produto_fornecedor',
    db.Column('produto_id', db.Integer, db.ForeignKey('produto.id'), primary_key=True),
    db.Column('fornecedora_id', db.Integer, db.ForeignKey('fornecedora.id'), primary_key=True)
)

# Modelo de Usuário
class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=True)
    sobrenome = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)  # Email único
    senha = db.Column(db.String(100), nullable=False)

# Modelo de Produto
class Produto(db.Model):    
    __tablename__ = "produto"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(500), nullable=True)
    data_de_fabricacao = db.Column(db.DateTime, nullable=True)
    data_de_validade = db.Column(db.DateTime, nullable=True)
    fornecedor = db.Column(db.String(100), nullable=False)
    

     # Relacionamento muitos-para-muitos com fornecedoras
    fornecedoras = db.relationship(
        'Fornecedora',
        secondary=produto_fornecedor,
        backref=db.backref('produtos', lazy='dynamic'),
        lazy='dynamic'
    )


    # Relacionamento com Fornecedor (muitos-para-muitos)
   

# Modelo de Fornecedor
class Fornecedora(db.Model):
    __tablename__ = "fornecedora"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    ramo = db.Column(db.String(100), nullable=True)
    cnpj = db.Column(db.Integer,nullable=False)
    endereco = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    mensagem = db.Column(db.String(500), nullable=True)
   
    
    

