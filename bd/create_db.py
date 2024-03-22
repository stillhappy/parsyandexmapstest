import psycopg2
import json

def create_categories(database, user, password, host, port=None):
    conn = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host
    )
    categories = set()
    with open('out.json', 'r', encoding='utf-8') as jsf:
        data = json.load(jsf)
        for cat in data['data']['categoryIcons']['items']:
            categories.add(cat['displayText'])
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f'''
            CREATE TABLE IF NOT EXISTS categories(
                category_id serial,
                category_name text
            );
        ''')
    for category in categories:
        cur.execute(f"SELECT category_name FROM categories WHERE category_name = '{category}'")
        if cur.rowcount == 0:
            cur.execute(f"INSERT INTO categories (category_name) VALUES ('{category}')")
        else:
            continue
    cur.close()
    conn.close()


def create_cities(database, user, password, host, port=None):
    conn = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host
    )
    cities = ['Москва', 'Видное', 'Воронеж', 'Уфа', 'Тула', 'Нижний Новгород', 'Дзержинский']
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f'''
                CREATE TABLE IF NOT EXISTS cities(
                    city_id serial,
                    city_name text
                );
            ''')
    for city in cities:
        cur.execute(f"SELECT city_name FROM cities WHERE city_name = '{city}'")
        if cur.rowcount == 0:
            cur.execute(f"INSERT INTO cities (city_name) VALUES ('{city}')")
        else:
            continue
    cur.close()
    conn.close()

def create_data(database, user, password, host, port=None):
    conn = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host
    )
    conn.autocommit = True
    cur = conn.cursor()
    # Дата, Баз, оп, Город, Сфера, Название, площадка, тип_клиента, ссылка на карточку, кол-во отзывов, рейтинг, ссылка на сайт, Телефон, Результат, дата звонка, email, оплата1, оплата2
    cur.execute(f'''
                    CREATE TABLE IF NOT EXISTS data_pars(
                        id serial,
                        date_request timestamp,
                        bar text,
                        operator text,
                        city int,
                        category int, 
                        name_org text,
                        parser_name,
                        role varchar(25),
                        url_res text,
                        count_reviews int,
                        rating float,
                        url_site text,
                        phone text,
                        result text,
                        date_phone timestamp,
                        email varchar(25),
                        Payment1 varchar(25),
                        Payment2 varchar(25)
                    );
                ''')
    cur.close()
    conn.close()