from pydantic import BaseModel, Field
from typing import Literal
class SolveRequest(BaseModel):
    prompt: str = Field(min_length=1,max_length=30000)
    mode: Literal['parallel','arena']='arena'
class Candidate(BaseModel):
    provider:str; answer:str; ok:bool=True; error:str|None=None
class SolveResponse(BaseModel):
    final:str; candidates:list[Candidate]; audit:dict
