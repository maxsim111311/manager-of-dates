# pip install calendar_widget
import time
from calendar_widget import Calendar
import tkinter as tk
from  tkinter import ttk
import sqlite3
from datetime import datetime
import  pandas as pd
from random import randint
import threading

def create_tables():
    '''
    Для каждого вида праздников создается таблица с данными,
    которые хранятся в файле "src\db\holidays.db"
    '''
    conn = sqlite3.connect("src\\db\\holidays.db")
    cursor = conn.cursor()

    categories = ['country', 'world', 'user', 'school']
    for category in categories:
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {category}_hlds (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                desc TEXT,
                time TEXT NOT NULL,
                date TEXT NOT NULL  
            );
        ''')

    conn.commit()
    cursor.close()
    conn.close()

def get_time():
    ''' Функция возвращает настоящее время '''
    return datetime.now().strftime("%H:%M")

def add_holiday(name, desc, time, date):
    '''
    Функция добавляет праздник, в зависимости от его категории
    Параметры:
        name - имя
        desc - описание
        time - время начала и конца
        date - дата
    '''
    conn = sqlite3.connect("src\\db\\holidays.db")
    cursor = conn.cursor()
    df = pd.read_sql_query(f"SELECT id  FROM user_hlds", conn)
    id = check_id(df, randint(100000, 999999))
    cursor.execute(
        f'''INSERT INTO user_hlds (id, name, desc, time, date) VALUES ({id}, '{name}', '{desc}', '{time}', '{date}');''')

def check_id(ids, id):
    '''
    В данной функции выполняется проверка id в списке ids, если он не уникален,
    генерирует новый и снова проверяет
    Параметры:
        id - идентификатор праздника
        ids - список всех id
    '''
    for _id in ids:
        if _id ==  id:
            new_id = randint(100000, 999999)
            return check_id(ids, new_id)
        return id

root = tk.Tk()
root.title("Менеджер дат")
root.geometry("450x600")

def notif():
    '''
    В данной функции выполняется воспроизведение уведомления в консоль,
    если до начала праздника осталось мало времени
    '''
    conn = sqlite3.connect("src\\db\\holidays.db")
    cursor = conn.cursor()
    df = pd.read_sql_query(f"SELECT date  FROM user_hlds", conn)
    cursor.close()
    conn.close()
    for hld in df:
        if (datetime(
            day=hld[4].split('-')[0],
            month=hld[4].split('-')[1],
            year=hld[4].split('-')[2],
        ) - datetime.now()).days < 2:
            print(f"СКОРО ПРАЗДНИК: {hld[1]} - {hld[2]} - {hld[3]}")
    cursor.close()
    conn.close()

def calendar_click():
    '''
    В данной функции считывается нажатие на дату, предлогается ввести название прздника,
    который отмечается в этот день, далее вводится время праздника, далее его описание,
    так же вывводится кнопка "Добавить праздник",
    по нажатию которой праздник сохраняется
    '''
    if calendar.getdate() is None:
        return
    win = tk.Toplevel(root)
    tk.Label(win, text="Название праздника").grid(pady=5, padx=5, row=0, column=0)
    name_input = tk.Entry(win)
    name_input.grid(pady=5, padx=5,row=0, column=1)
    tk.Label(win, text="Описание праздника:").grid(pady=5, padx=5, row=1, column=0)
    desk_input = tk.Text(win, height=10)
    desk_input.grid(pady=5, padx=5,row=1, column=1)
    tk.Label(win, text="Укажите время(ЧЧ:ММ, ЧЧ:ММ)").grid(pady=5, padx=5, row=2, column=0)
    time_input = tk.Text(win, height=10)
    time_input.grid(pady=5, padx=5, row=2, column=1)
    button_add = tk.Button(win, text="Добавить праздник", command=lambda:add_holiday(name_input.get(), desk_input.get(1.0, tk.END), time_input.get(), calendar.getdate(), "user"))
    button_add.grid(pady=5, padx=5, row=3, column=0, columnspan=2)
    '''
    Отрисовывается календарь, по заданным размерам и с заданными функциями
    Параметры:
    width - ширина
    height - длинна
    background - цвет фона
    '''
calendar = Calendar(
    root,
    width=450,
    height=600,
    background='black',
    command=calendar_click
)

create_tables()
root.mainloop()

create_tables()
thread = threading.Thread(target=root.mainloop())
thread.start()
while True:
    notif()
    time.sleep(3600)

