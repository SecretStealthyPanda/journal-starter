import json

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

from api.config import get_settings


def _default_client() -> AsyncOpenAI:
    settings = get_settings()
    return AsyncOpenAI(
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
    )


async def analyze_journal_entry(
    entry_id: str,
    entry_text: str,
    client: AsyncOpenAI | None = None,
) -> dict:
    if client is None:
        client = _default_client()
    messages: list[ChatCompletionMessageParam] = [
        {
            "role": "system",
            "content": "Analyze the user's journal entry and respond with JSON containing sentiment, summary, and key topics. Return only JSON, no explanatory text.",
        },
        {"role": "user", "content": entry_text},
    ]
    response = await client.chat.completions.create(
        model=get_settings().openai_model,
        messages=messages,
    )
    content = response.choices[0].message.content
    if content is None:
        return {
            "entry_id": entry_id,
            "sentiment": None,
            "summary": "No analysis available",
            "topics": [],
        }
    result = json.loads(content)
    return {
        "entry_id": entry_id,
        "sentiment": result.get("sentiment"),
        "summary": result.get("summary"),
        "topics": result.get("topics", []),
    }
