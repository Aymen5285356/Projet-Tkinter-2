# gui/rapports.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
from config import BG_SECTION, TEXT_PRIMARY, BTN_PRIMARY_BG, BTN_TEXT
from utils.export_excel import exporter_ventes_csv, exporter_produits_csv


class RapportsGUI:
    def __init__(self, parent, db, auth):
        self.db = db
        self.auth = auth
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.parent, bg=BG_SECTION)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        tk.Label(main_frame, text="RAPPORTS ET STATISTIQUES", font=('Arial', 18, 'bold'), bg=BG_SECTION,
                 fg=TEXT_PRIMARY).pack(pady=20)

        stats_frame = tk.Frame(main_frame, bg=BG_SECTION, relief='groove', bd=2)
        stats_frame.pack(fill='x', padx=20, pady=10)

        stats = self.db.get_statistiques()

        tk.Label(stats_frame, text=f"📦 Total produits: {stats['total_produits']}", font=('Arial', 12), bg=BG_SECTION,
                 fg=TEXT_PRIMARY).pack(anchor='w', padx=20, pady=5)
        tk.Label(stats_frame, text=f"💊 Total stock: {stats['total_stock']} unités", font=('Arial', 12), bg=BG_SECTION,
                 fg=TEXT_PRIMARY).pack(anchor='w', padx=20, pady=5)
        tk.Label(stats_frame, text=f"👥 Total clients: {stats['total_clients']}", font=('Arial', 12), bg=BG_SECTION,
                 fg=TEXT_PRIMARY).pack(anchor='w', padx=20, pady=5)
        tk.Label(stats_frame, text=f"🛒 Ventes aujourd'hui: {stats['ventes_aujourdhui']}", font=('Arial', 12),
                 bg=BG_SECTION, fg=TEXT_PRIMARY).pack(anchor='w', padx=20, pady=5)
        tk.Label(stats_frame, text=f"💰 Chiffre aujourd'hui: {stats['chiffre_aujourdhui']:.2f} DH",
                 font=('Arial', 12, 'bold'), bg=BG_SECTION, fg=BTN_PRIMARY_BG).pack(anchor='w', padx=20, pady=5)

        ventes_journalieres = self.db.get_ventes_journalieres()
        total_journalier = sum(v[6] for v in ventes_journalieres) if ventes_journalieres else 0
        tk.Label(stats_frame, text=f"📊 Total ventes aujourd'hui: {total_journalier:.2f} DH", font=('Arial', 12, 'bold'),
                 bg=BG_SECTION, fg="#27AE60").pack(anchor='w', padx=20, pady=5)

        produits_top = self.db.get_top_produits(5)

        tk.Label(main_frame, text="Top 5 des produits les plus vendus", font=('Arial', 14, 'bold'), bg=BG_SECTION,
                 fg=TEXT_PRIMARY).pack(pady=(20, 10))

        top_frame = tk.Frame(main_frame, bg=BG_SECTION, relief='groove', bd=2)
        top_frame.pack(fill='x', padx=20, pady=10)

        if produits_top:
            for i, produit in enumerate(produits_top, 1):
                tk.Label(top_frame, text=f"{i}. {produit[0]} - {produit[1]} ventes", font=('Arial', 11), bg=BG_SECTION,
                         fg="#555555").pack(anchor='w', padx=20, pady=5)
        else:
            tk.Label(top_frame, text="Aucune vente enregistrée", font=('Arial', 11), bg=BG_SECTION, fg="#888888").pack(
                anchor='w', padx=20, pady=10)

        export_frame = tk.Frame(main_frame, bg=BG_SECTION)
        export_frame.pack(pady=20)

        tk.Button(export_frame, text="Exporter ventes (CSV)", command=self.exporter_ventes, bg=BTN_PRIMARY_BG,
                  fg=BTN_TEXT, width=20).pack(side='left', padx=10)
        tk.Button(export_frame, text="Exporter produits (CSV)", command=self.exporter_produits, bg=BTN_PRIMARY_BG,
                  fg=BTN_TEXT, width=20).pack(side='left', padx=10)

        btn_refresh = tk.Button(main_frame, text="Actualiser", command=self.refresh, bg=BTN_PRIMARY_BG, fg=BTN_TEXT,
                                font=('Arial', 10, 'bold'), width=15)
        btn_refresh.pack(pady=20)

    def exporter_ventes(self):
        ventes = self.db.get_ventes_journalieres()
        if ventes:
            filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if filename:
                exporter_ventes_csv(ventes, filename)
                messagebox.showinfo("Succès", f"Exporté vers {filename}")
        else:
            messagebox.showwarning("Info", "Aucune vente à exporter")

    def exporter_produits(self):
        produits = self.db.get_all_produits()
        if produits:
            filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if filename:
                exporter_produits_csv(produits, filename)
                messagebox.showinfo("Succès", f"Exporté vers {filename}")
        else:
            messagebox.showwarning("Info", "Aucun produit à exporter")

    def refresh(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        self.setup_ui()