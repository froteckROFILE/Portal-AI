import asyncio,hashlib
from .models import Candidate
from .providers import openai_provider,anthropic_provider,xai_provider
PROVIDERS={'GPT':openai_provider.ask,'CLAUDE':anthropic_provider.ask,'GROK':xai_provider.ask}
async def safe_call(name,fn,prompt):
    try: return Candidate(provider=name,answer=(await fn(prompt)) or '(empty response)')
    except Exception as e: return Candidate(provider=name,answer='',ok=False,error=str(e))
async def parallel(prompt): return await asyncio.gather(*(safe_call(n,f,prompt) for n,f in PROVIDERS.items()))
def anonymous_packet(candidates):
    good=[c for c in candidates if c.ok]; labels='ABC'; return '\n\n'.join(f'SOLUTION {labels[i]}:\n{c.answer}' for i,c in enumerate(good[:3]))
async def arena(original_prompt,candidates):
    good=[c for c in candidates if c.ok]
    if not good:return 'No provider returned a usable answer.',{'status':'failed','usable_models':0}
    packet=anonymous_packet(good)
    rp=f'''You are a rigorous reviewer. Original task:\n{original_prompt}\n\nAnonymous candidate solutions:\n{packet}\n\nIdentify concrete errors, unsupported assumptions, conflicts, missing constraints, and strongest components. Do not vote by majority.'''
    reviews=await asyncio.gather(*(safe_call(n,f,rp) for n,f in PROVIDERS.items()))
    review_text='\n\n'.join(f'REVIEW {i+1}:\n{r.answer}' for i,r in enumerate(reviews) if r.ok)
    sp=f'''Produce ONE final product. Resolve disagreements using evidence and deterministic checks where possible. Mark unresolved uncertainty.\nORIGINAL:\n{original_prompt}\nCANDIDATES:\n{packet}\nREVIEWS:\n{review_text}'''
    finals=await asyncio.gather(*(safe_call(n,f,sp) for n,f in PROVIDERS.items())); usable=[x for x in finals if x.ok and x.answer]
    if not usable:return max(good,key=lambda x:len(x.answer)).answer,{'status':'degraded','usable_models':len(good)}
    drafts='\n\n'.join(f'FINAL DRAFT {i+1}:\n{x.answer}' for i,x in enumerate(usable)); cp=f'''Original task:\n{original_prompt}\nMerge these final drafts into one precise supported answer. Do not use majority vote.\n{drafts}'''
    for name,fn in PROVIDERS.items():
        c=await safe_call(name,fn,cp)
        if c.ok and c.answer:return c.answer,{'status':'ok','usable_models':len(good),'canonicalizer':name}
    return usable[0].answer,{'status':'degraded','usable_models':len(good)}
async def solve(prompt,mode):
    candidates=await parallel(prompt)
    if mode=='parallel':
        good=[c for c in candidates if c.ok]; return '\n\n'.join(f'{c.provider}:\n{c.answer}' for c in good),candidates,{'status':'parallel','usable_models':len(good),'prompt_hash':hashlib.sha256(prompt.encode()).hexdigest()[:16]}
    final,audit=await arena(prompt,candidates); audit['prompt_hash']=hashlib.sha256(prompt.encode()).hexdigest()[:16]; return final,candidates,audit
