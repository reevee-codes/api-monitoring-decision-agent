import random
import httpx

async def check_api():
    urls = [
        "https://httpbin.org/status/200",
        "https://httpbin.org/status/500",
        "https://httpbin.org/delay/2",
    ]
    try:
        async with httpx.AsyncClient(timeout=2) as client:
            response = await client.get(random.choice(urls))

        if response.status_code == 200:
            return "OK"
        return "ERROR"

    except httpx.RequestError:
        return "TIMEOUT"