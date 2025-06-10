from datetime import datetime
from typing import Dict
from utils import BTCReport



relatório = """
📌 Resumo de Mercado – 06 de Junho de 2025
• Preço Atual: US$ 84.411,00
• Variação 24h: +0,62%
• Máxima 24h: US$ 85.312,00
• Mínima 24h: US$ 83.536,00
• Volume 24h: US$ 27,13 bilhões
• Capitalização de Mercado: US$ 1,68 trilhão
• Fornecimento Circulante: 19,85 milhões BTC
• Fornecimento Máximo: 21 milhões BTC


📊 Análise Técnica
• Médias Móveis (MA):
• MA 50 dias: US$ 85.000 (atuando como resistência dinâmica)
• MA 200 dias: US$ 80.000 (servindo como suporte de longo prazo)
• Cruzamento de Médias: Ocorreu recentemente um “cruzamento dourado”, onde a MA de 50 dias cruzou acima da MA de 200 dias, sugerindo uma tendência de alta de longo prazo.
• Índice de Força Relativa (RSI):
• Atualmente em 68, indicando que o ativo está se aproximando da zona de sobrecompra.
• Bandas de Bollinger:
• As bandas estão se estreitando, sinalizando uma redução na volatilidade e possivelmente antecipando um movimento de preço significativo.


🔍 Níveis de Suporte e Resistência
• Suportes:
• US$ 83.900: Suporte imediato observado recentemente.
• US$ 83.061: Próximo nível de suporte técnico.
• US$ 82.478: Alinhado com a média móvel de 200 períodos, servindo como um suporte chave. ￼
• Resistências:
• US$ 84.500 – US$ 84.700: Zona de resistência onde o preço enfrentou rejeições.
• US$ 86.200: Próximo nível de resistência observado.
• US$ 88.600: Resistência adicional a ser monitorada.


📰 Notícias Recentes
• Notícia 1: "Bitcoin atinge novo recorde histórico"
• Link: https://www.binance.com/bitcoin-news
• Resumo: Bitcoin abaixo de US$ 85 mil causa saídas de US$ 171 milhões de ETFs: O Bitcoin tem enfrentado dificuldade significativa em superar a marca de US$ 85 mil nesta semana, e seu preço permanece estagnado abaixo dessa resistência chave. Assim, os entusiastas do BTC estão cada vez mais frustrados. Isso porque a criptomoeda luta para manter o impulso ascendente. Junto com essa estagnação de preço, houve uma queda no interesse aberto e saídas de ETFs, refletindo a crescente incerteza no mercado. 

• Notícia 2: "Adoção institucional do Bitcoin cresce" 
• Link: https://www.binance.com/bitcoin-news
• Resumo: Grandes instituições financeiras estão aumentando suas participações em Bitcoin, sinalizando uma crescente aceitação do ativo digital.


💡 Considerações Estratégicas
• Para Compradores:
• Considerar entradas próximas ao suporte de US$ 83.000, visando uma possível valorização até a resistência de US$ 85.500.
• Para Vendedores:
• Observar a resistência em US$ 85.500 como um possível ponto de realização de lucros, ajustando stops conforme a volatilidade do mercado.


✅ Conclusão
O Bitcoin apresenta uma leve tendência de alta no curto prazo, com suporte em US$ 83.000 e resistência em US$ 85.500. Fatores externos, como políticas econômicas e eventos globais, continuam influenciando o mercado. Recomenda-se monitorar os níveis de suporte e resistência mencionados e estar atento às notícias que possam impactar o valor do ativo.


⚠️ Aviso: Ao realizar operações de compra ou venda, é importante estar ciente de que o preço do Bitcoin pode sofrer variações devido a movimentos de mercado e notícias que possam impactar seu valor.
"""


