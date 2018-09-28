import Queue
import urllib2
import json
from threading import Thread

url = kobitonServer['remoteServer'] + '/verify'
results = {}

def main():
  if jobIds == {}:
    print 'No device in input.'
    return
  
  headers = {
    'Content-Type': 'application/json'
  }

  count = 0
  numOfKeys = len(jobIds.keys())
  while count < numOfKeys:
    for key, value in jobIds.iteritems():
      try:
        if results.has_key(key) == False:
          body = {
            key: value
          }
          request = urllib2.Request(url, json.dumps(body), headers=headers)
          response = urllib2.urlopen(request)
          data = response.read()
          if data == 'SUCCESS' or data == 'ERROR':
            results[key] = value + ' - ' + data
            count += 1
      except Exception as ex:
        print ex
        count += 1

main()