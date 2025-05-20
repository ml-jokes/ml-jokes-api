from pydantic import BaseModel


class JokeRailOutput(BaseModel):
    not_a_joke: bool