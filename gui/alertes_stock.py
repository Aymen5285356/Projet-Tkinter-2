# gui/alertes_stock.py
import tkinter as tk
from tkinter import ttk, messagebox
from config import BG_SECTION, TEXT_PRIMARY, BTN_PRIMARY_BG, BTN_TEXT


class AlertesStockGUI:
    def __init__(self, parent, db, auth):
        self.db = db
        self.auth = auth
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.parent, bg=BG_SECTION)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        tk.Label(main_frame, text="ALERTES STOCK", font=('Arial', 18, 'bold'), bg=BG_SECTION, fg="#C0392B").pack(
            pady=20)

        produits_stock = self.db.get_produits_stock_faible()

        tk.Label(main_frame, text="⚠️ Produits en stock faible", font=('Arial', 14, 'bold'), bg=BG_SECTION,
                 fg=TEXT_PRIMARY).pack(anchor='w', pady=10)

        stock_frame = tk.Frame(main_frame, bg=BG_SECTION, relief='groove', bd=2)
        stock_frame.pack(fill='x', padx=20, pady=10)

        if produits_stock:
            for p in produits_stock:
                tk.Label(stock_frame, text=f"📦 {p[2]} - Stock: {p[8]} (Seuil: {p[9]})", font=('Arial', 11),
                         bg=BG_SECTION, fg="#C0392B").pack(anchor='w', padx=20, pady=5)
        else:
            tk.Label(stock_frame, text="Aucun produit en stock faible", font=('Arial', 11), bg=BG_SECTION,
                     fg="#27AE60").pack(anchor='w', padx=20, pady=10)

        produits_exp = self.db.get_produits_expirant_bientot()

        tk.Label(main_frame, text="⚠️ Produits expirant bientôt", font=('Arial', 14, 'bold'), bg=BG_SECTION,
                 fg=TEXT_PRIMARY).pack(anchor='w', pady=10)

        exp_frame = tk.Frame(main_frame, bg=BG_SECTION, relief='groove', bd=2)
        exp_frame.pack(fill='x', padx=20, pady=10)

        if produits_exp:
            for p in produits_exp:
                tk.Label(exp_frame, text=f"💊 {p[2]} - Expiration: {p[10]}", font=('Arial', 11), bg=BG_SECTION,
                         fg="#E67E22").pack(anchor='w', padx=20, pady=5)
        else:
            tk.Label(exp_frame, text="Aucun produit expirant bientôt", font=('Arial', 11), bg=BG_SECTION,
                     fg="#27AE60").pack(anchor='w', padx=20, pady=10)

        btn_refresh = tk.Button(main_frame, text="Actualiser", command=self.refresh, bg=BTN_PRIMARY_BG, fg=BTN_TEXT,
                                font=('Arial', 10, 'bold'), width=15)
        btn_refresh.pack(pady=20)

    def refresh(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        self.setup_ui()