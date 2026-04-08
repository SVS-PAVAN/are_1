from pydantic import BaseModel
from typing import List, Optional


class AreAction(BaseModel):
    tool_name: str
    tool_input: str


class AreObservation(BaseModel):
    task: str
    history: List[str]
    last_tool_output: Optional[str] = None
    reflection: Optional[str] = None
    done: bool = False