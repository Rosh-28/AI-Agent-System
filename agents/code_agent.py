import asyncio
from ollama_client import call_ollama
from batching import batch_items

async def review_code_batch(codes):
    prompt = (
        "Review the following code and point out bugs, bad practices, and improvements:\n\n"
        + "\n\n".join(codes)
    )
    return call_ollama(prompt)

async def code_review_agent(code_snippets: list, stream=None):
    if stream:
        stream("Code Agent: Preparing code for review")

    reviews = []

    for batch, idx, total in batch_items(code_snippets):
        if stream:
            stream(f"Analyzer: Reviewing code batch {idx}/{total}")
        await asyncio.sleep(1)
        result = await review_code_batch(batch)
        reviews.append(result)

    if stream:
        stream("Writer: Finalizing code review")

    return "\n".join(reviews)

