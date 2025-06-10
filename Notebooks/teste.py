import asyncio
from typing import Any, Dict, List
from tavily import AsyncTavilyClient

tavily_client = AsyncTavilyClient()

async def fetch_news(queries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Dispara todas as buscas de uma vez e retorna
    a lista com as respostas brutas da API.
    """
    return await asyncio.gather(*(tavily_client.search(**q) for q in queries))


async def filter_and_extract(responses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # 1) filtra
    filtered = [
        result
        for response in responses
        for result   in response.get("results", [])
        if result.get("score", 0) > 0.5
    ]

    # 2) extrai raw_content de uma só vez
    urls = [item["url"] for item in filtered]
    ext_resp = await tavily_client.extract(urls=urls)

    # ext_resp['results'] deve ter a mesma ordem de `urls`
    ext_results = ext_resp.get("results", [])

    # anexa raw_content no próprio dict filtrado
    for item, ext in zip(filtered, ext_results):
        item["raw_content"] = ext.get("raw_content")

    # 3) formata
    formatted = []
    for idx, item in enumerate(filtered, start=1):
        formatted.append({
            "noticia":  f"noticia {idx}",
            "titulo":   item.get("title", ""),
            "url":      item.get("url", ""),
            "conteudo": item.get("raw_content", ""),
            "score":    item.get("score", 0),
        })

    return formatted


async def main():
    # 1) defina suas queries
    queries = [
        {"query": "Bitcoin", "topic": "finance", "search_depth": "advanced", "time_range": "week", "max_results": 3},
    ]

    # 2) busca
    responses = await fetch_news(queries)

    # 3–5) filtra, extrai e formata
    noticias = await filter_and_extract(responses)

    # imprime o resultado
    import pprint
    pprint.pprint(noticias)


if __name__ == "__main__":
    asyncio.run(main())
