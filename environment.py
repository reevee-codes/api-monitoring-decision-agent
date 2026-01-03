import httpx

def check_api():
    response = httpx.get("https://httpbin.org/status/200")
    if response.status_code == 200:
        return "OK"
    elif response.status_code == 500:
        return "ERROR"
    else:
        return "TIMEOUT"