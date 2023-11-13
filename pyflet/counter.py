import flet as ft
import psycopg2

class Database:
    def insert_record(self, last_name, first_name, middle_name, birth_year, phone_number):
        conn = psycopg2.connect(
            dbname="personal_db",
            user="postgres",
            password="postgres",
            host="127.0.0.1",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO people (last_name, first_name, middle_name, birth_year, phone_number)
            VALUES (%s, %s, %s, %s, %s)
        ''', (last_name, first_name, middle_name, birth_year, phone_number))
        conn.commit()
        conn.close()
    
    def create_table(self):
        conn = psycopg2.connect(
            dbname="personal_db",
            user="postgres",
            password="postgres",
            host="127.0.0.1",
            port="5432"
            )
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS people (
                id SERIAL PRIMARY KEY,
                last_name VARCHAR(50),
                first_name VARCHAR(50),
                middle_name VARCHAR(50),
                birth_year VARCHAR(8),
                phone_number VARCHAR(20)
            )
        ''')
        conn.commit()
        conn.close()

def main(page: ft.Page):
    
    database = Database()
    def button_clicked(e):
        # Получение значений из текстовых полей
        name = tb1.value
        surname = tb2.value
        lastname = tb3.value
        birthday = tb4.value
        phone = tb5.value

        database.create_table()
        # Запись данных в базу данных
        database.insert_record(last_name=name, first_name=surname, middle_name=lastname, birth_year=birthday, phone_number=phone)

        # Обновление текстового поля
        t.value = (
            f"Textboxes values are:  "
            f"'{tb1.value}', "
            f"'{tb2.value}', "
            f"'{tb3.value}', "
            f"'{tb4.value}', "
            f"'{tb5.value}'."
        )
        page.update()

    t = ft.Text()
    tb1 = ft.TextField(label="Name")
    tb2 = ft.TextField(label="Surname")
    tb3 = ft.TextField(label="Lastname")
    tb4 = ft.TextField(label="Birthday")
    tb5 = ft.TextField(label="Phone")
    b = ft.ElevatedButton(text="Submit", on_click=button_clicked)
    
    page.add(tb1, tb2, tb3, tb4, tb5, b, t)

# Запуск приложения
ft.app(target=main)
