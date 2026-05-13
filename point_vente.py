# gui/point_vente.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from config import BG_SECTION, TEXT_PRIMARY, BTN_PRIMARY_BG, BTN_SUCCESS_BG, BTN_WARNING_BG, BTN_TEXT


class PointVenteGUI:
    def __init__(self, parent, db, auth):
        self.db = db
        self.auth = auth
        self.parent = parent
        self.panier = []
        self.setup_ui()

    def setup_ui(self):
        left_frame = tk.Frame(self.parent, bg=BG_SECTION, relief='groove', bd=1)
        left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

        tk.Label(left_frame, text="Scan code barre:", font=('Arial', 12, 'bold'), bg=BG_SECTION).pack(pady=10)
        self.code_entry = tk.Entry(left_frame, font=('Arial', 14), width=20)
        self.code_entry.pack(pady=5)
        self.code_entry.bind('<Return>', lambda e: self.ajouter_par_code())
        tk.Button(left_frame, text="Ajouter", command=self.ajouter_par_code, bg=BTN_PRIMARY_BG, fg=BTN_TEXT,
                  width=15).pack(pady=5)

        tk.Label(left_frame, text="Recherche produit:", font=('Arial', 10, 'bold'), bg=BG_SECTION).pack(pady=(20, 5))
        self.search_entry = tk.Entry(left_frame, font=('Arial', 10), width=25)
        self.search_entry.pack(pady=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.rechercher_produits())

        self.search_listbox = tk.Listbox(left_frame, height=15, width=35)
        self.search_listbox.pack(pady=5)
        self.search_listbox.bind('<Double-Button-1>', self.ajouter_depuis_liste)

        right_frame = tk.Frame(self.parent, bg=BG_SECTION, relief='groove', bd=1)
        right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        tk.Label(right_frame, text="Panier", font=('Arial', 14, 'bold'), bg=BG_SECTION).pack(pady=10)

        columns = ('ID', 'Nom', 'Qte', 'PU', 'Total')
        self.panier_tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=12)
        self.panier_tree.heading('ID', text='ID')
        self.panier_tree.heading('Nom', text='Nom')
        self.panier_tree.heading('Qte', text='Qte')
        self.panier_tree.heading('PU', text='PU')
        self.panier_tree.heading('Total', text='Total')
        self.panier_tree.column('ID', width=50)
        self.panier_tree.column('Nom', width=200)
        self.panier_tree.column('Qte', width=80)
        self.panier_tree.column('PU', width=100)
        self.panier_tree.column('Total', width=100)
        self.panier_tree.pack(fill='both', expand=True, padx=10, pady=5)

        total_frame = tk.Frame(right_frame, bg=BG_SECTION)
        total_frame.pack(fill='x', padx=10, pady=10)

        self.total_label = tk.Label(total_frame, text="Total TTC: 0.00 DH", font=('Arial', 16, 'bold'), bg=BG_SECTION,
                                    fg=BTN_PRIMARY_BG)
        self.total_label.pack(side='left', padx=10)

        tk.Button(total_frame, text="Supprimer", command=self.supprimer_du_panier, bg=BTN_WARNING_BG, fg=BTN_TEXT,
                  width=12).pack(side='right', padx=5)

        paiement_frame = tk.Frame(right_frame, bg=BG_SECTION)
        paiement_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(paiement_frame, text="Client:", bg=BG_SECTION).pack(side='left', padx=5)
        self.client_combo = ttk.Combobox(paiement_frame, width=25)
        self.client_combo.pack(side='left', padx=5)
        self.rafraichir_clients()

        tk.Label(paiement_frame, text="Paiement:", bg=BG_SECTION).pack(side='left', padx=5)
        self.paiement_combo = ttk.Combobox(paiement_frame, values=['Espèces', 'Carte bancaire', 'Chèque'], width=15)
        self.paiement_combo.pack(side='left', padx=5)
        self.paiement_combo.set('Espèces')

        tk.Button(paiement_frame, text="Valider Vente", command=self.valider_vente, bg=BTN_SUCCESS_BG, fg=BTN_TEXT,
                  width=15, font=('Arial', 10, 'bold')).pack(side='right', padx=10)

    def rafraichir_clients(self):
        clients = self.db.get_all_clients()
        self.client_combo['values'] = [f"{c[0]} - {c[1]}" for c in clients]

    def ajouter_par_code(self):
        code = self.code_entry.get()
        if not code:
            return

        produit = self.db.get_produit_by_code(code)
        if produit:
            self.ajouter_au_panier(produit)
            self.code_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Erreur", "Produit non trouvé")

    def rechercher_produits(self):
        terme = self.search_entry.get()
        if not terme:
            self.search_listbox.delete(0, tk.END)
            return

        produits = self.db.rechercher_produits(terme)
        self.search_listbox.delete(0, tk.END)
        for p in produits:
            if p[8] > 0:
                self.search_listbox.insert(tk.END, f"{p[0]} - {p[2]} ({p[8]} dispo) - {p[6]} DH")

    def ajouter_depuis_liste(self, event):
        selection = self.search_listbox.curselection()
        if selection:
            texte = self.search_listbox.get(selection[0])
            produit_id = int(texte.split(' - ')[0])
            produit = self.db.get_produit_by_id(produit_id)
            if produit:
                self.ajouter_au_panier(produit)

    def ajouter_au_panier(self, produit):
        for i, item in enumerate(self.panier):
            if item['id'] == produit[0]:
                if item['quantite'] + 1 <= produit[8]:
                    self.panier[i]['quantite'] += 1
                    self.rafraichir_panier()
                else:
                    messagebox.showerror("Erreur", "Stock insuffisant")
                return

        if produit[8] > 0:
            self.panier.append({
                'id': produit[0],
                'nom': produit[2],
                'quantite': 1,
                'prix': produit[6],
                'stock': produit[8]
            })
            self.rafraichir_panier()

    def supprimer_du_panier(self):
        selection = self.panier_tree.selection()
        if selection:
            item_id = int(self.panier_tree.item(selection[0])['values'][0])
            for i, item in enumerate(self.panier):
                if item['id'] == item_id:
                    del self.panier[i]
                    break
            self.rafraichir_panier()

    def rafraichir_panier(self):
        self.panier_tree.delete(*self.panier_tree.get_children())
        total = 0
        for item in self.panier:
            total_item = item['quantite'] * item['prix']
            total += total_item
            self.panier_tree.insert('', 'end', values=(item['id'], item['nom'], item['quantite'], f"{item['prix']:.2f}",
                                                       f"{total_item:.2f}"))

        self.total_label.config(text=f"Total TTC: {total:.2f} DH")

    def valider_vente(self):
        if not self.panier:
            messagebox.showerror("Erreur", "Panier vide")
            return

        total_ht = sum(i['quantite'] * i['prix'] for i in self.panier) / 1.2
        total_tva = total_ht * 0.2
        total_ttc = total_ht + total_tva

        client_sel = self.client_combo.get()
        client_id = None
        if client_sel:
            client_id = int(client_sel.split(' - ')[0])

        import random
        numero_facture = f"FACT{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(10, 99)}"

        vente = {
            'numero_facture': numero_facture,
            'client_id': client_id,
            'total_ht': total_ht,
            'tva_total': total_tva,
            'total_ttc': total_ttc,
            'type_paiement': self.paiement_combo.get(),
            'remise': 0
        }

        details = []
        for item in self.panier:
            details.append({
                'produit_id': item['id'],
                'quantite': item['quantite'],
                'prix_unitaire': item['prix']
            })

        self.db.enregistrer_vente(vente, details)
        self.db.ajouter_log(self.auth.current_user[0], "Vente", f"Vente {numero_facture} - {total_ttc:.2f} DH")

        messagebox.showinfo("Succès", f"Vente enregistrée\nFacture: {numero_facture}\nTotal: {total_ttc:.2f} DH")

        self.panier = []
        self.rafraichir_panier()
        self.rafraichir_clients()