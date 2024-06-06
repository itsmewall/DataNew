from flask import Flask
from flask_cors import CORS
from database import db, migrate
import os

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configurações do aplicativo
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate.init_app(app, db)

    # Registra blueprints
    from api.endpoints import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    from api.satellite_endpoints import satellite_blueprint
    app.register_blueprint(satellite_blueprint, url_prefix='/api')

    return app