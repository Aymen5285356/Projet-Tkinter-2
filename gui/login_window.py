# gui/login_window.py
import tkinter as tk
from tkinter import messagebox
from database import Database
from auth import AuthSystem
from gui.main_window import MainWindow
from config import BTN_PRIMARY_BG, BTN_TEXT, BG_MAIN, BG_SECTION, TEXT_PRIMARY


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacie - Connexion")
        self.root.geometry("500x550")
        self.root.configure(bg=BG_MAIN)
        self.root.resizable(False, False)

        self.db = Database()
        self.auth = AuthSystem(self.db)

        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg=BG_SECTION, relief='groove', bd=2)
        main_frame.pack(expand=True, fill='both', padx=40, pady=40)

        logo_label = tk.Label(main_frame, text="🏥 PHARMACIE", font=('Arial', 28, 'bold'),
                              bg=BG_SECTION, fg=BTN_PRIMARY_BG)
        logo_label.pack(pady=30)

        sous_titre = tk.Label(main_frame, text="Système de Gestion", font=('Arial', 12),
                              bg=BG_SECTION, fg=TEXT_PRIMARY)
        sous_titre.pack(pady=(0, 30))

        form_frame = tk.Frame(main_frame, bg=BG_SECTION)
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Nom d'utilisateur", font=('Arial', 11),
                 bg=BG_SECTION, fg=TEXT_PRIMARY).pack(anchor='w', pady=(0, 5))
        self.username_entry = tk.Entry(form_frame, font=('Arial', 12), width=30,
                                       relief='solid', bd=1)
        self.username_entry.pack(pady=(0, 15))

        tk.Label(form_frame, text="Mot de passe", font=('Arial', 11),
                 bg=BG_SECTION, fg=TEXT_PRIMARY).pack(anchor='w', pady=(0, 5))
        self.password_entry = tk.Entry(form_frame, font=('Arial', 12), width=30,
                                       show="*", relief='solid', bd=1)
        self.password_entry.pack(pady=(0, 20))

        self.btn_login = tk.Button(form_frame, text="Se connecter", command=self.login,
                                   bg=BTN_PRIMARY_BG, fg=BTN_TEXT, font=('Arial', 11, 'bold'),
                                   width=25, height=1, relief='flat', cursor='hand2')
        self.btn_login.pack()

        info_label = tk.Label(main_frame, text="Compte par défaut: admin / admin123",
                              font=('Arial', 9), bg=BG_SECTION, fg="#888888")
        info_label.pack(pady=(30, 0))

        self.root.bind('<Return>', lambda e: self.login())

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Erreur", "Veuillez saisir nom d'utilisateur et mot de passe")
            return

        if self.auth.login(username, password):
            self.root.destroy()
            root = tk.Tk()
            app = MainWindow(root, self.db, self.auth)
            root.mainloop()
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")