import urllib2,httplib
import base64
import json
username = 'phanthao'
apiKey = 'da1fcf2b-2e15-42c4-ad20-3f7d59ffde3a'
filename = "appdemo.apk"
filePath = "/Users/thaotphan/Downloads/appdemo.apk"
def create_upload_url():
    url = 'https://api.kobiton.com/v1/apps/uploadUrl'
    header = {
        "Content-Type": "application/json",
        "Authorization": 'Basic ' + base64.b64encode(username + ":" + apiKey)
    }
    body = {
        "filename": filename
    }
    request = urllib2.Request(url, headers=header, data=json.dumps(body))
    response = urllib2.urlopen(request)
    body = response.read()
    return json.loads(body)


def convert_file_to_byte():
    with open(filePath, "rb") as apkFile:
        return base64.b64encode(apkFile.read())


def upload_s3():
    header = {
        "Content-Type": "application/octet-stream",
    }
    body = convert_file_to_byte()
    url = create_upload_url()['url']
    print url
    request = urllib2.Request(url, headers=header, data=str(body))
    request.get_method = lambda: 'PUT'
    response = urllib2.urlopen(request)
    print response.status

upload_s3()
# def  createApp(appPath):
#     header = {
#         "Authorization": 'Basic ' + base64.b64encode(username + ":" + apiKey),
#         "Accept": "application/json",
#         "Content-Type": "application/json"
#     }
#     body = json.dumps({
#         "filename": filename,
#         "appPath": appPath
#     })
#     conn = httplib.HTTPSConnection("api.kobiton.com")
#     conn.request("POST","/v1/apps",body,header)
#     response = conn.getresponse()
#     data = json.loads(response.read())
#     if data.get("appId"):
#         return data.get("appId")
#     else:
#         return None
#
# try:
#     urlAppPath = create_upload_url()
#     upload_s3
#     appId = createApp(urlAppPath[1])
#     if appId is not None:
#         print "Your app is uploaded successfully. Your appID is", appId
#     else:
#         raise Exception("No AppID")
# except Exception as ex:
#     print ex
#     print "Your app has not been uploaded. Please try again or upload manually on https://portal.kobiton.com/apps"
