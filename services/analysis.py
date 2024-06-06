import requests
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# URL da API
API_URL = 'http://127.0.0.1:5000/api/satellite-data'

def fetch_and_analyze_data(params):
    # Fazer a solicitação para a API
    response = requests.get(API_URL, params=params)
    data_json = response.json()

    # Preparar os dados
    data = []
    for key, value in data_json[0].items():
        param, date = key.split('.')
        data.append({'Parameter': param, 'Date': date, 'Value': value})

    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')

    # Filtrar apenas os dados de temperatura (T2M)
    df_temperature = df[df['Parameter'] == 'T2M'].set_index('Date')

    # Análise descritiva
    descriptive_stats = df_temperature['Value'].describe().to_frame()

    # Visualizar os dados
    fig, ax = plt.subplots(figsize=(10, 5))
    df_temperature['Value'].plot(marker='o', ax=ax)
    ax.set_title("Temperatura Diária (T2M)")
    ax.set_xlabel("Data")
    ax.set_ylabel("Temperatura (°C)")
    ax.grid(True)
    plt.tight_layout()

    # Salvar gráfico em buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_url = base64.b64encode(buf.getvalue()).decode('utf8')

    # Identificar padrões e tendências
    rolling_mean = df_temperature['Value'].rolling(window=7).mean()
    fig, ax = plt.subplots(figsize=(10, 5))
    df_temperature['Value'].plot(label='Temperatura Diária', marker='o', ax=ax)
    rolling_mean.plot(label='Média Móvel (7 dias)', linestyle='--', ax=ax)
    ax.set_title("Temperatura Diária com Média Móvel")
    ax.set_xlabel("Data")
    ax.set_ylabel("Temperatura (°C)")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()

    # Salvar gráfico em buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    rolling_mean_plot_url = base64.b64encode(buf.getvalue()).decode('utf8')

    # Detecção de anomalias (temperaturas fora do intervalo interquartil)
    Q1 = df_temperature['Value'].quantile(0.25)
    Q3 = df_temperature['Value'].quantile(0.75)
    IQR = Q3 - Q1
    anomalies = df_temperature[(df_temperature['Value'] < (Q1 - 1.5 * IQR)) | (df_temperature['Value'] > (Q3 + 1.5 * IQR))]

    fig, ax = plt.subplots(figsize=(10, 5))
    df_temperature['Value'].plot(label='Temperatura Diária', marker='o', ax=ax)
    ax.plot(anomalies.index, anomalies['Value'], 'ro', label='Anomalias')
    ax.set_title("Detecção de Anomalias na Temperatura Diária")
    ax.set_xlabel("Data")
    ax.set_ylabel("Temperatura (°C)")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()

    # Salvar gráfico em buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    anomalies_plot_url = base64.b64encode(buf.getvalue()).decode('utf8')

    return descriptive_stats, plot_url, rolling_mean_plot_url, anomalies_plot_url