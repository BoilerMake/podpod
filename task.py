import sys
import configparser
import requests
import threading
import argparse
import json
from time import sleep

config = configparser.ConfigParser()
config.read('config.ini')

API = config.get('config', 'BASE_API')
KEY = config.get('config', 'PODPOD_KEY')
ID = config.get('config', 'POD_ID')

parser = argparse.ArgumentParser(description='PodPod Communication software for BoilerMake Backend')
parser.add_argument('--stdin', help='Use stdin instead of /dev/hidraw0', action="store_true")
parser.add_argument('--no-gpio', help='Does not use GPIO if specified', action="store_true")
parser.add_argument('--no-heartbeat', help='Disables heartbeat connection with server', action="store_true")
args = parser.parse_args()

payload = {'pod_key': KEY, 'pod_id': ID}
r = requests.post(API + '/pods/heartbeat', data=payload)
parsed_json = json.loads(r.text)
if parsed_json['success'] != True:
  print('COULD NOT START PODPOD: ' + parsed_json['message'])
  print('exiting...')
  sys.exit(0)

file = open("log", "a+")

hid = { 4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm', 17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y', 29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 44: ' ', 45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';' , 52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'  }

hid2 = { 4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M', 17: 'N', 18: 'O', 19: 'P', 20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U', 25: 'V', 26: 'W', 27: 'X', 28: 'Y', 29: 'Z', 30: '!', 31: '@', 32: '#', 33: '$', 34: '%', 35: '^', 36: '&', 37: '*', 38: '(', 39: ')', 44: ' ', 45: '_', 46: '+', 47: '{', 48: '}', 49: '|', 51: ':' , 52: '"', 53: '~', 54: '<', 55: '>', 56: '?'  }

#TODO: Allow this thread to stop execution on API response
if not args.no_heartbeat:
  def heartbeatThread():
      while True:
        payload = {'pod_key': KEY, 'pod_id': ID}
        r = requests.post(API + '/pods/heartbeat', data=payload)
        print(r.text)
        sleep(120)
      pass
  
  t1 = threading.Thread(target=heartbeatThread, args=[])
  t1.setDaemon(True)
  t1.start()

print("Scanning for barcodes", end=" ")
if args.stdin:
   print("using stdin")
   for line in sys.stdin:
     payload = {'pod_key': KEY, 'pod_id': ID, 'code': line.rstrip('\n')}
     r = requests.post(API + '/pods/scan', data=payload)
     file.write(str(payload) + "\n")
     file.write(r.text + "\n")
     print(r.text)
else:
   print("using /dev/hidraw0")
   ss = ""
   shift = False
   done = False

   fp = open('/dev/hidraw0', 'rb')

   while True:
     while not done:
        print 
        ## Get the character from the HID
        buffer = fp.read(8)
        for c in buffer:
           if c > 0:
              ##  40 is carriage return which signifies
              ##  we are done looking for characters
              if c == 40:
                 done = True
                 break;
     
              ##  If we are shifted then we have to 
              ##  use the hid2 characters.
              if shift: 
                 ## If it is a '2' then it is the shift key
                 if c == 2 :
                    shift = True
     
                 ## if not a 2 then lookup the mapping
                 else:
                    ss += hid2[c]
                    shift = False
     
              ##  If we are not shifted then use
              ##  the hid characters
              else:
                 ## If it is a '2' then it is the shift key
                 if c == 2 :
                    shift = True
                 ## if not a 2 then lookup the mapping
                 else:
                    ss += hid[c]

     payload = {'pod_key': KEY, 'pod_id': ID, 'code': ss}
     r = requests.post(API + '/pods/scan', data=payload)
     print(r.text)
     print(ss)
     ss = ""
     done = False
file.close()