import os
from dotenv import load_dotenv
import random
from datetime import datetime
from fastapi import FastAPI
from agents import Agent, Runner, set_default_openai_key, ModelSettings, WebSearchTool, input_guardrail, GuardrailFunctionOutput


load_dotenv()
set_default_openai_key(os.environ["OPENAI_API_KEY"])
app = FastAPI();

#TODO: need to be split and proper orginized
@app.get("/openai_joke")
async def generate_joke():

    #agent as a tool
    languageAgent = Agent(name="language agent",  model="gpt-4o-mini", instructions="You translate the response to English")

    #guardrail agent
    joke_related_question_guardrail = Agent(name="guard rail agent",  model="gpt-4o-mini", instructions="Make sure I am asking to generate joke in valid topic")

    @input_guardrail
    async def joke_guardrail(context, agent: Agent, input: str) -> GuardrailFunctionOutput:
        return GuardrailFunctionOutput(output_info={}, tripwire_triggered=False)

    clown = Agent(
        name="Clown", 
        instructions=(
            "You are joke inventor."
            "Make sure it's never the same."
            "Always use translate_to_language tool to make sure final response is translated"
        ), 
        model="gpt-4o-mini",
        model_settings=ModelSettings(temperature=1.9, max_tokens=150, top_p=0.9),
        tools=[WebSearchTool(), languageAgent.as_tool(tool_name="translate_to_language", tool_description="it will translate response to selected language")],
        input_guardrails=[joke_guardrail]
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
