import psycopg2
import configparser


def create_db(conn):
    # удаление таблиц
    cur.execute("""DROP TABLE phones; DROP TABLE clients;""")
    # создание таблиц
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY, first_name VARCHAR(30), 
        last_name VARCHAR(30), email VARCHAR(30) NOT NULL);
        """)
    conn.commit()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phones(
        id SERIAL PRIMARY KEY, phone VARCHAR(30) NOT NULL,
        client_id INTEGER NOT NULL REFERENCES clients(id));
        """)
    conn.commit()


# Добавление клиентов
def add_client(conn, first_name, last_name, email, phone=None):
    cur.execute("""
        INSERT INTO clients(first_name, last_name, email) 
        VALUES(%s, %s, %s) RETURNING id, first_name, last_name;
        """, (first_name, last_name, email))
    new_client = cur.fetchone()
    print(f'Добавлен клиент {new_client}')
    if phone is not None:
        cur.execute("""
            INSERT INTO phones(client_id, phone) VALUES(%s, %s);
            """, (new_client[0], phone))
        conn.commit()


# Добавление телефонных номеров
def add_phone(conn, client_id, phone):
    search_phone = check_phone(cur, client_id, phone)
    if search_phone is None or len(search_phone) == 0:
        print(f'Добавлен телефон {phone} для клиента {client_id}')
        cur.execute("""
            INSERT INTO phones(client_id, phone) VALUES(%s, %s);
            """, (client_id, phone))
        conn.commit()


# Проверка наличия телефонного номера
def check_phone(cur, client_id, phone):
    cur.execute("""
        SELECT phone FROM phones WHERE client_id=%s AND phone=%s;
        """, (client_id, phone))
    search_phone = cur.fetchone()
    return search_phone


# Изменение данных о клиенте
def change_client(conn, client_id, first_name=None, last_name=None, email=None, phone=None):
    if first_name is not None:
        cur.execute("""
            UPDATE clients SET first_name=%s WHERE id=%s
            """, (first_name, client_id))
        print(f'Имя у клиента {client_id} заменено на {first_name}')
    if last_name is not None:
        cur.execute("""
            UPDATE clients SET last_name=%s WHERE id=%s
            """, (last_name, client_id))
        print(f'Фамилия у клиента {client_id} заменена на {last_name}')
    if email is not None:
        cur.execute("""
            UPDATE clients SET email=%s WHERE id=%s
            """, (email, client_id))
        print(f'Адрес у клиента {client_id} заменен на {email}')
    if phone is not None:
        add_phone(conn, client_id, phone)
        print(f'Телефон {phone} добавлен клиенту {client_id}')
    conn.commit()


# Удаление номера телефона
def delete_phone(conn, client_id, phone):
    cur.execute("""
        DELETE FROM phones WHERE client_id=%s and phone=%s;
        """, (client_id, phone))
    conn.commit()
    print(f'Номер {phone} у клиента {client_id} удален')


# Удаление клиента из таблицы
def delete_client(conn, client_id):
    cur.execute("""
        DELETE FROM phones WHERE client_id=%s;
        """, (client_id,))
    cur.execute("""
        DELETE FROM clients WHERE id=%s;
        """, (client_id,))
    conn.commit()
    print(f'Клиент {client_id} удален')


# Поиск клиента по его данным: имени, фамилии, email или телефону
def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    if phone is not None:
        cur.execute("""
            SELECT clients.id FROM clients
            JOIN phones ON phones.client_id = clients.id
            WHERE phones.phone=%s;
            """, (phone,))
    else:
        cur.execute("""
            SELECT id FROM clients 
            WHERE first_name=%s OR last_name=%s OR email=%s;
            """, (first_name, last_name, email))
    conn.commit()
    print('Клиент', end=' ')
    print(*cur.fetchone())


# Получение пароля от PostgreSQL
def get_password(file_name):
    data = configparser.ConfigParser()
    data.read(file_name)
    password = data["password"]["password"]
    return password


