import urllib2, httplib
import base64
import json
import struct
username = 'phanthao'
apiKey = 'da1fcf2b-2e15-42c4-ad20-3f7d59ffde3a'
base64EncodeBasicAuth = 'Basic ' + base64.b64encode(username + ":" + apiKey)

filename = "appdemo.apk"
filePath = "/Users/thaotphan/Downloads/appdemo.apk"

def generateUrl():
    header = {
        "Authorization": base64EncodeBasicAuth,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    body = json.dumps({
        "filename": filename
    })
    url = "https://api.kobiton.com/v1/apps/uploadUrl"
    request = urllib2.Request(url,body,header)
    response = urllib2.urlopen(request)
    data = json.loads(response.read())
    return data.get("url"), data.get("appPath")

def uploadToS3(presignedUrl):
    header = {
        'Content-Type': 'application/octet-stream',
        'x-amz-tagging': 'unsaved=true'
    }
    body =  base64.b64encode(open(filePath,"rb").read())
    request = urllib2.Request(presignedUrl, headers=header, data=body)
    request.get_method = lambda: str('PUT')
    response = urllib2.urlopen(request)
    print response.code

def  createApp(appPath):
    header = {
        "Authorization": base64EncodeBasicAuth,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    body = json.dumps({
        "filename": filename,
        "appPath": appPath
    })
    url = "https://api.kobiton.com/v1/apps"
    request = urllib2.Request(url,body,header)
    response = urllib2.urlopen(request)
    data = json.loads(response.read())
    if data.get("appId"):
        return data.get("appId")
    else:
        return None

try:
    urlAppPath = generateUrl()
    uploadToS3(urlAppPath[0])
    appId = createApp(urlAppPath[1])
    if appId is not None:
        print "Your app is uploaded successfully. Your appID is", appId
    else:
        raise Exception("No AppID")
except Exception as ex:
    print ex
    print "Your app has not been uploaded. Please try again or upload manually on https://portal.kobiton.com/apps"
