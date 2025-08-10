import requests
import hashlib
import json

from urllib import parse


class Translator:
    appid: str
    apikey: str

    salt = 'CQUPT3G'

    def get_sign(self, src: str):
        return hashlib.md5((self.appid + src + self.salt + self.apikey).encode('utf-8')).hexdigest()

    def translate(self, query, src='auto', dst='zh'):
        res = requests.post('https://fanyi-api.baidu.com/api/trans/vip/translate',
                            headers={
                                'Content-Type': 'application/x-www-form-urlencoded'
                            }, data=parse.urlencode({
                'q': query,
                'from': src,
                'to': dst,
                'appid': self.appid,
                'salt': self.salt,
                'sign': self.get_sign(query)
            }))
        return json.loads(res.text)['trans_result'][0]['dst']

    def __init__(self, appid, key):
        self.appid = appid
        self.apikey = key


if __name__ == '__main__':
    from priv import appid, apikey

    translator = Translator(appid, apikey)
    res = translator.translate('Hello world!')
    print(res)
