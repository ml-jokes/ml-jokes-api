from datetime import datetime
import random
from agents import Runner
from fastapi import APIRouter
from services.joke import Joke

router = APIRouter(prefix="/joke")

@router.get("/generate")
async def generate_joke():
    funny_guy = Joke()

    unique_id = f"{random.randint(1, 1000000)}-{datetime.now().isoformat()}"
    
    prompt = f"Tell me a new hilarious programming joke I haven't heard before. Be bold, unique, and creative. {unique_id}"
    result = await Runner.run(starting_agent=funny_guy.get_joke_agent(), input=prompt)
    return {"r": result.final_output}