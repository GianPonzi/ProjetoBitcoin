# Coleta de analises profissionais: ✅
from openai import OpenAI
from prompt import PROMPT_EXTRACTION_ANALYSIS
client = OpenAI()


def coleta_analises_profissionais():
    prompt = PROMPT_EXTRACTION_ANALYSIS
    response = client.responses.create(
        model="gpt-4.1",
        tools=[{"type": "web_search_preview", "search_context_size": "high"}],
        input=prompt,
        )
    analises = response.output_text
    return analises