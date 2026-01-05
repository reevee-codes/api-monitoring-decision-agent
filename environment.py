import random

import httpx

def check_api():
    list = ["https://httpbin.org/status/200", "https://httpbin.org/status/500",
    "https://httpbin.org/delay/2"]
    response = httpx.get(random.choice(list), timeout=5)
    if response.status_code == 200:
        return "OK"
    elif response.status_code == 500:
        return "ERROR"
    else:
        return "TIMEOUT"