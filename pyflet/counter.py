import flet as ft
import psycopg2

class Database:
    def insert_record(self, table, last_name, first_name, middle_name, birth_year, phone_number):
        conn = psycopg2.connect(
            dbname="personal_db",
            user="postgres",
            password="postgres",
            host="127.0.0.1",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO '''+ table +''' (last_name, first_name, middle_name, birth_year, phone_number)
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
            );
            CREATE TABLE IF NOT EXISTS unpeople (
                id SERIAL PRIMARY KEY,
                last_name VARCHAR(50),
                first_name VARCHAR(50),
                middle_name VARCHAR(50),
                birth_year VARCHAR(8),
                phone_number VARCHAR(20)
            );
        ''')
        conn.commit()
        conn.close()
        
    def fetch_all_records(self, table_name):
        conn = psycopg2.connect(
            dbname="personal_db",
            user="postgres",
            password="postgres",
            host="127.0.0.1",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute('SELECT * FROM ' + table_name)
        records = cur.fetchall()
        conn.close()
        return records    
    
    def get_value(self, id, value):
        conn = psycopg2.connect(
            dbname="personal_db",
            user="postgres",
            password="postgres",
            host="127.0.0.1",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute('SELECT ' + value + ' from people where' + id)
        result = cur.fetchone()[0]
        conn.close()
        return result  
    
        
def main(page: ft.Page):
    database = Database()
    
    database.create_table()
    
    def update_table(table, table_name):
        # Очищаем текущую таблицу
        table.rows.clear()
        records = database.fetch_all_records(table_name)
        for row_data in records:
            cells = [ft.DataCell(ft.Text(str(cell))) for cell in row_data]
            table.rows.append(ft.DataRow(cells=cells))
    
    # Create the first table
    table1 = ft.DataTable(
        bgcolor="#4B0082",
        border_radius=10,
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Last Name")),
            ft.DataColumn(ft.Text("First Name")),
            ft.DataColumn(ft.Text("Middle Name")),
            ft.DataColumn(ft.Text("Birth Year")),
            ft.DataColumn(ft.Text("Phone Number")),
        ],
        rows=[],
    )
    
    # Create the second table
    table2 = ft.DataTable(
        bgcolor="#008080",
        border_radius=10,
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Last Name")),
            ft.DataColumn(ft.Text("First Name")),
            ft.DataColumn(ft.Text("Middle Name")),
            ft.DataColumn(ft.Text("Birth Year")),
            ft.DataColumn(ft.Text("Phone Number")),
        ],
        rows=[],
    )

 
    
    def button_clicked(e):
        # Получение значений из текстовых полей
        name = tb1.value
        surname = tb2.value
        lastname = tb3.value
        birthday = tb4.value
        phone = tb5.value

        
        # Запись данных в базу данных
        database.insert_record(table='people',last_name=name, first_name=surname, middle_name=lastname, birth_year=birthday, phone_number=phone)

        # Обновление текстового поля
        t.value = (
            f"Textboxes values are:  "
            f"'{tb1.value}', "
            f"'{tb2.value}', "
            f"'{tb3.value}', "
            f"'{tb4.value}', "
            f"'{tb5.value}'."
        )
        # Обновление данных в первой таблице
        update_table(table1, 'people')

        # Обновление страницы
        page.update()

    def shift_columns_down(data):
        # Определяем сдвиги для каждой колонки
        shifts = [0, 1, 3, 2, 1]

        # Получаем количество строк и столбцов в данных
        num_rows = len(data)
        num_columns = len(data[0])

        # Создаем новый список с сдвинутыми колонками вниз
        shifted_data = [[data[(i - shifts[j % num_rows]) % num_rows][j] for j in range(num_columns)] for i in range(num_rows)]

        return shifted_data
    
    def shift_columns_up(data):
        # Определяем сдвиги для каждой колонки
        shifts = [0, 1, 3, 2, 1]

        # Получаем количество строк и столбцов в данных
        num_rows = len(data)
        num_columns = len(data[0])

        # Создаем новый список с сдвинутыми колонками вверх
        shifted_data = [[data[(i + shifts[j % num_rows]) % num_rows][j] for j in range(num_columns)] for i in range(num_rows)]

        return shifted_data

    def unpesronal_button(e):
        # Получаем все записи из базы данных
        records = database.fetch_all_records('people')
        
        shifted_data = shift_columns_down(records)
        # Вывод результатов
        for row in shifted_data:
            database.insert_record('unpeople', *row[1:])
        # Обновление данных в таблице
        update_table(table2,'unpeople')

        # Обновление страницы
        page.update()
        
    def pesronal_button(e):
        # Получаем все записи из базы данных
        records = database.fetch_all_records('unpeople')
        
        shifted_data = shift_columns_up(records)
        # Вывод результатов
        for row in shifted_data:
            database.insert_record('unpeople', *row[1:])
        # Обновление данных в таблице
        update_table(table2,'unpeople')

        # Обновление страницы
        page.update()


    t = ft.Text()
    tb1 = ft.TextField(label="Name")
    tb2 = ft.TextField(label="Surname")
    tb3 = ft.TextField(label="Lastname")
    tb4 = ft.TextField(label="Birthday")
    tb5 = ft.TextField(label="Phone")
    b = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=button_clicked)
    un = ft.ElevatedButton(text="Uppersonal", icon=ft.icons.SAFETY_CHECK, on_click=unpesronal_button)
    not_un = ft.ElevatedButton(icon=ft.icons.SAFETY_DIVIDER, text="Personal", on_click=pesronal_button)
    tabs = ft.Tabs(
        selected_index=1,
        animation_duration=300,
        tabs=[
            ft.Tab(
                tab_content=ft.Icon(ft.icons.ACCOUNT_BOX),
                content=table2,
            ),
        ],
        expand=1,
    )
    update_table(table1,'people')
    update_table(table2,'unpeople')
    page.add(tb1, tb2, tb3, tb4, tb5, b, t, table1, un, not_un, tabs)
    
        
    page.scroll = "always"
    page.update()
    
# Запуск приложения
ft.app(target=main)
