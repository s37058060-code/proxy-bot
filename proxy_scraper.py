import requests

def get_indian_proxies():
    proxies = set()

    # Source 1 (Indian)
    try:
        url1 = "https://api.proxyscrape.com/v2/?request=getproxies&country=IN&protocol=http&timeout=10000"
        res1 = requests.get(url1).text.split("\n")
        proxies.update(res1)
    except:
        pass

    # Source 2 (Global)
    try:
        url2 = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
        res2 = requests.get(url2).text.split("\n")
        proxies.update(res2)
    except:
        pass

    return [p.strip() for p in proxies if p.strip()]
