# 6. Indicadores Técnicos (podem ser calculados a partir dos dados de mercado ou fornecidos diretamente):
# * Médias Móveis (SMA, EMA).
# * Índice de Força Relativa (RSI).
# * MACD (Moving Average Convergence Divergence).
# * Bandas de Bollinger.
# * Níveis de Suporte e Resistência.
# * Retrações e Extensões de Fibonacci.
# * VWAP (Volume Weighted Average Price).
# * OBV (On-Balance Volume).


import pandas as pd
import numpy as np
import yfinance as yf
import pandas_ta as ta
import json


# Função para coletar indicadores diários do Bitcoin usando a API do Yahoo Finance
def get_bitcoin_data_yf():
    """
    Coleta indicadores referentes ao Bitcoin usando a API pública do Yahoo Finance.

    Retorno:
    - Dicionário:
        'descrição': 'description'
        'preço_anterior': 'previousClose'
        'preço_atual': 'regularmarketPrice'
        'variação_24h': 'regularmarketChange'
        'variação_percentual_24h': 'regularmarketChangePercent'
        'máximo_24h': 'dayHigh'
        'mínimo_24h': 'dayLow'
        'volume_24h': 'regularmarketVolume'
        'volume_10_dias': 'averageDailyVolume10Day'
        'volume_3_meses': 'averageDailyVolume3Month'
        'capitalização_mercado': 'marketCap'
        'fornecimento_circulante': 'circulatingSupply'
        'MSA_50': 'fiftyDayAverage'
        'MSA_50_variacao': 'fiftyDayAverageChange'
        'MSA_50_variacao_percentual': 'fiftyDayAverageChangePercent'
        'MSA_200': 'twoHundredDayAverage'
        'MSA_200_variacao': 'twoHundredDayAverageChange'
        'MSA_200_variacao_percentual': 'twoHundredDayAverageChangePercent'
        'faixa_52_semanas_low': 'fiftyTwoWeekLow'
        'faixa_52_semanas_high': 'fiftyTwoWeekHigh'
        'faixa_52_semanas_low_variacao': 'fiftyTwoWeekLowChange'
        'faixa_52_semanas_low_variacao_percentual': 'fiftyTwoWeekLowChangePercent'
        'faixa_52_semanas_high_variacao': 'fiftyTwoWeekHighChange'
        'faixa_52_semanas_high_variacao_percentual': 'fiftyTwoWeekHighChangePercent'
        'faixa_52_semanas_variacao_percentual': 'fiftyTwoWeekChangePercent'    
    """
    # Definir símbolo e intervalo da API Yahoo Finance
    symbol = "BTC-USD"  # Bitcoin vs USD
    # Coletar dados usando yfinance
    raw_data = yf.Ticker(symbol)
    raw_data_dict = raw_data.get_info()
    # Extraindo os dados relevantes do dicionário raw_data_dict
    bitcoin_data = {
        #"descrição": raw_data_dict.get("description", 0),
        #"preço_anterior": raw_data_dict.get("previousClose", 0),
        #"preço_atual": raw_data_dict.get("regularMarketPrice", 0),
        "variação_24h": raw_data_dict.get("regularMarketChange", 0),
        "variação_percentual_24h": raw_data_dict.get("regularMarketChangePercent", 0),
        "máximo_24h": raw_data_dict.get("dayHigh", 0),
        "mínimo_24h": raw_data_dict.get("dayLow", 0),
        "volume_24h": raw_data_dict.get("volume24Hr", 0),
        "volume_10_dias": raw_data_dict.get("averageDailyVolume10Day", 0),
        "volume_3_meses": raw_data_dict.get("averageDailyVolume3Month", 0),
        "capitalização_mercado": raw_data_dict.get("marketCap", 0),
        "fornecimento_circulante": raw_data_dict.get("circulatingSupply", 0),
        "MSA_50": raw_data_dict.get("fiftyDayAverage", 0),
        "MSA_50_variacao": raw_data_dict.get("fiftyDayAverageChange", 0),
        "MSA_50_variacao_percentual": raw_data_dict.get("fiftyDayAverageChangePercent", 0),
        "MSA_200": raw_data_dict.get("twoHundredDayAverage", 0),
        "MSA_200_variacao": raw_data_dict.get("twoHundredDayAverageChange", 0),
        "MSA_200_variacao_percentual": raw_data_dict.get("twoHundredDayAverageChangePercent", 0),
        "faixa_52_semanas_low": raw_data_dict.get("fiftyTwoWeekLow", 0),
        "faixa_52_semanas_high": raw_data_dict.get("fiftyTwoWeekHigh", 0),
        "faixa_52_semanas_low_variacao": raw_data_dict.get("fiftyTwoWeekLowChange", 0),
        "faixa_52_semanas_low_variacao_percentual": raw_data_dict.get("fiftyTwoWeekLowChangePercent", 0),
        "faixa_52_semanas_high_variacao": raw_data_dict.get("fiftyTwoWeekHighChange", 0),
        "faixa_52_semanas_high_variacao_percentual": raw_data_dict.get("fiftyTwoWeekHighChangePercent", 0),
        "faixa_52_semanas_variacao_percentual": raw_data_dict.get("fiftyTwoWeekChangePercent", 0),
    }
    # Retornar os dados coletados
    dados_indicadores_str = json.dumps(bitcoin_data, indent=2, ensure_ascii=False)
    return dados_indicadores_str

