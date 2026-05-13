# gui/parametres.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from config import BG_SECTION, TEXT_PRIMARY, BTN_PRIMARY_BG, BTN_WARNING_BG, BTN_TEXT
from utils.backup import sauvegarder_base_donnees, restaurer_base_donnees, lister_sauvegardes
from auth import AuthSystem


class ParametresGUI:
    def __init__(self, parent, db, auth):
        self.db = db
        self.auth = auth
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.parent, bg=BG_SECTION)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        tk.Label(main_frame, text="PARAMÈTRES", font=('Arial', 18, 'bold'), bg=BG_SECTION, fg=TEXT_PRIMARY).pack(
            pady=20)

        backup_frame = tk.Frame(main_frame, bg=BG_SECTION, relief='groove', bd=2)
        backup_frame.pack(fill='x', padx=20, pady=10)

        tk.Label(backup_frame, text="💾 Sauvegarde et Restauration", font=('Arial', 14, 'bold'), bg=BG_SECTION,
                 fg=TEXT_PRIMARY).pack(anchor='w', padx=20, pady=10)

        btn_sauvegarde = tk.Button(backup_frame, text="Sauvegarder la base", command=self.sauvegarder,
                                   bg=BTN_PRIMARY_BG, fg=BTN_TEXT, width=20)
        btn_sauvegarde.pack(anchor='w', padx=20, pady=5)

        btn_restaurer = tk.Button(backup_frame, text="Restaurer une sauvegarde", command=self.restaurer,
                                  bg=BTN_WARNING_BG, fg=BTN_TEXT, width=20)
        btn_restaurer.pack(anchor='w', padx=20, pady=5)

        self.backup_listbox = tk.Listbox(backup_frame, height=5, width=50)
        self.backup_listbox.pack(anchor='w', padx=20, pady=5, fill='x')
        self.rafraichir_liste_sauvegardes()

        users_frame = tk.Frame(main_frame, bg=BG_SECTION, relief='groove', bd=2)
        users_frame.pack(fill='x', padx=20, pady=10)

        tk.Label(users_frame, text="👥 Gestion des utilisateurs", font=('Arial', 14, 'bold'), bg=BG_SECTION,
                 fg=TEXT_PRIMARY).pack(anchor='w', padx=20, pady=10)

        if self.auth.has_permission('admin'):
            self.setup_gestion_utilisateurs(users_frame)
        else:
            tk.Label(users_frame, text="Accès réservé à l'administrateur", font=('Arial', 11), bg=BG_SECTION,
                     fg="#C0392B").pack(anchor='w', padx=20, pady=10)

    def setup_gestion_utilisateurs(self, parent):
        form_frame = tk.Frame(parent, bg=BG_SECTION)
        form_frame.pack(fill='x', padx=20, pady=10)

        tk.Label(form_frame, text="Nom d'utilisateur:", bg=BG_SECTION).grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.new_username = tk.Entry(form_frame, width=20)
        self.new_username.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Mot de passe:", bg=BG_SECTION).grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.new_password = tk.Entry(form_frame, width=20, show="*")
        self.new_password.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Rôle:", bg=BG_SECTION).grid(row=0, column=4, padx=5, pady=5, sticky='e')
        self.new_role = ttk.Combobox(form_frame, values=['pharmacien', 'stagiaire'], width=12)
        self.new_role.grid(row=0, column=5, padx=5, pady=5)
        self.new_role.set('pharmacien')

        tk.Button(form_frame, text="Ajouter", command=self.ajouter_utilisateur, bg=BTN_PRIMARY_BG, fg=BTN_TEXT,
                  width=10).grid(row=0, column=6, padx=10, pady=5)

        self.users_tree = ttk.Treeview(parent, columns=('ID', 'Nom', 'Rôle'), show='headings', height=5)
        self.users_tree.heading('ID', text='ID')
        self.users_tree.heading('Nom', text='Nom')
        self.users_tree.heading('Rôle', text='Rôle')
        self.users_tree.column('ID', width=50)
        self.users_tree.column('Nom', width=150)
        self.users_tree.column('Rôle', width=100)
        self.users_tree.pack(fill='x', padx=20, pady=10)

        self.rafraichir_utilisateurs()

    def rafraichir_utilisateurs(self):
        self.db.cursor.execute("SELECT id, username, role FROM utilisateurs")
        users = self.db.cursor.fetchall()

        self.users_tree.delete(*self.users_tree.get_children())
        for u in users:
            self.users_tree.insert('', 'end', values=u)

    def ajouter_utilisateur(self):
        auth_temp = AuthSystem(self.db)

        username = self.new_username.get()
        password = self.new_password.get()
        role = self.new_role.get()

        if not username or not password:
            messagebox.showerror("Erreur", "Nom et mot de passe requis")
            return

        hashed = auth_temp.hash_password(password)

        try:
            from datetime import datetime
            self.db.cursor.execute(
                "INSERT INTO utilisateurs (username, password, role, nom_complet, date_creation) VALUES (?, ?, ?, ?, ?)",
                (username, hashed, role, username, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            self.db.conn.commit()
            self.db.ajouter_log(self.auth.current_user[0], "Création utilisateur", f"Ajout de l'utilisateur {username}")
            messagebox.showinfo("Succès", "Utilisateur ajouté")
            self.new_username.delete(0, tk.END)
            self.new_password.delete(0, tk.END)
            self.rafraichir_utilisateurs()
        except:
            messagebox.showerror("Erreur", "Nom d'utilisateur existe déjà")

    def sauvegarder(self):
        backup_path = sauvegarder_base_donnees()
        if backup_path:
            self.db.ajouter_log(self.auth.current_user[0], "Sauvegarde", f"Sauvegarde créée: {backup_path}")
            messagebox.showinfo("Succès", f"Sauvegarde créée:\n{backup_path}")
            self.rafraichir_liste_sauvegardes()
        else:
            messagebox.showerror("Erreur", "Erreur lors de la sauvegarde")

    def restaurer(self):
        selection = self.backup_listbox.curselection()
        if not selection:
            messagebox.showerror("Erreur", "Sélectionnez une sauvegarde")
            return

        fichier = self.backup_listbox.get(selection[0])
        backup_path = f"backups/{fichier}"

        if messagebox.askyesno("Confirmation", "La restauration effacera les données actuelles. Continuer ?"):
            if restaurer_base_donnees(backup_path):
                self.db.ajouter_log(self.auth.current_user[0], "Restauration", f"Restauration depuis {fichier}")
                messagebox.showinfo("Succès", "Base restaurée. Redémarrez l'application.")
            else:
                messagebox.showerror("Erreur", "Erreur lors de la restauration")

    def rafraichir_liste_sauvegardes(self):
        self.backup_listbox.delete(0, tk.END)
        for f in lister_sauvegardes():
            self.backup_listbox.insert(tk.END, f)