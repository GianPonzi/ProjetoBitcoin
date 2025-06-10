# Criando uma classe com esquema Pydantic com os valores do relatório
from pydantic import BaseModel, Field

class Resumo_de_Mercado(BaseModel):
    preco_atual: float 
    variacao_24h_pct: float
    max_24h: float
    min_24h: float
    volume_24h: float
    market_cap: float
    fornecimento_circulante: float
    fornecimento_max: float

class Analise_Tecnica(BaseModel):
    sma50: float 
    sma50_interpretacao: str 
    sma200: float 
    sma200_interpretacao: str 
    cruzamento_medias_interpretacao: str 
    rsi: float 
    rsi_interpretacao: str 
    bollinger_interpretacao: str                           

class Nivel_Suporte(BaseModel):
    nivel_suporte_valor: float 
    nivel_suporte_interpretacao: str 

class Nivel_Resistencia(BaseModel):
    nivel_resistencia_valor: float 
    nivel_resistencia_interpretacao: str 

class Suporte_Resistencia(BaseModel):
    suporte1: Nivel_Suporte
    suporte2: Nivel_Suporte
    suporte3: Nivel_Suporte
    resistencia1: Nivel_Resistencia
    resistencia2: Nivel_Resistencia
    resistencia3: Nivel_Resistencia

class Noticia(BaseModel):
    titulo: str
    link: str 
    resumo: str

class Noticias(BaseModel):
    noticia1: Noticia
    noticia2: Noticia

class Estrategias(BaseModel):
    compradores: str 
    vendedores: str 

class Estrategias_OCO(BaseModel):
    compradores: str 
    vendedores: str

class BTCReport(BaseModel):
    resumo: Resumo_de_Mercado
    analise_tecnica: Analise_Tecnica
    suporte_resistencia: Suporte_Resistencia
    noticias: Noticias
    estrategias: Estrategias
    estrategias_oco: Estrategias_OCO
    conclusao: str

###########################################################################
# Função para chamar o modelo da OpenAI
def call_openai_model(prompt: str) -> str:
    from openai import OpenAI
    client = OpenAI()
    
    response = client.responses.parse(
    model="o3-mini",
    input=[
        {
            "role": "system",
            "content": prompt,
        },
    ],
    text_format=BTCReport,
    )
    resultado = response.output_parsed
    return resultado