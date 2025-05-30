import os
from dotenv import load_dotenv
from fastapi import FastAPI
from agents import set_default_openai_key
from routers.jokes import router as jokes_router


load_dotenv()
set_default_openai_key(os.environ["OPENAI_API_KEY"])
app = FastAPI();

app.include_router(jokes_router)


@app.post("/openai_joke_feedback")
async def record_feedback():
    return {}


@app.post("/openai_joke_settings")
async def record_settings_for_joke_agent():
    return {}
