import requests
import pandas as pd
import logging

API_KEY = 'private-key'

def get_earthdata(start_date, end_date, bbox):
    lon_min, lat_min, lon_max, lat_max = bbox
    url = f"https://power.larc.nasa.gov/api/temporal/daily/point?start={start_date.replace('-', '')}&end={end_date.replace('-', '')}&latitude={lat_min}&longitude={lon_min}&community=SB&parameters=T2M,PRECTOT&format=JSON&user=sample&header=true&time-standard=UTC"
    
    response = requests.get(url)
    data = response.json()
    
    # Logar a resposta completa
    logging.info(f"Response Data: {data}")

    # Verificar a estrutura da resposta
    if 'properties' in data:
        # Converter os dados para um DataFrame do Pandas
        df = pd.json_normalize(data['properties']['parameter'])
        return df
    else:
        logging.error(f"Unexpected response structure: {data}")
        raise KeyError("The expected key 'properties' is not in the response.")