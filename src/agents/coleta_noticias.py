# Funções de coletas e tratamento de noticias relacionadas ao Bitcoin. Serão usados as bibliotecas yfinance e Tavily para coletar as informações necessárias.
import requests
from datetime import datetime
import yfinance as yf
from tavily import AsyncTavilyClient
from dotenv import load_dotenv
import asyncio
from datetime import datetime
import pytz
import os


load_dotenv()

# Configuração do cliente Tavily
tavily_client = AsyncTavilyClient()

# Função de coleta de noticias Tavily:
async def coleta_news_tavily():
    # Define the queries with search_depth and max_results inside the query dictionary
    queries = [
        {"query": "Bitcoin", "topic": "news", "search_depth": "advanced", "time_range": "day","max_results": 4},
        {"query": "Bitcoin price analysis", "topic": "news", "search_depth": "advanced", "time_range": "day", "max_results": 3},
        {"query": "Bitcoin Fear & Greed Index", "topic": "news", "search_depth": "advanced", "time_range": "week", "max_results": 2},
    ]

    # Perform the search queries concurrently, passing the entire query dictionary
    responses = await asyncio.gather(*[tavily_client.search(**q) for q in queries])

    # Retorna o resultado:
    return responses

# Função que formata as respostas em um novo dicionario estruturado:
def format_tavily_search_news(responses):

    search_response = responses
    list_dict_news = []

    for response in search_response:
        for item in response.get('results', []):
            list_dict_news.append({
                'titulo': item.get('title'),
                'url': item.get('url'),
                'data': item.get('published_date'),
                'resumo': item.get('content'),
                'score': item.get('score'),
            })
    return list_dict_news

# ---------------------------------------------------------------------------------------------------------- #

# Função para coletar noticias do Bitcoin usando a API do Yahoo Finance: ✅
def coleta_noticias_yfinance():
    """
    Busca as últimas notícias sobre Bitcoin (BTC-USD) usando a biblioteca yfinance,
    processa os dados e retorna uma lista de notícias formatadas.

    Returns:
        list: Uma lista de dicionários, cada um representando uma notícia.
              Retorna uma lista vazia caso ocorra um erro ou nenhuma notícia seja encontrada.
    """
    # 1. Tenta buscar os dados da API
    try:
        ticker = yf.Ticker('BTC-USD')
        # Usamos .news() que é o método mais atual da biblioteca
        api_response = ticker.news
        if not api_response:
            print("[AVISO] Nenhuma notícia encontrada para BTC-USD no Yahoo Finance.")
            return []
    except Exception as e:
        print(f"[ERRO] Falha ao buscar notícias do Yahoo Finance: {e}")
        return []

    # 2. Processa a resposta da API
    noticias_extraidas = []
    fuso_horario_local = pytz.timezone("America/Sao_Paulo")
    formato_data_saida = "%d/%m/%Y %H:%M:%S %Z"

    for entry in api_response:
        # Acesso ao dicionário 'content' que contém os dados principais
        content = entry.get('content', {})
        if not content:
            continue # Pula para o próximo item se 'content' for vazio

        # Pega a data/hora original (string no formato ISO 8601 com 'Z')
        raw_date_str = content.get('pubDate')

        if raw_date_str:
            # Converte a string para um objeto datetime...
            dt_naive = datetime.strptime(raw_date_str, "%Y-%m-%dT%H:%M:%SZ")
            # ... e o torna ciente do fuso horário UTC
            dt_utc = dt_naive.replace(tzinfo=pytz.UTC)
            
            # Converte do fuso UTC para o fuso local de São Paulo
            dt_local = dt_utc.astimezone(fuso_horario_local)
            
            # Formata a data local para o formato de texto desejado
            data_formatada = dt_local.strftime(formato_data_saida)
        else:
            data_formatada = None

        # Acessa a URL de forma segura, pois ela também está aninhada
        url_canonica = content.get('canonicalUrl', {}).get('url')

        noticias_extraidas.append({
            'titulo': content.get('title'),
            'resumo': content.get('summary', 'Resumo não disponível.'),
            'data': data_formatada,
            'url': url_canonica
        })

    return noticias_extraidas


# ---------------------------------------------------------------------------------------------------------- #
# Função para coletar noticias da Coindesk API: ✅
def coleta_news_coindesk():
    """
    Extrai campos (TITLE, URL, KEYWORDS, SENTIMENT, PUBLISHED_ON, BODY) da segunda API.
    Converte PUBLISHED_ON (timestamp UTC em segundos) para formato legível.
    """
    api_key = os.getenv("COINDESK_API_KEY")
    # Parametros de requisição:
    url = 'https://data-api.coindesk.com/news/v1/article/list'
    params={"lang":"EN", "limit":10, "categories":"BTC,MARKET", "api_key": api_key}
    headers={"Content-type":"application/json; charset=UTF-8"}
    
    # Requisição para a API Coindesk:
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        json_response = response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Falha ao se comunicar com a API da Coindesk: {e}")
        return []
    
    # Preocessando dados:
    noticias_extraidas = []
    fuso_horario_local = pytz.timezone("America/Sao_Paulo")
    formato_data = "%d/%m/%Y %H:%M:%S %Z"

    for entry in json_response.get('Data', []):
        raw_ts = entry.get('PUBLISHED_ON')
        if raw_ts:
            # Converte timestamp UTC para datetime e depois para o fuso local
            dt_utc = datetime.fromtimestamp(raw_ts, tz=pytz.UTC)
            dt_local = dt_utc.astimezone(fuso_horario_local)
            # Formatação direta, sem função auxiliar
            data_formatada = dt_local.strftime(formato_data)
        else:
            data_formatada = None

        noticias_extraidas.append({
            'titulo': entry.get('TITLE'),
            'url': entry.get('URL'),
            'keywords': entry.get('KEYWORDS'),
            'sentimento': entry.get('SENTIMENT'),
            'data': data_formatada,
            'resumo': entry.get('BODY')
        })
    return noticias_extraidas

#################################################################################################################