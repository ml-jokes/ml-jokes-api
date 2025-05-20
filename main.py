import os
from dotenv import load_dotenv
import random
from datetime import datetime
from fastapi import FastAPI
from agents import Runner, set_default_openai_key
from services.joke import Joke


load_dotenv()
set_default_openai_key(os.environ["OPENAI_API_KEY"])
app = FastAPI();

#TODO: need to be split and proper orginized
@app.get("/openai_joke")
async def generate_joke():
    funny_guy = Joke()

    unique_id = f"{random.randint(1, 1000000)}-{datetime.now().isoformat()}"
    
    prompt = f"Tell me a new hilarious programming joke I haven't heard before. Be bold, unique, and creative. {unique_id}"
    result = await Runner.run(starting_agent=funny_guy.get_joke_agent(), input=prompt)
    return {"r": result.final_output}
  

@app.post("/openai_joke_feedback")
async def record_feedback():
    return {}


@app.post("/openai_joke_settings")
async def record_settings_for_joke_agent():
    return {}
