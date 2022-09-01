import requests

def Translate(content):
    try:
        if(content=='最喜欢哥哥了'):
            return 'お兄ちゃん大好き'
        url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
        data = {}

        data['i'] = content
        data['type'] = 'AUTO'
        data['smartresult'] = 'dict'
        data['client'] = 'fanyideskweb'
        data['salt'] = '16611770649142'
        data['sign'] = '4ed326d5b51b81dcdf3d60d4f2dbe9d5'
        data['doctype'] = 'json'
        data['version'] = '2.1'
        data['keyfrom'] = 'fanyi.web'
        data['action'] = 'FY_BY_REALTIME'
        data['Its']='1661177064914'
        data['bv']='50b61ff102560ebc7bb0148b22d7715c'

        response = requests.post(url,headers=headers,data=data)
        # print(data)
        dictTrans = response.json()
        # print(dictTrans)
        if(dictTrans['type'][:2]=='JA'):
            return content
        data['type'] = dictTrans['type'].split('2')[0]+'2JA'
        response = requests.post(url,headers=headers,data=data)
        dictTrans = response.json()
        return dictTrans['translateResult'][0][0]['tgt']
    except:
        return content

# if __name__=='__main__':
#     print(Translate('お兄ちゃん大好き'))