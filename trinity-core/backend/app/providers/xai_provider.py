import os
from .base import post_json
async def ask(prompt:str)->str:
    key=os.getenv('XAI_API_KEY','')
    if not key: raise RuntimeError('XAI_API_KEY missing')
    model=os.getenv('XAI_MODEL','grok-4')
    data=await post_json('https://api.x.ai/v1/chat/completions',{'Authorization':f'Bearer {key}','Content-Type':'application/json'},{'model':model,'messages':[{'role':'user','content':prompt}],'temperature':0.2})
    return data['choices'][0]['message']['content'].strip()
