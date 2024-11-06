import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import os
import json

# File paths
USER_DATA_FILE = 'users.txt'
TASKS_FILE_TEMPLATE = 'Data/Data_Tugas_{}.json'

# Fungsi untuk menyimpan data pengguna
def save_user_data(username, password):
    # Buka file dalam mode append dan tambahkan username serta passoword
    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{username},{password}\n")

# Fungsi untuk memeriksa apakah username dan password valid
def check_credentials(username, password):
    if os.path.exists(USER_DATA_FILE):
        # periksa file pengguna menggunakan mode read-only
        with open(USER_DATA_FILE, "r") as file:
            # Membaca data pengguna dari file dan mencari kecocokan
            for line in file:
                stored_username, stored_password = line.strip().split(",")
                if username == stored_username and password == stored_password:
                    return True # login berhasil
    return False # login gagal

# Kelas untuk aplikasi To-Do List dengan fitur login
class TodoListApp:
    def __init__(self, root, username):
        self.root = root # Window utama tkinter
        self.username = username # Username saat ini
        self.tasks = self.load_tasks() # Memuat data tugas user

        # Set title for the window
        self.root.title(f"To-Do List - {self.username}")

        # Frame untuk menampilkan daftar tugas
        ttk.Label(text='List Tugas').pack()
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.task_listbox = tk.Listbox(self.frame, width=50, height=15)
        self.task_listbox.pack()

        self.load_tasks_to_listbox()

        # Entry untuk pencarian
        ttk.Label(text='Cari tugas:').pack()
        self.search_entry = tk.Entry(self.root, width=50)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.search_tasks)  # Pencarian saat mengetik

        # Tombol untuk menambah, mengedit, dan menghapus tugas
        self.add_button = tk.Button(self.root, text="Tambah Tugas", command=self.add_task)
        self.add_button.pack(pady=5)

        self.edit_button = tk.Button(self.root, text="Edit Tugas", command=self.edit_task)
        self.edit_button.pack(pady=5)

        self.delete_button = tk.Button(self.root, text="Hapus Tugas", command=self.delete_task)
        self.delete_button.pack(pady=5)

    # Memuat tugas dari file JSON berdasarkan username
    def load_tasks(self):
        task_file = TASKS_FILE_TEMPLATE.format(self.username)
        if os.path.exists(task_file):
            with open(task_file, 'r') as file:
                return json.load(file)
        return []

    # Menyimpan tugas ke file JSON berdasarkan username
    def save_tasks(self):
        task_file = TASKS_FILE_TEMPLATE.format(self.username)
        with open(task_file, 'w') as file:
            json.dump(self.tasks, file)

    # Memuat tugas ke listbox
    def load_tasks_to_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, f"{task['title']} - {task['description']}")

    # Fungsi menambah tugas
    def add_task(self):
        title = simpledialog.askstring("Input", "Masukkan judul tugas:")
        if title:
            description = simpledialog.askstring("Input", "Masukkan deskripsi tugas:")
            if description is not None:
                self.tasks.append({"title": title, "description": description})
                self.save_tasks()
                self.load_tasks_to_listbox()
            else:
                messagebox.showwarning("Input Error", "Deskripsi tidak boleh kosong.")
        else:
            messagebox.showwarning("Input Error", "Judul tidak boleh kosong.")

    # Fungsi edit tugas
    def edit_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            index = selected_task_index[0]
            current_task = self.tasks[index]
            new_title = simpledialog.askstring("Input", "Edit judul tugas:", initialvalue=current_task['title'])
            if new_title:
                new_description = simpledialog.askstring("Input", "Edit deskripsi tugas:", initialvalue=current_task['description'])
                if new_description is not None:
                    self.tasks[index] = {"title": new_title, "description": new_description}
                    self.save_tasks()
                    self.load_tasks_to_listbox()
                else:
                    messagebox.showwarning("Input Error", "Deskripsi tidak boleh kosong.")
            else:
                messagebox.showwarning("Input Error", "Judul tidak boleh kosong.")
        else:
            messagebox.showwarning("Selection Error", "Silakan pilih tugas yang ingin diedit.")

    # Fungsi hapus tugas
    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            index = selected_task_index[0]
            del self.tasks[index]
            self.save_tasks()
            self.load_tasks_to_listbox()
        else:
            messagebox.showwarning("Selection Error", "Silakan pilih tugas yang ingin dihapus.")

    # Fungsi untuk mencari tugas
    def search_tasks(self, event):
        search_term = self.search_entry.get().lower()
        self.task_listbox.delete(0, tk.END)

        for task in self.tasks:
            if search_term in task['title'].lower() or search_term in task['description'].lower():
                self.task_listbox.insert(tk.END, f"{task['title']} - {task['description']}")

# Fungsi untuk menangani login
def login():
    username = username_entry.get()
    password = password_entry.get()

    if check_credentials(username, password):
        root.destroy()
        new_root = tk.Tk()
        TodoListApp(new_root, username)
        new_root.mainloop()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Fungsi untuk menangani pendaftaran
def register():
    username = username_entry.get()
    password = password_entry.get()

    if username and password:
        save_user_data(username, password)
        messagebox.showinfo("Registration Successful", "User registered successfully!")
    else:
        messagebox.showwarning("Input Error", "Username and password cannot be empty.")

# Membuat jendela utama login
root = tk.Tk()
root.title("Login Form")
root.geometry("300x250")

# Membuat label dan entry untuk username dan password
username_label = tk.Label(root, text="Username:")
username_label.pack(pady=5)

username_entry = tk.Entry(root)
username_entry.pack(pady=5)

password_label = tk.Label(root, text="Password:")
password_label.pack(pady=5)

password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)

# Membuat tombol Login dan Register
login_button = tk.Button(root, text="Login", command=login)
login_button.pack(pady=5)

register_button = tk.Button(root, text="Register", command=register)
register_button.pack(pady=20)

# Menjalankan loop utama Tkinter
root.mainloop()
