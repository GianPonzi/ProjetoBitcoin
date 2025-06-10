import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# Importa o template do prompt que você irá editar
from agents.prompt import PROMPT
# Importa a função de chamada da OpenAI que você já tem
from utils import call_openai_model 

def testar_prompt_com_dados_cacheados():
    """
    Carrega os dados salvos, formata o prompt mais recente e chama a IA.
    """
    print("--- Iniciando teste de prompt com dados em cache ---")

    # 1. Carrega as variáveis de ambiente para a chave da API
    load_dotenv()
    client = OpenAI()

    # 2. Carrega o contexto de dados do arquivo JSON
    try:
        with open("contexto_cache.json", "r", encoding="utf-8") as f:
            contexto = json.load(f)
        print("Dados do cache carregados com sucesso.")
    except FileNotFoundError:
        print("[ERRO] Arquivo 'contexto_cache.json' não encontrado.")
        print("Você precisa executar o 'agente.py' pelo menos uma vez para gerar este arquivo.")
        return
    except Exception as e:
        print(f"[ERRO] Falha ao carregar o arquivo de cache: {e}")
        return

    # 3. Monta o prompt usando o template mais recente de 'prompt.py'
    try:
        prompt_final = PROMPT.format(**contexto)
        print("\n--- PROMPT FINAL ENVIADO PARA A IA ---")
        #print(prompt_final)
        print("--------------------------------------")
    except KeyError as e:
        print(f"[ERRO] A chave {e} está faltando no seu PROMPT_TEMPLATE ou no arquivo de cache.")
        return

    # 4. Chama o modelo da OpenAI e imprime a resposta
    print("\nEnviando prompt para a OpenAI...")
    try:
        # Aqui você pode chamar a função que formata a resposta também, se quiser
        resposta = call_openai_model(prompt_final)
        print("\n--- RESPOSTA DA IA ---")
        print(resposta)
        print("----------------------")
    except Exception as e:
        print(f"Erro ao chamar a API da OpenAI: {e}")

if __name__ == "__main__":
    testar_prompt_com_dados_cacheados()