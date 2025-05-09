import os
from dotenv import load_dotenv
import random
from datetime import datetime
from fastapi import FastAPI
from agents import Agent, Runner, set_default_openai_key, ModelSettings
from fastapi.concurrency import run_in_threadpool


load_dotenv()
set_default_openai_key(os.environ["OPENAI_API_KEY"])
app = FastAPI();


@app.get("/openai_joke")
async def generate_joke():
    clown = Agent(
        name="Clown", 
        instructions=(
            "You are joke inventor. "
            "Make sure it's never the same. "
            "Always respond in English."
        ), 
        model="gpt-4o-mini",
        model_settings=ModelSettings(temperature=1.9, max_tokens=150, top_p=0.9)
    )
    unique_id = f"{random.randint(1, 1000000)}-{datetime.now().isoformat()}"
    
    prompt = f"Tell me a new hilarious programming joke I haven't heard before. Be bold, unique, and creative. {unique_id}"
    
    result = await Runner.run(starting_agent=clown, input=prompt)
    return {"r": result.final_output}
  

@app.post("/openai_joke_feedback")
async def record_feedback():
    return {}


@app.post("/openai_joke_settings")
async def record_settings_for_joke_agent():
    return {}
