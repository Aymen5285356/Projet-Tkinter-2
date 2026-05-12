# gui/main_window.py
import tkinter as tk
from tkinter import ttk, messagebox
from gui.gestion_produits import GestionProduitsGUI
from gui.point_vente import PointVenteGUI
from gui.gestion_clients import GestionClientsGUI
from gui.rapports import RapportsGUI
from gui.alertes_stock import AlertesStockGUI
from gui.parametres import ParametresGUI
from config import BG_MAIN, BG_SECTION, BTN_PRIMARY_BG, BTN_TEXT


class MainWindow:
    def __init__(self, root, db, auth):
        self.root = root
        self.db = db
        self.auth = auth
        self.root.title("Pharmacie - Système de Gestion")
        self.root.geometry("1400x800")
        self.root.configure(bg=BG_MAIN)

        self.create_header()
        self.create_notebook()
        self.check_alerts()

    def create_header(self):
        header_frame = tk.Frame(self.root, bg=BTN_PRIMARY_BG, height=70)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)

        tk.Label(header_frame, text="🏥 PHARMACIE", font=('Arial', 22, 'bold'),
                 fg=BTN_TEXT, bg=BTN_PRIMARY_BG).pack(side='left', padx=30, pady=15)

        user_info = f"👤 {self.auth.current_user[1]} ({self.auth.current_user[3]})"
        tk.Label(header_frame, text=user_info, font=('Arial', 11),
                 fg=BTN_TEXT, bg=BTN_PRIMARY_BG).pack(side='right', padx=20, pady=15)

        btn_deconnexion = tk.Button(header_frame, text="Déconnexion", command=self.deconnexion,
                                    bg="#C0392B", fg=BTN_TEXT, font=('Arial', 10, 'bold'),
                                    relief='flat', cursor='hand2', padx=15)
        btn_deconnexion.pack(side='right', padx=20, pady=15)

    def create_notebook(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background=BG_MAIN, borderwidth=0)
        style.configure("TNotebook.Tab", font=('Arial', 11, 'bold'), padding=[15, 5])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        self.tab_vente = ttk.Frame(self.notebook)
        self.tab_produits = ttk.Frame(self.notebook)
        self.tab_clients = ttk.Frame(self.notebook)
        self.tab_rapports = ttk.Frame(self.notebook)
        self.tab_alertes = ttk.Frame(self.notebook)
        self.tab_parametres = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_vente, text="🛒 Point de Vente")
        self.notebook.add(self.tab_produits, text="📦 Produits")
        self.notebook.add(self.tab_clients, text="👥 Clients")
        self.notebook.add(self.tab_rapports, text="📊 Rapports")
        self.notebook.add(self.tab_alertes, text="⚠️ Alertes")
        self.notebook.add(self.tab_parametres, text="⚙️ Paramètres")

        self.point_vente = PointVenteGUI(self.tab_vente, self.db, self.auth)
        self.gestion_produits = GestionProduitsGUI(self.tab_produits, self.db, self.auth)
        self.gestion_clients = GestionClientsGUI(self.tab_clients, self.db, self.auth)
        self.rapports = RapportsGUI(self.tab_rapports, self.db, self.auth)
        self.alertes = AlertesStockGUI(self.tab_alertes, self.db, self.auth)
        self.parametres = ParametresGUI(self.tab_parametres, self.db, self.auth)

    def check_alerts(self):
        produits_exp = self.db.get_produits_expirant_bientot()
        produits_stock = self.db.get_produits_stock_faible()

        if produits_exp or produits_stock:
            self.notebook.select(self.tab_alertes)
            messagebox.showwarning("Alertes",
                                   f"⚠️ {len(produits_exp)} produit(s) expirent bientôt\n⚠️ {len(produits_stock)} produit(s) en stock faible")

    def deconnexion(self):
        if messagebox.askyesno("Déconnexion", "Voulez-vous vraiment vous déconnecter ?"):
            self.auth.logout()
            self.root.destroy()
            import tkinter as tk
            from gui.login_window import LoginWindow
            root = tk.Tk()
            LoginWindow(root)
            root.mainloop()