def gerar_relatorio_markdown(report) -> str:
    hoje = datetime.now()
    data_pt = hoje.strftime("%d de %B de %Y")
    
    md = []
    # Título Principal (H1)
    md.append(f"# RELATÓRIO DIÁRIO QBITS (BTC)")
    md.append("")

    # Resumo de Mercado (H3)
    md.append(f"### 📌 Resumo de Mercado – {data_pt}") # <-- ALTERADO
    md.append(f"* **Preço Atual:** {report.resumo.preco_atual}")
    md.append(f"* **Variação 24h:** {report.resumo.variacao_24h_pct}")
    md.append(f"* **Máxima 24h:** {report.resumo.max_24h}")
    md.append(f"* **Mínima 24h:** {report.resumo.min_24h}")
    md.append(f"* **Volume 24h:** {report.resumo.volume_24h}")
    md.append(f"* **Capitalização de Mercado:** {report.resumo.market_cap}")
    md.append(f"* **Fornecimento Circulante:** {report.resumo.fornecimento_circulante}")
    md.append(f"* **Fornecimento Máximo:** {report.resumo.fornecimento_max}")
    md.append("")

    # Análise Técnica (H3)
    md.append("### 📊 Análise Técnica")
    md.append("")
    md.append("* **Médias Móveis (MA):**")
    # Abaixo, uma lista ANINHADA. A indentação (4 espaços) é crucial.
    md.append(f"    * **MA 50 dias:** {report.analise_tecnica.sma50} || _{report.analise_tecnica.sma50_interpretacao}_")
    md.append(f"    * **MA 200 dias:** {report.analise_tecnica.sma200} || _{report.analise_tecnica.sma200_interpretacao}_")
    md.append(f"* **Cruzamento de Médias:** {report.analise_tecnica.cruzamento_medias_interpretacao}")
    md.append(f"* **RSI:** {report.analise_tecnica.rsi} || _{report.analise_tecnica.rsi_interpretacao}_")
    md.append(f"* **Bandas de Bollinger:** _{report.analise_tecnica.bollinger_interpretacao}_")
    md.append("")

    # Suportes e Resistências (H3)
    sup = report.suporte_resistencia
    md.append("### 🔍 Níveis de Suporte e Resistência") # <-- ALTERADO
    md.append("**Suportes:**")
    md.append(f"* **{sup.suporte1.nivel_suporte_valor}:** {sup.suporte1.nivel_suporte_interpretacao}")
    md.append(f"* **{sup.suporte2.nivel_suporte_valor}:** {sup.suporte2.nivel_suporte_interpretacao}")
    md.append(f"* **{sup.suporte3.nivel_suporte_valor}:** {sup.suporte3.nivel_suporte_interpretacao}")
    md.append("") 
    md.append("**Resistências:**")
    md.append(f"* **{sup.resistencia1.nivel_resistencia_valor}:** {sup.resistencia1.nivel_resistencia_interpretacao}")
    md.append(f"* **{sup.resistencia2.nivel_resistencia_valor}:** {sup.resistencia2.nivel_resistencia_interpretacao}")
    md.append(f"* **{sup.resistencia3.nivel_resistencia_valor}:** {sup.resistencia3.nivel_resistencia_interpretacao}")
    md.append("")

    # Notícias (H3)
    md.append("### 📰 Notícias Recentes") # <-- ALTERADO
    md.append(f"**Notícia 1:** \"_{report.noticias.noticia1.titulo}_\"")
    md.append(f"  * **Link:** {report.noticias.noticia1.link}")
    md.append(f"  * **Resumo:** {report.noticias.noticia1.resumo}")
    md.append("")
    md.append(f"**Notícia 2:** \"_{report.noticias.noticia2.titulo}_\"")
    md.append(f"  * **Link:** {report.noticias.noticia2.link}")
    md.append(f"  * **Resumo:** {report.noticias.noticia2.resumo}")
    md.append("")

    # Estratégias (H3)
    md.append("### 💡 Considerações Estratégicas") # <-- ALTERADO
    md.append("")
    md.append(f"* **Para Compradores:** {report.estrategias.compradores}")
    md.append(f"* **Para Vendedores:** {report.estrategias.vendedores}")
    md.append("")

    # Estratégias OCO (H3)
    md.append("### 📙 Estratégias para OCO") # <-- ALTERADO
    md.append("")
    md.append(f"* **Para Compradores:** {report.estrategias_oco.compradores}")
    md.append(f"* **Para Vendedores:** {report.estrategias_oco.vendedores}")
    md.append("")

    # Conclusão e Aviso (H3)
    md.append("### ✅ Conclusão") # <-- ALTERADO
    md.append(f" {report.conclusao}")
    md.append("")
    md.append("---")
    md.append("")
    md.append("⚠️ **Aviso:** *Ao realizar operações de compra ou venda, é importante estar ciente de que o preço do Bitcoin pode sofrer variações devido a movimentos de mercado e notícias que possam impactar seu valor.*")

    return "\n".join(md)		


# with open("relatorio_btc_corrigido4.md", "w", encoding="utf-8") as f:
#     f.write(md_corrigido)