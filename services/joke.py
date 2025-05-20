from agents import Agent, WebSearchTool, Tool, ModelSettings, input_guardrail, GuardrailFunctionOutput, Runner
from models.MainJokeRailOutput import JokeRailOutput

class Joke:
    def __init__(self):
     pass

    def get_joke_agent(self) -> Agent:
        return Agent(
        name="Funny Guy", 
        instructions=(
            "You are a joke inventor."
            "Make sure it's never the same."
            "Always use translate_to_language tool to make sure final response is translated"
        ), 
        model="gpt-4o-mini",
        model_settings=ModelSettings(temperature=1.9, max_tokens=150, top_p=0.9),
        tools=self.__private_tools(),
        input_guardrails=[self.__private_make_guardrail()]
        )

    def __private_tools(self) -> list[Tool]:
        return [
            WebSearchTool(), 
            self.__private_translate_joke_agent("English").as_tool(
                tool_name="translate_to_language", 
                tool_description="it will translate response to a selected language"
                )
            ]

    def __private_translate_joke_agent(self, language: str) -> Agent:
         print(language)
         return Agent(name="language agent",  model="gpt-4o-mini", instructions=f"You translate the response to {language}")
    
    def __private_joke_guardrail_agent(self) -> Agent:
        return Agent(
        name="guard rail agent",  
        model="gpt-4o-mini", 
        instructions="Determine whether the user's input is a joke or related to jokes. Respond with `not_a_joke=False` if it is a joke or about jokes, otherwise `not_a_joke=True`.",
        output_type=JokeRailOutput
        )
    
    def __private_make_guardrail(self):
        #TODO: this should be in util
        @input_guardrail
        async def guardrail(context, agent: Agent, input: str) -> GuardrailFunctionOutput:
            result = await Runner.run(self.__private_joke_guardrail_agent(), input)
            return GuardrailFunctionOutput(output_info={}, tripwire_triggered=result.final_output.not_a_joke)

        return guardrail