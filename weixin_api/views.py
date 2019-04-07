from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.http import HttpResponse
import  hashlib
from django.views.decorators.csrf import csrf_exempt
#from django.utils.encoding import smart_str #我们在需要将用户提交的数据转换为 Unicode 的时候可以使用 smart_unicode，而在需要将程序中字符输出到非 Unicode 环境（比如 HTTP 协议数据）时
from lxml import etree
#import  json
import  time
from django.template import loader
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from .bdaipface import *
import requests


API_key='1085948580'
keyfrom='weixinapi2017'


@csrf_exempt
def index(request):
    if request.method == "GET":
        signature = request.GET.get("signature", None)
        timestamp = request.GET.get("timestamp", None)
        nonce = request.GET.get("nonce", None)
        echostr = request.GET.get("echostr", None)
        token = "weiping"
        list_wx = [token, timestamp, nonce]
        list_wx.sort()
        hashcode = "%s%s%s" % tuple(list_wx)
        hashcode=hashcode.encode('utf8')
        hashcode = hashlib.sha1(hashcode).hexdigest()
        if hashcode == signature:
           return HttpResponse(echostr)
        else:
           return HttpResponse('success')
    else:       #request.method == "POST"
        #return HttpResponse("Hello, world. You're at the polls index.")
        xml_str = request.body   #xml字符串
        print(xml_str)
        print('xxxxxxxxxxxxxxxxxxxxx')
        request_xml = etree.fromstring(xml_str)     #转化成xml
        toUser = request_xml.find('ToUserName').text
        fromUser = request_xml.find('FromUserName').text
        CreateTime = request_xml.find('CreateTime').text
        MsgType = request_xml.find('MsgType').text
        time_wx=int(time.time())       #打时间戳
        default_msg='感谢您的关注！\n回复【帮助】两个字查看支持的功能，还可以回复任意内容开始聊天【<a href="http://www.baidu.com">我们的主页</a>】'
        if MsgType == 'text':     #文字消息
           content = request_xml.find('Content').text
           MsgId = request_xml.find('MsgId').text
           if content=='帮助':
              help_msg='目前处于开发阶段，待后续上线'
              haha=''' 
              <xml>
              <ToUserName><![CDATA[%s]]></ToUserName>
              <FromUserName><![CDATA[%s]]></FromUserName>
              <CreateTime>%d</CreateTime>
              <MsgType><![CDATA[text]]></MsgType>
              <Content><![CDATA[%s]]></Content>
              </xml>
              '''  % (fromUser,toUser,time_wx,default_msg)
              return HttpResponse(haha)
           else:
              youdao_api_url='http://fanyi.youdao.com/openapi.do?keyfrom=%s&key=%s&type=data&doctype=json&version=1.1&q=%s' % (keyfrom,API_key,content)
              res = requests.get(youdao_api_url).json()
              errorCode=res['errorCode']
              print(res)
              if errorCode==0:
                 result_text=res['translation'][0]
              else:
                 result_text='错误的输入,请重新输入'
              haha=''' 
              <xml>
              <ToUserName><![CDATA[%s]]></ToUserName>
              <FromUserName><![CDATA[%s]]></FromUserName>
              <CreateTime>%d</CreateTime>
              <MsgType><![CDATA[text]]></MsgType>
              <Content><![CDATA[%s]]></Content>
              </xml>
              '''  % (fromUser,toUser,time_wx,result_text)
              return HttpResponse(haha)
        elif MsgType == 'image':    #图片消息
              PicUrl=request_xml.find('PicUrl').text
              #PicUrl='https://ss0.bdstatic.com/94oJfD_bAAcT8t7mm9GUKT-xh_/timg?image&quality=100&size=b4000_4000&sec=1554632855&di=9998bb5c8131864dbc4ce568ae923a80&src=http://image.biaobaiju.com/uploads/20180803/20/1533300389-KFRyeJpPvX.jpg'
              MsgId = request_xml.find('MsgId').text
              MediaId=request_xml.find('MediaId').text
              print(PicUrl)
              bd_face=identify_face(PicUrl)
              if bd_face == 0000:
                 print('error')
              else:
                 for x in bd_face:
                    print(x)
             # try:
            #     MediaId=request_xml.find('MediaId').text
           #   except AttributeError as e:                 #腾讯接口调试会没有mediaid,所有有个异常处理，实际不需要
          #       print(e)
         #        MediaId='1'
              haha=''' 
              <xml>
              <ToUserName><![CDATA[%s]]></ToUserName>
              <FromUserName><![CDATA[%s]]></FromUserName>
              <CreateTime>%d</CreateTime>
              <MsgType><![CDATA[image]]></MsgType>
              <Image><MediaId><![CDATA[%s]]></MediaId></Image>
              </xml>
              '''  % (fromUser,toUser,time_wx,MediaId)
              return HttpResponse(haha)
        
        elif MsgType == 'voice':            #语音消息
            #  print xml_str
              MediaId=request_xml.find('MediaId').text
              haha=''' 
              <xml>
              <ToUserName><![CDATA[%s]]></ToUserName>
              <FromUserName><![CDATA[%s]]></FromUserName>
              <CreateTime>%d</CreateTime>
              <MsgType><![CDATA[voice]]></MsgType>
              <Voice><MediaId><![CDATA[%s]]></MediaId></Voice>
              </xml>
              '''  % (fromUser,toUser,time_wx,MediaId)
              return HttpResponse(haha)
        elif MsgType == 'video':      #视频消息
              MediaId=request_xml.find('MediaId').text
              ThumbMediaId=request_xml.find('ThumbMediaId').text
              haha='''
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%d</CreateTime>
                <MsgType><![CDATA[video]]></MsgType>
                <Video>
                   <MediaId><![CDATA[%s]]></MediaId>
                   <Title><![CDATA[title]]></Title>
                   <Description><![CDATA[description]]></Description>
                </Video> 
                </xml>
                '''  % (fromUser,toUser,time_wx,MediaId)
              return HttpResponse(haha)
        elif MsgType == 'music':      #音乐消息
              ThumbMediaId=request_xml.find('ThumbMediaId').text
              haha='''
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%d</CreateTime>
                <MsgType><![CDATA[music]]></MsgType>
                <Music><ThumbMediaId><![CDATA[%s]]></ThumbMediaId></Music>
                </xml>
                '''  % (fromUser,toUser,time_wx,ThumbMediaId)
