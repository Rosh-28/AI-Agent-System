import asyncio
from ollama_client import call_ollama
from batching import batch_items

async def analyze_documents_batch(docs):
    prompt = (
        "Analyze the following documents and extract risks:\n\n"
        + "\n\n".join(docs)
    )
    return call_ollama(prompt)

async def document_agent(documents: list, stream=None):
    if stream:
        stream("Document Agent: Ingesting document")

    results = []

    for batch, idx, total in batch_items(documents):
        if stream:
            stream(f"Analyzer: Analyzing document batch {idx}/{total}")

        await asyncio.sleep(1)
        result = await analyze_documents_batch(batch)
        results.append(result)

    if stream:
        stream("Writer: Writing executive summary")

    return "\n".join(results)

