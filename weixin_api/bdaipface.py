from aip import AipFace
import base64
 
APP_ID = '9837784'
API_KEY = 'DWMYBEzB0ksAWtp1aeneOhlc'
SECRET_KEY = 'IBGC9RNlpsq2Yg8vWAuAjxt2Wzc9Dibb'


#image = 'https://ss0.bdstatic.com/94oJfD_bAAcT8t7mm9GUKT-xh_/timg?image&quality=100&size=b4000_4000&sec=1554632855&di=9998bb5c8131864dbc4ce568ae923a80&src=http://image.biaobaiju.com/uploads/20180803/20/1533300389-KFRyeJpPvX.jpg'
def identify_face(image):
    client = AipFace(APP_ID, API_KEY, SECRET_KEY)
    #image = "取决于image_type参数，传入BASE64字符串或URL字符串或FACE_TOKEN字符串"
    #imageType = "URL"
    imageType = "BASE64"
    """ 调用人脸检测 """
    """ 如果有可选参数 """
    options = {}
    options["face_field"] = "age,beauty,expression,faceshape,gender,glasses,race,facetype"
    options["max_face_num"] = 2
    options["face_type"] = "LIVE"
    """ 带参数调用人脸检测 """
    face_res=client.detect(image, imageType, options)
    #print(face_res)
    if face_res['error_code']==0:
       face_info=face_res['result']['face_list']
       #for face in face_info:
          #reply_face=[]
         # age=face['age']
         # race=face['race']['type']
         # faceshape=face['face_shape']['type']
         # gender=face['gender']['type']
         # beauty=face['beauty']
         # expression=face['expression']['type']
         # face_type=face['face_type']['type']
      # print(face_info)
       return face_info

    else:
       print(face_res['error_msg'])
       return 0000

#with open("20190614152105_006.jpg", 'rb') as f:
#    base64_data = base64.b64encode(f.read())
#    s = base64_data.decode()
#    print(s)
#identify_face('20190614152105_006.jpg')
#identify_face(s)
if __name__ != "__main__":
     pass
