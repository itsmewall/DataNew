from flask import Blueprint, jsonify
from services.nasa_earthdata_service import get_earthdata
import logging

satellite_blueprint = Blueprint('satellite', __name__)

@satellite_blueprint.route('/satellite-data', methods=['GET'])
def fetch_satellite_data():
    # Parâmetros diretos para teste
    start_date = "2000-01-01"
    end_date = "2023-01-31"
    bbox = [-120.0, 35.0, -119.0, 36.0] 

    try:
        data = get_earthdata(start_date, end_date, bbox)
        return data.to_json(orient='records')
    except KeyError as e:
        logging.error(f"KeyError: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        logging.error(f"Error fetching satellite data: {e}")
        return jsonify({"error": str(e)}), 500