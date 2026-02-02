def plan_task(user_input: str):
    text = user_input.lower()

    if any(k in text for k in ["pdf", "document", "analyze document"]):
        return {
            "task_type": "document_analysis",
            "steps": ["load", "analyze", "write"]
        }

    if any(k in text for k in ["code", "bug", "review", "optimize"]):
        return {
            "task_type": "code_review",
            "steps": ["parse", "analyze", "review"]
        }

    if any(k in text for k in ["research", "web", "search"]):
        return {
            "task_type": "web_research",
            "steps": ["search", "scrape", "analyze", "write"]
        }

    return {"task_type": "unsupported", "steps": []}
