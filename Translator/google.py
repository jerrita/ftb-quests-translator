import requests

class Translator:
    def __init__(self):
        pass

    def translate(self, query, src='auto', dst='zh'):
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            'client': 'gtx',
            'sl': src,
            'tl': dst,
            'dt': 't',
            'dj': 1,
            'q': query
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()["sentences"][0]["trans"]
