import os
from .base import post_json
async def ask(prompt:str)->str:
    key=os.getenv('OPENAI_API_KEY','')
    if not key: raise RuntimeError('OPENAI_API_KEY missing')
    model=os.getenv('OPENAI_MODEL','gpt-5.6')
    data=await post_json('https://api.openai.com/v1/responses',{'Authorization':f'Bearer {key}','Content-Type':'application/json'},{'model':model,'input':prompt})
    if data.get('output_text'): return data['output_text']
    parts=[]
    for item in data.get('output',[]):
        for c in item.get('content',[]):
            if c.get('type')=='output_text': parts.append(c.get('text',''))
    return '\n'.join(parts).strip()
