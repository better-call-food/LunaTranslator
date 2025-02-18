import requests
import base64

from myutils.config import globalconfig 
from ocrengines.baseocrclass import baseocr 
class OCR(baseocr):
    def langmap(self):
        return {"zh":"CHN_ENG","en":"ENG","ja":"JAP","en":"ENG","ko":"KOR","fr":"FRE","es":"SPA"}
    def initocr(self):
        self.appid,self.secretKey,self.accstoken=None,None,None
        self.checkchange()
    def checkchange(self): 
        self.checkempty(['API Key','Secret Key'])
        if (self.config['API Key'],self.config['Secret Key'] )!=(self.appid,self.secretKey)  :
            self.appid,self.secretKey=self.config['API Key'],self.config['Secret Key']
            self.accstoken=requests.get('https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+self.appid+'&client_secret='+self.secretKey, proxies=self.proxy).json()['access_token']
    def ocr(self,imgfile):
        self.checkchange()
        if self.accstoken=="":
            return ''
        headers = {
            'authority': 'aip.baidubce.com',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cache-control': 'no-cache',
            'origin': 'chrome-extension://hmpjibmn1ncjokocepchnea',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Microsoft Edge";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'none',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53',
        }

        params = {
            'access_token':self.accstoken# '',
        }
        with open(imgfile,'rb') as ff:
            f=ff.read()
        b64=base64.b64encode(f)

        data = {
            'image': b64 , 
            'detect_direction':globalconfig['verticalocr'],
            'language_type':self.srclang 
        } 
        interfacetype=self.config['接口']
         
        url=[
            'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic',
            'https://aip.baidubce.com/rest/2.0/ocr/v1/general',
            'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic',
            'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate'
        ][interfacetype]
        response = requests.post(url, params=params, headers=headers, data=data, proxies=self.proxy)
        try: 
            
            self.countnum()
             
            if globalconfig['verticalocr'] and (interfacetype in [1,3]):
                _collect=[(x['words'],x['location']['left'])  for x in response.json()['words_result']] 
                _collect.sort(key=lambda x:-x[1])
                return  self.space.join([_[0]  for _ in _collect])
            else:
                return  self.space.join([x['words']  for x in response.json()['words_result']])
        except:
            raise Exception(response.text)