import urllib
import urllib2
import time
import json


appId = "wxf511ea0110065830"
appSecret = "324a7f6f0df56ed870d9050691106854"

postUrl = ('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (appId, appSecret))
urlResp = urllib.urlopen(postUrl)
urlResp = json.loads(urlResp.read())
#urlResp = urlResp.read()
print  urlResp
print  urlResp['access_token']
print  urlResp['expires_in']

accessToken = urlResp['access_token']
mediaType = 'image'
filePath='4-15012G52133.jpg'
fileName = ""

#def uplaod(accessToken, filePath, mediaType):
def uplaod():
        openFile = open(filePath, "rb")
    #    param = {'media': openFile, 'filename': fileName}
        param = {'media': openFile}
       # postHeaders = poster.encode.multipart_encode(param)
        postData = urllib.urlencode(param)

        postUrl = 'https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s' % (accessToken, mediaType)
       # request = urllib2.Request(postUrl, postData, postHeaders)
        request = urllib2.Request(postUrl, postData)
        urlResp = urllib2.urlopen(request)
        print urlResp.read()

uplaod()
