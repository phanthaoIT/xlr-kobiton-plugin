import base64
import json
import urllib2

username = 'blackheat'
api_key = '8d978d7d-0ac9-4be6-84e2-e69c1485eb2b'

# Return list in XebiaLabs
devices = []


def create_basic_authentication_token():
    s = username + ":" + api_key
    return "Basic " + s.encode("base64").rstrip()


def create_upload_url():
    auth_token = create_basic_authentication_token()
    url = 'https://api.kobiton.com/v1/apps/uploadUrl'
    header = {
        "Content-Type": "application/json",
        "Authorization": auth_token
    }
    body = {
        "filename": "appdemo.apk"
    }
    request = urllib2.Request(url, headers=header, data=json.dumps(body))
    response = urllib2.urlopen(request)
    body = response.read()
    return json.loads(body)


def convert_file_to_byte():
    with open("appdemo.apk", "rb") as apkFile:
        return base64.b64encode(apkFile.read())


def upload_s3():
    header = {
        "Content-Type": "application/octet-stream",
    }
    body = convert_file_to_byte()
    upload_url = create_upload_url()
    print upload_url
    url = upload_url['url']
    print url
    request = urllib2.Request(url, headers=header, data=str(body))
    request.get_method = lambda: 'PUT'
    response = urllib2.urlopen(request)
    print response.code
    #createApp("demo.apk", upload_url['appPath'])


def  createApp(file_name, app_path):
    apps_url = 'https://api.kobiton.com/v1/apps'
    header = {
        "Authorization": create_basic_authentication_token(),
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    body = {
        "appPath": app_path
    }

    request = urllib2.Request(url=apps_url, headers=header, data=str(json.dumps(body)))
    response = urllib2.urlopen(request)

    data = json.loads(response.read())
    if data['appId']:
        print data['appId']
    else:
        print 'failed'


upload_s3()