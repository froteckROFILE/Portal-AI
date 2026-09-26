import httpx
async def post_json(url,headers,payload,timeout=90):
    async with httpx.AsyncClient(timeout=timeout) as client:
        r=await client.post(url,headers=headers,json=payload); r.raise_for_status(); return r.json()