if __name__ == '__main__':
    password = 'password.ini'  # Пароль от PostgreSQL нужно вставить в папку password.ini

    with psycopg2.connect(database="clients_db", user="postgres", password=get_password(password)) as conn:
        with conn.cursor() as cur:
            # создание таблиц, удаление таблиц
            create_db(conn)

            # Добавление клиентов
            add_client(conn, 'Vanya', 'Ivanov', 'Vanya@ya.ru', '83578123')
            add_client(conn, 'Igor', 'Petrov', 'Igor@ya.ru')
            add_client(conn, 'Sasha', 'Sidorov', 'Sasha@ya.ru', '85312873')

            # Добавление телефонных номеров
            add_phone(conn, 3, '81234567')
            add_phone(conn, 1, '82312352')
            add_phone(conn, 2, '83251751')

            # Изменение данных о клиенте
            change_client(conn, 1, 'Petya', None, None, '83125717')
            change_client(conn, 2, None, 'Vasechkin')
            change_client(conn, 3, None, None, 'Sidorov@ya.ru')
            change_client(conn, 2, None, None, None, '87328515')

            # Удаление номера телефона
            delete_phone(conn, 1, '83125717')
            delete_phone(conn, 1, '82312352')

            # Удаление клиента из таблицы
            delete_client(conn, 3)

            # Поиск клиента по его данным: имени, фамилии, email или телефону
            find_client(conn, 'Igor')
            find_client(conn, None, 'Ivanov')
            find_client(conn, None, None, 'Vanya@ya.ru')
            find_client(conn, None, None, None, '83578123')


# Первоначальный вариант
# with psycopg2.connect(database="clients_db", user="postgres", password=get_password(password)) as conn:
#     with conn.cursor() as cur:
        # cur.execute("""DROP TABLE phones; DROP TABLE clients;""")
        # conn.commit()
        #
        # cur.execute("""CREATE TABLE IF NOT EXISTS clients(id SERIAL PRIMARY KEY, first_name VARCHAR(30), last_name VARCHAR(30), email VARCHAR(30) UNIQUE);""")
        # conn.commit()
        #
        # cur.execute("""CREATE TABLE IF NOT EXISTS phones(id SERIAL PRIMARY KEY, phone VARCHAR(30) NOT NULL, client_id INTEGER NOT NULL REFERENCES clients(id));""")
        # conn.commit()
        #
        # cur.execute("""INSERT INTO clients(first_name, last_name, email) VALUES('Vanya', 'Ivanov', 'Vanya@ya.ru'), ('Igor', 'Petrov', 'Igor@ya.ru'), ('Sasha', 'Sidorov', 'Sasha@ya.ru');""")
        # conn.commit()
        #
        # cur.execute("""INSERT INTO phones(phone, client_id) VALUES('81234567', 1), ('82312352', 2), ('83251751', 3);""")
        # conn.commit()
        #
        # cur.execute("""SELECT client_id, phone FROM phones WHERE client_id=3 AND phone='81234567';""")
        # conn.commit()
        # print(cur.fetchone())
        #
        # cur.execute("""INSERT INTO phones(client_id, phone) VALUES(3, '81234567');""")
        # conn.commit()
        #
        # cur.execute("""INSERT INTO phones(client_id, phone) VALUES(1, '82312352');""")
        # conn.commit()
        #
        # cur.execute("""INSERT INTO phones(client_id, phone) VALUES(2, '83251751');""")
        # conn.commit()
        #
        # cur.execute("""UPDATE clients SET first_name='Petya' WHERE id=1""")
        # conn.commit()
        # #
        # cur.execute("""UPDATE clients SET last_name='Vasechkin' WHERE id=2""")
        # conn.commit()
        # #
        # cur.execute("""UPDATE clients SET email='Sidorov@ya.ru' WHERE id=3""")
        # conn.commit()
        #
        # cur.execute("""DELETE FROM phones WHERE client_id=1 and phone='83125717';""")
        # conn.commit()
        #
        # cur.execute("""DELETE FROM phones WHERE client_id=1 and phone='82312352';""")
        # conn.commit()
        #
        # cur.execute("""DELETE FROM phones WHERE client_id=3;""")
        # conn.commit()
        #
        # cur.execute("""DELETE FROM clients WHERE id=3;""")
        # conn.commit()

        # cur.execute("""SELECT clients.id FROM clients JOIN phones ON phones.client_id = clients.id WHERE phones.phone='81234567';""")
        # conn.commit()
        # print(cur.fetchall())
        #
        # cur.execute("""SELECT id FROM clients WHERE first_name='Igor' OR last_name='Ivanov' OR email='Ivanov';""")
        # conn.commit()
        # print(cur.fetchall())