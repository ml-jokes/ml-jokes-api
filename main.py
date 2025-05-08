import os
from dotenv import load_dotenv
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
            "Gnerate a funny dev jokes.",
            "Make sure it does not repeat."
        ), 
        model="gpt-4.1-nano",
        model_settings=ModelSettings(temperature=0.9)
    )
    result = await Runner.run(starting_agent=clown, input="Give me random funny dev joke.")
    return {"r": result.final_output}
  

@app.post("/openai_joke_feedback")
async def record_feedback():
    return {}


@app.post("/openai_joke_settings")
async def record_settings_for_joke_agent():
    return {}
