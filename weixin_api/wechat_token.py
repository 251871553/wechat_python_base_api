import requests


appId = "wxf511ea0110065830"
appSecret = "8ec03c9201477f9a4236a3b1414e5f58"

token_url = ('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (appId, appSecret))
r = requests.get(token_url).json()
print(r['access_token'])

print(r)
