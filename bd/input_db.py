import psycopg2

def inp_into_data_pars(data: list, database, user, password, host, port=None):
    conn = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host
    )
    conn.autocommit = True
    cur = conn.cursor()
    for item in data:
        cur.execute(f"SELECT name_org FROM data_pars WHERE name_org=")
    # Доделать
    cur.close()
    conn.close()