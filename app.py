from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Inicializa o banco de dados
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configurações do aplicativo
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa extensões
    db.init_app(app)

    # Registra blueprints
    from api.endpoints import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app