from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .models import SolveRequest,SolveResponse
from .orchestrator import solve
load_dotenv(); app=FastAPI(title='Trinity Core API',version='0.1.0')
app.add_middleware(CORSMiddleware,allow_origins=['*'],allow_methods=['*'],allow_headers=['*'])
@app.get('/health')
def health(): return {'ok':True,'service':'trinity-core'}
@app.post('/solve',response_model=SolveResponse)
async def solve_route(req:SolveRequest):
    final,candidates,audit=await solve(req.prompt,req.mode); return SolveResponse(final=final,candidates=candidates,audit=audit)
