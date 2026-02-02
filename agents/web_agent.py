import asyncio
import requests
from bs4 import BeautifulSoup
from ollama_client import call_ollama
from batching import batch_items

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_article_links(query):
    url = "https://lite.duckduckgo.com/lite/"
    payload = {
        "q": query
    }

    response = requests.post(url, data=payload, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("http"):
            links.append(href)

    return links[:3]


def scrape_article(url):
    html = requests.get(url, headers=HEADERS, timeout=10).text
    soup = BeautifulSoup(html, "html.parser")
    paragraphs = [p.text for p in soup.find_all("p")]
    return " ".join(paragraphs[:8])

async def analyze_batch(texts):
    prompt = (
        "Summarize key points from the following:\n\n"
        + "\n\n".join(texts)
    )
    return call_ollama(prompt)

async def web_research_agent(query: str, stream=None):
    if stream:
        stream("Retriever: Searching web")

    links = get_article_links(query)

    if stream:
        stream(f"Retriever: Found {len(links)} article links")

    if not links:
        return "No articles found."

    contents = [scrape_article(link) for link in links if link]
    contents = [c for c in contents if len(c.strip()) > 200]

    if stream:
        stream(f"Retriever: Extracted {len(contents)} readable articles")

    results = []

    for batch, idx, total in batch_items(contents):
        if stream:
            stream(f"Analyzer: Processing batch {idx}/{total}")

        await asyncio.sleep(1)
        result = await analyze_batch(batch)
        results.append(result)

    if stream:
        stream("Writer: Generating final research summary")

    return "\n\n".join(results)
