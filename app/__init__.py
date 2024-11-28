from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap4

from flask_login import LoginManager
from flask_bcrypt import Bcrypt 
#atualizando a camada de segurança
import os #icarregar a var
from dotenv import load_dotenv
load_dotenv('.env')

app= Flask(__name__)
bootstrap = Bootstrap4(app)


#atualizando a camada de segurança
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URI') #nome do banco de dados 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SECRET_KEY']= os.getenv('SECRET_KEY')
app.config['UPLOAD_FILES'] = r'static/data'
#DEFINIR A VARIAVEL DO BANCO DE DADOS
#variaveis para autenticação (Login e logout )
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)  # Renomeado para `login_manager`
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)




#rotas 
from app.routes import homepage 
from app.routes import cadastrar_novo

from app.routes import cadastro
from app.routes import logout

from app.routes import  deletarproduto
from app.routes import detalhes_vizualizar_produto
from app.routes import  editar_produto
from app.routes import  fornecedora_nova
from app.routes import  fornecedora_nova
# tela principal(MENU) 
from app.models import Produto
from app.models import User
from app.models import Fornecedora


                                #exibir produto