import os
from .base import post_json
async def ask(prompt:str)->str:
    key=os.getenv('ANTHROPIC_API_KEY','')
    if not key: raise RuntimeError('ANTHROPIC_API_KEY missing')
    model=os.getenv('ANTHROPIC_MODEL','claude-sonnet-4-5')
    data=await post_json('https://api.anthropic.com/v1/messages',{'x-api-key':key,'anthropic-version':'2023-06-01','content-type':'application/json'},{'model':model,'max_tokens':4000,'messages':[{'role':'user','content':prompt}]})
    return '\n'.join(x.get('text','') for x in data.get('content',[]) if x.get('type')=='text').strip()
