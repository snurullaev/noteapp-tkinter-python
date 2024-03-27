from tkinter import *
import customtkinter
import sqlite3

noteapp = Tk()

# Функция для подключения к базе данных и создания таблицы
def db_start():
    global conn, cur
    conn = sqlite3.connect('notes.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, note TEXT)")

# Функция для обновления списка заметок из базы данных
def update_notes():
    notes_list.delete(0, customtkinter.END)  # Очищаем список заметок
    cur.execute("SELECT * FROM notes")
    notes = cur.fetchall()
    for note in notes:
        notes_list.insert(customtkinter.END, note[1])

# Функция для сохранения новой заметки
def save_button():
    note = note_entry.get()
    cur.execute("INSERT INTO notes (note) VALUES (?)", (note,))
    conn.commit()
    update_notes()
    note_entry.delete(0, customtkinter.END)

# Функция для удаления выбранной заметки
def delete_button():
    index = notes_list.curselection()
    if index:
        selected_note = notes_list.get(index)
        cur.execute("DELETE FROM notes WHERE note=?", (selected_note,))
        conn.commit()
        update_notes()

# Заголовок и настройка окна приложения
noteapp.title('Заметки')
noteapp.geometry('268x288')
noteapp.resizable(0, 0)
noteapp['bg'] = 'gray'

# Создание виджетов GUI
note_label = customtkinter.CTkLabel(noteapp, text='Заметки: ')
note_label.pack(pady=5)

note_entry = customtkinter.CTkEntry(noteapp)
note_entry.pack(pady=5)

save_button = customtkinter.CTkButton(noteapp, text='Добавить заметку', command=save_button)
save_button.pack(pady=5)

delete_button = customtkinter.CTkButton(noteapp, text='Удалить заметку', command=delete_button)
delete_button.pack(pady=5)

notes_list = Listbox(noteapp, width=45, height=15)
notes_list.pack(pady=5)

db_start()  # соединение с базой данных
update_notes()  # Получаем и выводим текущие заметки из базы данных

noteapp.mainloop()
conn.close()  # Закрываем соединение с базой данных по завершении работы с программой