#可选
#<Title><![CDATA[TITLE]]></Title><Description><![CDATA[DESCRIPTION]]></Description><MusicUrl><![CDATA[MUSIC_Url]]></MusicUrl><HQMusicUrl><![CDATA[HQ_MUSIC_Url]]></HQMusicUrl>

              return HttpResponse('haha')
        elif MsgType == 'news':        #图文消息
              haha='''
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%d</CreateTime>
                <MsgType><![CDATA[news]]></MsgType>
                <ArticleCount>1</ArticleCount>
                <Articles>
                <item>
                <Url><![CDATA[http://news.cnhubei.com/xw/yl/201701/t3774582.shtml]]></Url>
                </item>
                </Articles>
                </xml>
                '''  % (fromUser,toUser,time_wx)
                #可选<Title><![CDATA[title]]></Title>,<Description><![CDATA[description]]></Description>,<PicUrl><![CDATA[picurl]]></PicUrl><Url><![CDATA[url]]></Url>
              
              return HttpResponse('haha')
        elif MsgType == 'shortvideo':    #小视频消息
              return HttpResponse('success')
        elif MsgType == 'location':     #地理位置消息
              Location_X=request_xml.find('Location_X').text    #地理位置维度
              Location_Y=request_xml.find('Location_Y').text    #地理位置经度
              Scale=request_xml.find('Scale').text              #地图缩放大小
              Label=request_xml.find('Label').text              #地理位置信息
              return HttpResponse('success')
        elif MsgType == 'link':      #链接消息
              return HttpResponse('success')
        else:
   #           print MsgType
              return HttpResponse('不知道说的什么')
      #  template = loader.get_template('weixin_api/weixin_api.xml')
       # return HttpResponse(template.render())


