import requests
import pandas as pd
import pandas_ta as ta
import os
from dotenv import load_dotenv
import json


# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# --- Função para buscar dados OHLCV dos últimos 3 meses da API CoinDesk por horas ---
def fetch_last_3_months_hourly():
    url = "https://data-api.coindesk.com/spot/v1/historical/hours"

    # Parâmetros fixos comuns às requisições
    params = {"instrument":"BTC-USDT",
                    "aggregate":1,
                    "fill":"true",
                    "apply_mapping":"true",
                    "response_format":"JSON",
                    "groups":"OHLC,VOLUME",
                    "limit":2000,
                    "market":"coinbase",
                    "api_key":os.getenv("COINDESK_API_KEY")}
    
    headers = {
        "Content-Type": "application/json; charset=UTF-8"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        resposta = response.json()
        return resposta['Data']
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar dados do latest tick da API CoinDesk: {e}")
        return None


# --- Função para converter os dados OHLCV em DataFrame ---
def converte_ohlcv_para_df(resposta_api: list) -> pd.DataFrame:
    """
    Converte uma lista de dicionários da API em um DataFrame do pandas,
    processa o timestamp e seleciona as colunas de interesse.
    """
    df = pd.DataFrame(resposta_api)
    df = df.set_index(pd.to_datetime(df['TIMESTAMP'], unit='s', utc=True))
    df.index = pd.DatetimeIndex(df.index).tz_convert("America/Sao_Paulo")
    df_final = df[['OPEN', 'HIGH', 'LOW', 'CLOSE', 'QUOTE_VOLUME']].rename(columns={'QUOTE_VOLUME': 'VOLUME'})
    return df_final


# --- Função para buscar dados OHLCV dos últimos 3 meses da API CoinDesk por dia --- ✅
def fetch_last_3_months_daily():
    url = "https://data-api.coindesk.com/spot/v1/historical/days"

    # Parâmetros fixos comuns às requisições
    params = {"instrument":"BTC-USD",
                    "aggregate":1,
                    "fill":"true",
                    "apply_mapping":"true",
                    "response_format":"JSON",
                    "groups":"OHLC",
                    "limit":90,
                    "market":"coinbase",
                    "api_key":os.getenv("COINDESK_API_KEY")}
    
    headers = {
        "Content-Type": "application/json; charset=UTF-8"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        resposta = response.json()
        return resposta['Data']
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar dados do latest tick da API CoinDesk: {e}")
        return None
    

# --- Função para formatar dados daily --- ✅
def formata_ohlcv_daily(dados_api: list) -> list:
    """
    Recebe dados da API, transforma em DataFrame e retorna uma lista de dicionários.
    Args:
        dados_api (list): Lista de dicionários vinda da API.
    Returns:
        list: Lista de dicionários com as chaves 'DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE'.
    """
    # Cria o DataFrame a partir dos dados da API
    df = pd.DataFrame(dados_api)
    # Converte o timestamp para data e define como índice
    df['DATE'] = pd.to_datetime(df['TIMESTAMP'], unit='s', utc=True).dt.strftime('%Y-%m-%d')
    # Seleciona as colunas desejadas e renomeia se necessário (aqui os nomes já batem)
    df_final = df[['DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE']]
    # Retorna a lista de dicionários
    return df_final.to_dict(orient='records')


# --- Funções que retorna dados Latest Tick CoinDesk --- ✅
def fetch_coindesk_latest_tick():
    """
    Busca os dados mais recentes (latest tick) da API CoinDesk.
    (Endpoint e parâmetros exatos podem precisar de ajuste conforme a documentação da CoinDesk para este endpoint específico)
    """
    url = 'https://data-api.coindesk.com/spot/v1/latest/tick'
    
    params = {
        "market": "coinbase",
        "instruments": "BTC-USD",
        "apply_mapping":"true",
        "api_key": os.getenv("COINDESK_API_KEY")
    }
    headers = {
        "Content-type": "application/json; charset=UTF-8"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar dados do latest tick da API CoinDesk: {e}")
        return None


# --- Função para converter os dados de latest tick em DataFrame --- ✅
def converte_latest_tick_para_dict(json_response) -> pd.DataFrame:
    """
    Extrai informações chave do JSON de resposta do "latest tick".
    """
    if not json_response or 'Data' not in json_response:
        print("Resposta JSON do latest tick inválida ou sem dados para o instrumento.")
        return None

    dicionario_dados_brutos = json_response['Data']['BTC-USD']

    # Convertendo o timestamp para legível, apenas para referência ou se for injetar no prompt
    last_update_ts_readable = pd.to_datetime(dicionario_dados_brutos.get('PRICE_LAST_UPDATE_TS'), unit='s', errors='coerce')

    # Selecionando os dados que eu quero:
    key_current_data = {
        "current_price": dicionario_dados_brutos.get('PRICE'),
        "price_last_update_utc": last_update_ts_readable.strftime('%Y-%m-%d %H:%M:%S UTC') if pd.notnull(last_update_ts_readable) else None,
        "price_movement_flag": dicionario_dados_brutos.get('PRICE_FLAG'), 
        
        "current_day_open": dicionario_dados_brutos.get('CURRENT_DAY_OPEN'),
        "current_day_high": dicionario_dados_brutos.get('CURRENT_DAY_HIGH'),
        "current_day_low": dicionario_dados_brutos.get('CURRENT_DAY_LOW'),
        "current_day_volume_btc": dicionario_dados_brutos.get('CURRENT_DAY_VOLUME'),
        "current_day_volume_usd": dicionario_dados_brutos.get('CURRENT_DAY_QUOTE_VOLUME'),
        "current_day_change_percentage": dicionario_dados_brutos.get('CURRENT_DAY_CHANGE_PERCENTAGE'),

        "moving_24_hour_open": dicionario_dados_brutos.get('MOVING_24_HOUR_OPEN'),
        "moving_24_hour_high": dicionario_dados_brutos.get('MOVING_24_HOUR_HIGH'),
        "moving_24_hour_low": dicionario_dados_brutos.get('MOVING_24_HOUR_LOW'),
        "moving_24_hour_volume_btc": dicionario_dados_brutos.get('MOVING_24_HOUR_VOLUME'),
        "moving_24_hour_volume_usd": dicionario_dados_brutos.get('MOVING_24_HOUR_QUOTE_VOLUME'),
        "moving_24_hour_change_percentage": dicionario_dados_brutos.get('MOVING_24_HOUR_CHANGE_PERCENTAGE'),

        "moving_7_day_open": dicionario_dados_brutos.get("MOVING_7_DAY_OPEN"),
        "moving_7_day_high": dicionario_dados_brutos.get("MOVING_7_DAY_HIGH"),
        "moving_7_day_low": dicionario_dados_brutos.get("MOVING_7_DAY_LOW"),
        "moving_7_day_volume_btc": dicionario_dados_brutos.get("MOVING_7_DAY_VOLUME"),
        "moving_7_day_volume_usd": dicionario_dados_brutos.get("MOVING_7_DAY_QUOTE_VOLUME"),
        "moving_7_day_change_percentage" : dicionario_dados_brutos.get("MOVING_7_DAY_CHANGE_PERCENTAGE"),

        "hr_open": dicionario_dados_brutos.get("CURRENT_HOUR_OPEN"),
        "hr_high": dicionario_dados_brutos.get("CURRENT_HOUR_HIGH"),
        "hr_low": dicionario_dados_brutos.get("CURRENT_HOUR_LOW"),
        "hr_volume_btc": dicionario_dados_brutos.get("CURRENT_HOUR_VOLUME"),
        "hr_change_pct": dicionario_dados_brutos.get("CURRENT_HOUR_CHANGE_PERCENTAGE"),

        "hr_open": dicionario_dados_brutos.get("CURRENT_HOUR_OPEN"),
        "hr_high": dicionario_dados_brutos.get("CURRENT_HOUR_HIGH"),
        "hr_low": dicionario_dados_brutos.get("CURRENT_HOUR_LOW"),
        "hr_volume_btc": dicionario_dados_brutos.get("CURRENT_HOUR_VOLUME"),
        "hr_change_pct": dicionario_dados_brutos.get("CURRENT_HOUR_CHANGE_PERCENTAGE"),

    }
    return key_current_data



