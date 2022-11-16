import requests
import hashlib

def Translate(content):
    try:
        #     if(content=='最喜欢哥哥了'):
        #         return 'お兄ちゃん大好き'
        url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        headers={
                "Referer": "https://fanyi.youdao.com/",
                "Cookie": 'OUTFOX_SEARCH_USER_ID_NCOO=2117581713.9679494; OUTFOX_SEARCH_USER_ID="-1072317107@10.108.162.135"; _ga=GA1.2.1860116172.1661188928; UM_distinctid=18307542edd679-09f730b7cb115e-26021c51-1fa400-18307542ede1097; ___rl__test__cookies=1668598080306',
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
                }
        # data = {}
        salt='16685958257638'
        sign_str = 'fanyideskweb' + content + salt + 'Ygy_4c=r#e#4EX^NUGUc5'
        m=hashlib.md5()
        m.update(sign_str.encode())
        sign = m.hexdigest()
        data={
            'i':content,
            'from':'zh_CHS',
            'to':'ja',
            'smartresult':'dict',
            'client':'fanyideskweb',
            'salt':salt,
            'sign':sign,
            'Its':'1668595825763',
            'bv':'9edd1e630b7d8f13679a536d504f3d9f',
            'doctype':'json',
            'version':'2.1',
            'keyfrom':'fanyi.web',
            'action':'FY_BY_CLICKBUTTION',
            }
        response = requests.post(url,headers=headers,data=data)
        dictTrans = response.json()
        if(dictTrans['type'][:2]=='ja'):
            return content
        return dictTrans['translateResult'][0][0]['tgt']
    except:
        return content

if __name__=='__main__':
    # print(Translate('お兄ちゃん大好き,私は高性能のロボット'))
    # print(Translate('最喜欢哥哥了'))
    print(Translate('我是高性能机器人'))