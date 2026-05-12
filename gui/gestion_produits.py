# gui/gestion_produits.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from config import BG_SECTION, TEXT_PRIMARY, BTN_PRIMARY_BG, BTN_DANGER_BG, BTN_TEXT


class GestionProduitsGUI:
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
            ('Code barre:', 'code_barre'), ('Nom:', 'nom'), ('Catégorie:', 'categorie'),
            ('Laboratoire:', 'laboratoire'), ('Prix achat:', 'prix_achat'), ('Prix vente:', 'prix_vente'),
            ('Quantité:', 'quantite'), ('Seuil alerte:', 'seuil_alerte'), ('Date péremption:', 'date_peremption')
        ]

        self.entries = {}
        for i, (label, key) in enumerate(champs):
            row = i // 3
            col = (i % 3) * 2
            tk.Label(form_frame, text=label, font=('Arial', 9), bg=BG_SECTION, fg=TEXT_PRIMARY).grid(row=row,
                                                                                                     column=col, padx=5,
                                                                                                     pady=5, sticky='e')
            entry = tk.Entry(form_frame, font=('Arial', 9), width=15)
            entry.grid(row=row, column=col + 1, padx=5, pady=5, sticky='w')
            self.entries[key] = entry

        self.entries['date_peremption'].insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entries['quantite'].insert(0, '0')
        self.entries['seuil_alerte'].insert(0, '10')

        btn_frame = tk.Frame(form_frame, bg=BG_SECTION)
        btn_frame.grid(row=3, column=0, columnspan=6, pady=10)

        tk.Button(btn_frame, text="Ajouter", command=self.ajouter, bg=BTN_PRIMARY_BG, fg=BTN_TEXT, width=10).pack(
            side='left', padx=5)
        tk.Button(btn_frame, text="Modifier", command=self.modifier, bg=BTN_PRIMARY_BG, fg=BTN_TEXT, width=10).pack(
            side='left', padx=5)
        tk.Button(btn_frame, text="Supprimer", command=self.supprimer, bg=BTN_DANGER_BG, fg=BTN_TEXT, width=10).pack(
            side='left', padx=5)
        tk.Button(btn_frame, text="Générer code", command=self.generer_code, bg="#27AE60", fg=BTN_TEXT, width=12).pack(
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

        self.tree = ttk.Treeview(self.parent,
                                 columns=('ID', 'Code', 'Nom', 'Catégorie', 'Laboratoire', 'PA', 'PV', 'Qte', 'Seuil',
                                          'Péremption'), show='headings', height=15)

        self.tree.heading('ID', text='ID')
        self.tree.heading('Code', text='Code barre')
        self.tree.heading('Nom', text='Nom')
        self.tree.heading('Catégorie', text='Catégorie')
        self.tree.heading('Laboratoire', text='Laboratoire')
        self.tree.heading('PA', text='PA')
        self.tree.heading('PV', text='PV')
        self.tree.heading('Qte', text='Quantité')
        self.tree.heading('Seuil', text='Seuil')
        self.tree.heading('Péremption', text='Péremption')

        self.tree.column('ID', width=40)
        self.tree.column('Code', width=100)
        self.tree.column('Nom', width=150)
        self.tree.column('Catégorie', width=100)
        self.tree.column('Laboratoire', width=120)
        self.tree.column('PA', width=70)
        self.tree.column('PV', width=70)
        self.tree.column('Qte', width=70)
        self.tree.column('Seuil', width=60)
        self.tree.column('Péremption', width=90)

        self.tree.pack(fill='both', expand=True, padx=20, pady=10)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def ajouter(self):
        if not self.auth.has_permission('pharmacien'):
            messagebox.showerror("Erreur", "Permission refusée")
            return

        produit = {key: self.entries[key].get() for key in self.entries}

        try:
            produit['prix_achat'] = float(produit['prix_achat']) if produit['prix_achat'] else 0
            produit['prix_vente'] = float(produit['prix_vente']) if produit['prix_vente'] else 0
            produit['quantite'] = int(produit['quantite']) if produit['quantite'] else 0
            produit['seuil_alerte'] = int(produit['seuil_alerte']) if produit['seuil_alerte'] else 10
            produit['tva'] = 20
        except:
            messagebox.showerror("Erreur", "Valeurs numériques invalides")
            return

        if not produit['nom']:
            messagebox.showerror("Erreur", "Le nom du produit est requis")
            return

        self.db.ajouter_produit(produit)
        self.db.ajouter_log(self.auth.current_user[0], "Ajout produit", f"Ajout du produit {produit['nom']}")
        self.refresh_table()
        self.vider_champs()
        messagebox.showinfo("Succès", "Produit ajouté")

    def modifier(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror("Erreur", "Sélectionnez un produit")
            return

        if not self.auth.has_permission('pharmacien'):
            messagebox.showerror("Erreur", "Permission refusée")
            return

        id = self.tree.item(selection[0])['values'][0]
        produit = {key: self.entries[key].get() for key in self.entries}

        try:
            produit['prix_achat'] = float(produit['prix_achat']) if produit['prix_achat'] else 0
            produit['prix_vente'] = float(produit['prix_vente']) if produit['prix_vente'] else 0
            produit['quantite'] = int(produit['quantite']) if produit['quantite'] else 0
            produit['seuil_alerte'] = int(produit['seuil_alerte']) if produit['seuil_alerte'] else 10
        except:
            messagebox.showerror("Erreur", "Valeurs numériques invalides")
            return

        if not produit['nom']:
            messagebox.showerror("Erreur", "Le nom du produit est requis")
            return

        self.db.modifier_produit(id, produit)
        self.db.ajouter_log(self.auth.current_user[0], "Modification produit",
                            f"Modification du produit {produit['nom']}")
        self.refresh_table()
        self.vider_champs()
        messagebox.showinfo("Succès", "Produit modifié")

    def supprimer(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror("Erreur", "Sélectionnez un produit")
            return

        if not self.auth.has_permission('admin'):
            messagebox.showerror("Erreur", "Permission refusée - Admin uniquement")
            return

        if messagebox.askyesno("Confirmation", "Supprimer ce produit ?"):
            id = self.tree.item(selection[0])['values'][0]
            self.db.supprimer_produit(id)
            self.db.ajouter_log(self.auth.current_user[0], "Suppression produit", f"Suppression du produit ID {id}")
            self.refresh_table()
            self.vider_champs()
            messagebox.showinfo("Succès", "Produit supprimé")

    def rechercher(self):
        terme = self.search_entry.get()
        if not terme:
            self.refresh_table()
            return

        resultats = self.db.rechercher_produits(terme)
        self.tree.delete(*self.tree.get_children())
        for p in resultats:
            self.tree.insert('', 'end', values=p)

    def refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        produits = self.db.get_all_produits()
        for p in produits:
            self.tree.insert('', 'end', values=p)

    def on_select(self, event):
        selection = self.tree.selection()
        if selection:
            valeurs = self.tree.item(selection[0])['values']
            keys = list(self.entries.keys())
            for i, key in enumerate(keys):
                self.entries[key].delete(0, tk.END)
                self.entries[key].insert(0, str(valeurs[i + 1]) if valeurs[i + 1] else '')

    def generer_code(self):
        import random
        code = f"PH{random.randint(10000, 99999)}{random.randint(100, 999)}"
        self.entries['code_barre'].delete(0, tk.END)
        self.entries['code_barre'].insert(0, code)

    def vider_champs(self):
        for key in self.entries:
            self.entries[key].delete(0, tk.END)
        self.entries['date_peremption'].insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entries['quantite'].insert(0, '0')
        self.entries['seuil_alerte'].insert(0, '10')