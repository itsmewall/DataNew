from flask import Flask, render_template
from flask_cors import CORS
from database import db, migrate
import os
from services.analysis import fetch_and_analyze_data

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configurações do aplicativo
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Certificar-se de que o diretório 'instance' existe
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db)

    # Registra blueprints
    from api.endpoints import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    from api.satellite_endpoints import satellite_blueprint
    app.register_blueprint(satellite_blueprint, url_prefix='/api')

    @app.route('/analyze')
    def analyze():
        params = {
            'start_date': '2023-01-01',
            'end_date': '2023-01-31',
            'bbox': '-120.0,35.0,-119.0,36.0'
        }
        descriptive_stats, plot_url, rolling_mean_plot_url, anomalies_plot_url = fetch_and_analyze_data(params)
        return render_template('analysis.html', 
                               descriptive_stats=descriptive_stats.to_html(), 
                               plot_url=plot_url, 
                               rolling_mean_plot_url=rolling_mean_plot_url, 
                               anomalies_plot_url=anomalies_plot_url)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)