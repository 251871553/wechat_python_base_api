import urllib
import json
import sys

text='apple'

API_key='1085948580'
keyfrom='weixinapi2017'

postUrl = 'http://fanyi.youdao.com/openapi.do?keyfrom=%s&key=%s&type=data&doctype=xml&version=1.1&q=%s' % (keyfrom,API_key,text)

print  postUrl
#sys.exit()
urlResp = urllib.urlopen(postUrl)
#urlResp = json.loads(urlResp.read())
urlResp = urlResp.read()
print  urlResp
print  type(urlResp)
#print  urlResp['access_token']
#print  urlResp['expires_in']

