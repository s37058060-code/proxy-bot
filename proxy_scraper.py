import requests

def get_indian_proxies():
    url = "https://api.proxyscrape.com/v2/?request=getproxies&country=IN&protocol=http&timeout=10000"
    
    res = requests.get(url)
    proxies = res.text.split("\n")
    
    return [p.strip() for p in proxies if p.strip()]
