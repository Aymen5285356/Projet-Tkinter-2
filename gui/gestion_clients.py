# gui/gestion_clients.py
import tkinter as tk
from tkinter import ttk, messagebox
from config import BG_SECTION, TEXT_PRIMARY, BTN_PRIMARY_BG, BTN_DANGER_BG, BTN_TEXT


class GestionClientsGUI:
    def __init__(self, parent, db, auth):
        self.db = db
        self.auth = auth
        self.parent = parent
        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        form_frame = tk.Frame(self.parent, bg=BG_SECTION, relief='groove', bd=1)
        form_frame.pack(fill='x', padx=20, pady=10)

        champs = [
            ('Nom complet:', 'nom'), ('Téléphone:', 'telephone'),
            ('Email:', 'email'), ('Adresse:', 'adresse')
        ]

        self.entries = {}
        for i, (label, key) in enumerate(champs):
            row = i // 2
            col = (i % 2) * 2
            tk.Label(form_frame, text=label, font=('Arial', 10), bg=BG_SECTION, fg=TEXT_PRIMARY).grid(row=row,
                                                                                                      column=col,
                                                                                                      padx=5, pady=10,
                                                                                                      sticky='e')
            entry = tk.Entry(form_frame, font=('Arial', 10), width=25)
            entry.grid(row=row, column=col + 1, padx=5, pady=10, sticky='w')
            self.entries[key] = entry

        btn_frame = tk.Frame(form_frame, bg=BG_SECTION)
        btn_frame.grid(row=1, column=0, columnspan=4, pady=10)

        tk.Button(btn_frame, text="Ajouter", command=self.ajouter, bg=BTN_PRIMARY_BG, fg=BTN_TEXT, width=10).pack(
            side='left', padx=5)
        tk.Button(btn_frame, text="Modifier", command=self.modifier, bg=BTN_PRIMARY_BG, fg=BTN_TEXT, width=10).pack(
            side='left', padx=5)
        tk.Button(btn_frame, text="Supprimer", command=self.supprimer, bg=BTN_DANGER_BG, fg=BTN_TEXT, width=10).pack(
            side='left', padx=5)

        search_frame = tk.Frame(self.parent, bg=BG_SECTION)
        search_frame.pack(fill='x', padx=20, pady=10)

        tk.Label(search_frame, text="Rechercher:", font=('Arial', 10), bg=BG_SECTION).pack(side='left', padx=5)
        self.search_entry = tk.Entry(search_frame, font=('Arial', 10), width=30)
        self.search_entry.pack(side='left', padx=5)
        tk.Button(search_frame, text="Chercher", command=self.rechercher, bg=BTN_PRIMARY_BG, fg=BTN_TEXT).pack(
            side='left', padx=5)
        tk.Button(search_frame, text="Afficher tout", command=self.refresh_table, bg=BTN_PRIMARY_BG, fg=BTN_TEXT).pack(
            side='left', padx=5)

        self.tree = ttk.Treeview(self.parent, columns=('ID', 'Nom', 'Téléphone', 'Email', 'Adresse', 'Points'),
                                 show='headings', height=15)

        self.tree.heading('ID', text='ID')
        self.tree.heading('Nom', text='Nom')
        self.tree.heading('Téléphone', text='Téléphone')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Adresse', text='Adresse')
        self.tree.heading('Points', text='Points')

        self.tree.column('ID', width=50)
        self.tree.column('Nom', width=150)
        self.tree.column('Téléphone', width=120)
        self.tree.column('Email', width=200)
        self.tree.column('Adresse', width=200)
        self.tree.column('Points', width=80)

        self.tree.pack(fill='both', expand=True, padx=20, pady=10)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def ajouter(self):
        client = {key: self.entries[key].get() for key in self.entries}

        if not client['nom']:
            messagebox.showerror("Erreur", "Nom requis")
            return

        self.db.ajouter_client(client)
        self.db.ajouter_log(self.auth.current_user[0], "Ajout client", f"Ajout du client {client['nom']}")
        self.refresh_table()
        self.vider_champs()
        messagebox.showinfo("Succès", "Client ajouté")

    def modifier(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror("Erreur", "Sélectionnez un client")
            return

        id = self.tree.item(selection[0])['values'][0]
        client = {key: self.entries[key].get() for key in self.entries}

        if not client['nom']:
            messagebox.showerror("Erreur", "Nom requis")
            return

        self.db.modifier_client(id, client)
        self.db.ajouter_log(self.auth.current_user[0], "Modification client", f"Modification du client {client['nom']}")
        self.refresh_table()
        self.vider_champs()
        messagebox.showinfo("Succès", "Client modifié")

    def supprimer(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror("Erreur", "Sélectionnez un client")
            return

        if messagebox.askyesno("Confirmation", "Supprimer ce client ?"):
            id = self.tree.item(selection[0])['values'][0]
            self.db.supprimer_client(id)
            self.db.ajouter_log(self.auth.current_user[0], "Suppression client", f"Suppression du client ID {id}")
            self.refresh_table()
            self.vider_champs()
            messagebox.showinfo("Succès", "Client supprimé")

    def rechercher(self):
        terme = self.search_entry.get()
        if not terme:
            self.refresh_table()
            return

        resultats = self.db.rechercher_clients(terme)
        self.tree.delete(*self.tree.get_children())
        for c in resultats:
            self.tree.insert('', 'end', values=c)

    def refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        clients = self.db.get_all_clients()
        for c in clients:
            self.tree.insert('', 'end', values=c)

    def on_select(self, event):
        selection = self.tree.selection()
        if selection:
            valeurs = self.tree.item(selection[0])['values']
            keys = list(self.entries.keys())
            for i, key in enumerate(keys):
                self.entries[key].delete(0, tk.END)
                self.entries[key].insert(0, str(valeurs[i + 1]) if valeurs[i + 1] else '')

    def vider_champs(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)