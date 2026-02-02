import streamlit as st
import asyncio
from planner import plan_task
from manager import run_task

st.set_page_config(page_title="Agentic AI System", layout="centered")
st.title("Agentic AI System")

user_input = st.text_area("Enter your task / document / code")
run_btn = st.button("Run Task")

status = st.empty()
output = st.empty()

def stream(msg):
    status.info(msg)

if run_btn and user_input:
    plan = plan_task(user_input)
    st.subheader("🧠 Execution Plan")
    st.json(plan)

    async def exec():
        return await run_task(plan, user_input, stream)

    result = asyncio.run(exec())
    output.success("✅ Completed")
    st.write(result)
