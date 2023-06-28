import tkinter as tk
from tkinter import messagebox

def save_image():
    number = get_student_number.get()
    name = get_student_name.get()
    surname = get_student_surname.get()
    print(number, name, surname)
    messagebox.showinfo("Sistem", "Sisteme Başarıyla Giriş Yapıldı")


def create_window():
    global get_student_number, get_student_name, get_student_surname

    register_screen = tk.Tk()
    register_screen.title("Kayıt Ekranı")
    register_screen.geometry("400x400+700+200")

    get_number = tk.Label(register_screen, text="Öğrenci Numaranız: ", font="Times 10 bold")
    get_number.place(x=140, y=60)
    get_student_number = tk.Entry(register_screen)
    get_student_number.place(x=140, y=90, height=35)

    get_name = tk.Label(register_screen, text="Adınız: ", font="Times 10 bold")
    get_name.place(x=140, y=140)
    get_student_name = tk.Entry(register_screen, )
    get_student_name.place(x=140, y=170, height=35)

    get_surname = tk.Label(register_screen, text="Soyadınız: ", font="Times 10 bold")
    get_surname.place(x=140, y=220)
    get_student_surname = tk.Entry(register_screen)
    get_student_surname.place(x=140, y=250, height=35)

    button = tk.Button(register_screen, bg="white", text="Kaydet", command=lambda: [save_image(), register_screen.quit()])
    button.place(x=170, y=300, width=60, height=30)

    register_screen.mainloop()

create_window()