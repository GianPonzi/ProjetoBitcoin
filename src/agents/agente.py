
import pandas as pd
import json
import os
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

    # Etapa 2. Preparação das datas e do contexto do relatório
    hoje = pd.Timestamp.now(tz="America/Sao_Paulo")
    contexto_do_relatorio = {
        "data_de_hoje": hoje.strftime('%d/%m/%Y'),
        "data_de_ontem": (hoje - pd.Timedelta(days=1)).strftime('%d/%m/%Y'),
        "coindesk_ohlcv_3months_hours": None,
        "coindesk_ohlcv_3months_daily": "Dados históricos não disponíveis.",
        "dados_indicadores": "Indicadores técnicos não disponíveis.",
        "noticias": "Notícias não disponíveis.",
        "analises_openai": "Análises profissionais não disponíveis."
    }

    
    print("Iniciando a geração do relatório de Bitcoin...")

    # Etapa 3.1: Coleta de dados brutos horários
    try:
        # Coleta de dados históricos de OHLCV (Coindesk)
        dados_ohlcv_coindesk = fetch_last_3_months_hourly()
        contexto_do_relatorio["coindesk_ohlcv_3months_hours"] = converte_ohlcv_para_df(dados_ohlcv_coindesk)
        print("[SUCESSO] Dados horários de mercado coletados e convertidos para DataFrame.")
    except Exception as e:
        print(f"[FALHA] Etapa 3.1 - Não foi possível obter os dados horários: {e}")
    
    # Etapa 3.2: Coleta de dados brutos diários   
    try:
        # Coleta de dados históricos de OHLCV diários (Coindesk)
        dados_ohlcv_diarios_coindesk = fetch_last_3_months_daily()
        contexto_do_relatorio["coindesk_ohlcv_3months_daily"] = formata_ohlcv_daily(dados_ohlcv_diarios_coindesk) # Dados que serão passados no prompt
        print("[SUCESSO] Dados diários de mercado coletados e formatados.")
    except Exception as e:
        print(f"[FALHA] Etapa 3.2 - Não foi possível obter os dados diários: {e}")


    # Etapa 4: Cálculo de indicadores técnicos e coleta do último tick
    try:
        # Cálculo de indicadores técnicos customizados
        indicadores_pandas_ta = get_latest_bitcoin_indicators(contexto_do_relatorio["coindesk_ohlcv_3months_hours"])
        # Coleta do último tick (Coindesk)
        ultimo_tick = fetch_coindesk_latest_tick()
        tick_info = converte_latest_tick_para_dict(ultimo_tick)
        # Mescla indicadores customizados com o último tick
        contexto_do_relatorio['dados_indicadores'] = {**indicadores_pandas_ta, **tick_info}
        print("[SUCESSO] Indicadores técnicos calculados e mesclados com o último tick.")
    except Exception as e:
        print(f"[FALHA] Etapa 4 - Não foi possível calcular os indicadores ou obter o último tick: {e}")


    # Etapa 5.1: Coleta de notícias
    try:
        # Coleta de notícias recentes
        contexto_do_relatorio['noticias'] = coleta_news_coindesk()
        print("[SUCESSO] Notícias recentes coletadas.")
    except Exception as e:
        print(f"[FALHA] Etapa 5.1 - Não foi possível coletar notícias: {e}")

    # Etapa 5.2: Coleta de análises
    try:
        # Coleta de notícias recentes
        contexto_do_relatorio['analises_openai'] = coleta_analises_profissionais()
        print("[SUCESSO] Análises profissionais coletadas.")
    except Exception as e:
        print(f"[FALHA] Etapa 5.2 - Não foi possível coletar análises profissionais: {e}")
    
    
    # Etapa 6: Montagem e chamada da IA
    # -------- NOVO BLOCO DE CÓDIGO PARA SALVAR O CONTEXTO --------
    print("\nSalvando o contexto de dados em 'contexto_cache.json'...")
    try:
        # Criamos uma cópia para não modificar o dicionário original
        contexto_para_salvar = contexto_do_relatorio.copy()
        if 'coindesk_ohlcv_3months_hours' in contexto_para_salvar:
            del contexto_para_salvar['coindesk_ohlcv_3months_hours']

        with open("contexto_cache.json", "w", encoding="utf-8") as f:
            json.dump(contexto_para_salvar, f, indent=4, ensure_ascii=False)
        print("[SUCESSO] Contexto salvo.")
    except Exception as e:
        print(f"[FALHA] Não foi possível salvar o arquivo de cache do contexto: {e}")
    # -------- FIM DO BLOCO DE CÓDIGO PARA SALVAR O CONTEXTO --------
    print("\nMontando prompt e chamando a API da OpenAI...")
    relatorio = "# Erro na Geração do Relatório\n\nCausa: Falha ao formatar o prompt ou ao chamar a API da OpenAI."
    try:
        prompt_final = PROMPT.format(**contexto_do_relatorio)
        response = call_openai_model(prompt_final)
        relatorio = gerar_relatorio_markdown(response)
        print("[SUCESSO] Resposta da OpenAI recebida e relatório formatado.")
    except KeyError as e:
        print(f"[FALHA CRÍTICA] Etapa 6 - Chave faltando no template do prompt: {e}")
    except Exception as e:
        print(f"[FALHA CRÍTICA] Etapa 6 - Erro ao chamar a OpenAI ou formatar a resposta: {e}")
    

    # Etapa 7: Salvando o arquivo final
    nome_arquivo = f"relatorio_btc_{hoje.strftime('%Y-%m-%d_%H-%M-%S')}.md"
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(relatorio)
        print(f"\n[FINALIZADO] Relatório salvo com sucesso em: {nome_arquivo}")
    except Exception as e:
        print(f"[FALHA CRÍTICA] Etapa 7 - Não foi possível salvar o arquivo do relatório: {e}")

if __name__ == "__main__":
    main()