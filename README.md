`python src\prepare_vectordb.py`
`python src\prepare_sqldb.py`



import os
import json
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
client = OpenAI()

from coleta_dados_coindesk import (
    fetch_last_3_months_hourly,
    converte_ohlcv_para_df,
    fetch_last_3_months_daily,
    formata_ohlcv_daily,
    fetch_coindesk_latest_tick,
    converte_latest_tick_para_dict,
)
from indicadores_tecnicos import (
    get_latest_bitcoin_indicators,
)
from coleta_noticias import coleta_news_coindesk
from coleta_analises import coleta_analises_profissionais
from prompt import PROMPT
from utils import call_openai_model
from formato_relatório import gerar_relatorio_markdown





def main():
    # 1. Carregar variáveis de ambiente
    load_dotenv()

    # 2. Coleta de dados históricos de OHLCV (Coindesk)
    dados_ohlcv_coindesk = fetch_last_3_months_hourly()
    df_ohlcv_coindesk = converte_ohlcv_para_df(dados_ohlcv_coindesk)
    # 2.1. Coleta de dados históricos de OHLCV diários (Coindesk)
    dados_ohlcv_diarios_coindesk = fetch_last_3_months_daily()
    dados_ohlcv_dict = formata_ohlcv_daily(dados_ohlcv_diarios_coindesk) # Dados que serão passados no prompt

    # 3. Cálculo de indicadores técnicos customizados
    indicadores_pandas_ta = get_latest_bitcoin_indicators(df_ohlcv_coindesk)

    # 4. Coleta do último tick (Coindesk)
    ultimo_tick = fetch_coindesk_latest_tick()
    tick_info = converte_latest_tick_para_dict(ultimo_tick)

    # 5. Mescla indicadores customizados com o último tick
    indicadores = {**indicadores_pandas_ta, **tick_info}

    # 6. Coleta de notícias recentes
    noticias_coindesk = coleta_news_coindesk()

    # 7. Coleta de análises profissionais
    analises_coindesk = coleta_analises_profissionais()

    # 8. Preparação das datas de referência
    hoje = pd.Timestamp.now(tz="America/Sao_Paulo")
    data_hoje = hoje.strftime('%d/%m/%Y')
    data_ontem = (hoje - pd.Timedelta(days=1)).strftime('%d/%m/%Y')

    # 9. Montagem do prompt
    prompt = PROMPT.format(
        data_de_hoje=data_hoje,
        data_de_ontem=data_ontem,
        dados_indicadores=indicadores,
        noticias=noticias_coindesk,
        analises_relevantes=analises_coindesk,
        dados_historicos_ohlcv=dados_ohlcv_dict,
    )

    # 10. Chamada ao modelo OpenAI
    response = call_openai_model(prompt)

    # 11. Conversão da resposta para o modelo BTCReport em Markdown
    relatório = gerar_relatorio_markdown(response)
    with open("relatorio_btc_corrigido4.md", "w", encoding="utf-8") as f:
        f.write(relatório)