# Função para coletar dados históricos do Bitcoin usando a API do Yahoo Finance
def get_historical_data_yf():
    """
    Coleta dados históricos do Bitcoin usando a API pública do Yahoo Finance.

    Retorno:
    - DataFrame do pandas contendo os dados históricos do Bitcoin.
    """
    # Definir símbolo e intervalo da API Yahoo Finance
    symbol = "BTC-USD"  # Bitcoin vs USD
    # Coletar dados históricos usando yfinance
    raw_data = yf.Ticker(symbol)
    df_dados = raw_data.history(period="1y", interval="1d")
    #Deixando apenas as colunas "Date" e "Close"
    df_dados = df_dados.reset_index()
    df_dados = df_dados[['Date', 'Close']]
    #Alterando a coluna "Date" para o formato DD/MM/AAAA
    df_dados['Date'] = df_dados['Date'].dt.strftime('%d/%m/%Y')
    hist_list_of_dicts = df_dados.to_dict(orient='records')
    dados_historicos_str = json.dumps(hist_list_of_dicts, indent=2)
    # Retornar os dados coletados
    return dados_historicos_str


# Função para calcular indicadores técnicos usando a biblioteca pandas_ta
def get_latest_bitcoin_indicators(dataframe):
    """
    Coleta dados de OHLCV do Bitcoin (3 meses, candles de 1h),
    calcula os indicadores técnicos via ta.Strategy,
    remove as colunas de preço, e retorna um dicionário com
    apenas os valores mais recentes de cada indicador.
    """
    # 1. Baixar dados OHLCV de BTC-USD (últimos 3 meses, intervalo 1h)
    ohlc_df = dataframe
    # ohlc_df.index = pd.DatetimeIndex(ohlc_df.index)
    # ohlc_df = ohlc_df.tz_convert("America/Sao_Paulo")

    # 2. Definir a Strategy para os indicadores desejados
    MyStrategy = ta.Strategy(
        name="BitcoinIndicators",
        ta=[
            # Médias Móveis Simples
            {"kind": "sma", "length": 20},
            {"kind": "sma", "length": 50},
            {"kind": "sma", "length": 200},
            # Médias Móveis Exponenciais
            {"kind": "ema", "length": 20},
            {"kind": "ema", "length": 50},
            {"kind": "ema", "length": 200},
            # Índice de Força Relativa
            {"kind": "rsi", "length": 14},
            # MACD (12, 26, 9)
            {"kind": "macd","fast": 12, "slow": 26, "signal": 9},
            # Bandas de Bollinger (20, 2)
            {"kind": "bbands","length": 20, "std": 2},
        ]
    )

    # 3. Aplicar a Strategy ao DataFrame de OHLCV
    ohlc_df.ta.strategy(MyStrategy)

    # 4. Remover colunas de preço para ficar apenas com indicadores
    price_cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']
    indicators_df = ohlc_df.drop(columns=[c for c in price_cols if c in ohlc_df.columns])

    # 5. Obter a última linha de indicadores e converter para dicionário
    latest_series = indicators_df.iloc[-1]
    latest_dict = latest_series.to_dict()

    return latest_dict