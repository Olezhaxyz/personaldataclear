import flet
from flet import ElevatedButton, Page, Text, TextField, icons


def main(page: Page):
    def button_clicked(e):
        t.value = (
            f"Textboxes values are:  "
            f"'{tb1.value}', "
            f"'{tb2.value}', "
            f"'{tb3.value}', "
            f"'{tb4.value}', "
            f"'{tb5.value}'."
        )
        page.update()

    t = Text()
    tb1 = TextField(label="Name")
    tb2 = TextField(label="Surname")
    tb3 = TextField(label="Lastname")
    tb4 = TextField(label="Bithday")
    tb5 = TextField(label="Phone")
    b = ElevatedButton(text="Submit", on_click=button_clicked)
    page.add(tb1, tb2, tb3, tb4, tb5, b, t)


flet.app(target=main)


class Database():
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
                birth_year INTEGER,
                phone_number VARCHAR(20)
            )
        ''')
        conn.commit()
        conn.close()
    def insert_record(self):
        last_name = self.ids.last_name.text
        first_name = self.ids.first_name.text
        middle_name = self.ids.middle_name.text
        birth_year = int(self.ids.birth_year.text)
        phone_number = self.ids.phone_number.text

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
