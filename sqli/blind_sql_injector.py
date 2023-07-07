"""
This blind SQL Injection attack tool was created by simya. 
This tool uses bit operations to perform the attack. 2023-07-03.
"""
import sys
from get_attack_payloads import blind_sql_injection_attack as get
from post_attack_payloads import blind_sql_injection_attack as post


method = input("Does the attack target use the POST or GET method? ")

if method.upper() == "GET":
    get()
elif method.upper() == "POST":
    post()
else:
    print("Quit.")
    print( sys.exit(0))
