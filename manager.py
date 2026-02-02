import asyncio
from agents.doc_agent import document_agent
from agents.code_agent import code_review_agent
from agents.web_agent import web_research_agent
from redis_queue import push_task, pop_task

MAX_RETRIES = 2

async def run_with_retry(fn, *args):
    for attempt in range(MAX_RETRIES + 1):
        try:
            return await fn(*args)
        except Exception as e:
            if attempt == MAX_RETRIES:
                raise e
            await asyncio.sleep(1)

async def run_task(plan, user_input, stream):
    stream(f"Planner: Task classified as {plan['task_type']}")
    await asyncio.sleep(1)

    task_payload = {
        "task_type": plan["task_type"],
        "input": user_input
    }

    stream("📤 Manager: Enqueuing task into Redis queue")
    push_task(task_payload)
    await asyncio.sleep(1)

    stream("Manager: Waiting for agent worker to pick up task")

    while True:
        task = pop_task()

        if not task:
            await asyncio.sleep(0.5)
            continue

        task_type = task["task_type"]
        data = task["input"]

        stream(f"Manager: Task dequeued from Redis ({task_type})")
        await asyncio.sleep(1)

        if task_type == "document_analysis":
            stream("Document Agent: Received document text")
            result = await run_with_retry(document_agent, [data])
            stream("Document Agent: Analysis completed")
            return result

        if task_type == "code_review":
            stream("Code Agent: Received source code")
            result = await run_with_retry(code_review_agent, [data])
            stream("Code Agent: Review completed")
            return result

        if task_type == "web_research":
            stream("Web Agent: Starting web research")
            result = await run_with_retry(web_research_agent, data)
            stream("Web Agent: Research completed")
            return result
        
        stream("Manager: Unsupported task type")
        return "Unsupported task"