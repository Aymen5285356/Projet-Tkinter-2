# database.py
import sqlite3
from datetime import datetime
from config import DB_PATH


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.insert_default_data()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS utilisateurs (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT UNIQUE NOT NULL,
                                password TEXT NOT NULL,
                                role TEXT CHECK(role IN ('admin', 'pharmacien', 'stagiaire')),
                                nom_complet TEXT,
                                date_creation TEXT)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS produits (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                code_barre TEXT UNIQUE,
                                nom TEXT NOT NULL,
                                categorie TEXT,
                                laboratoire TEXT,
                                prix_achat REAL,
                                prix_vente REAL,
                                tva REAL DEFAULT 20,
                                quantite INTEGER DEFAULT 0,
                                seuil_alerte INTEGER DEFAULT 10,
                                date_peremption TEXT,
                                date_entree TEXT)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS clients (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nom TEXT NOT NULL,
                                telephone TEXT,
                                email TEXT,
                                adresse TEXT,
                                points_fidelite INTEGER DEFAULT 0,
                                date_inscription TEXT)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS ventes (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                numero_facture TEXT UNIQUE,
                                client_id INTEGER,
                                date_vente TEXT,
                                total_ht REAL,
                                tva_total REAL,
                                total_ttc REAL,
                                type_paiement TEXT,
                                remise REAL DEFAULT 0,
                                FOREIGN KEY (client_id) REFERENCES clients(id))''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS vente_details (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                vente_id INTEGER,
                                produit_id INTEGER,
                                quantite INTEGER,
                                prix_unitaire REAL,
                                FOREIGN KEY (vente_id) REFERENCES ventes(id),
                                FOREIGN KEY (produit_id) REFERENCES produits(id))''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                utilisateur_id INTEGER,
                                action TEXT,
                                details TEXT,
                                date_action TEXT)''')
        self.conn.commit()

    def insert_default_data(self):
        self.cursor.execute("SELECT COUNT(*) FROM utilisateurs")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute('''INSERT INTO utilisateurs (username, password, role, nom_complet, date_creation)
                                   VALUES ('admin', 'c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd3', 'admin', 'Administrateur', ?)''',
                                (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))
            self.conn.commit()

    def get_utilisateur(self, username):
        self.cursor.execute("SELECT * FROM utilisateurs WHERE username=?", (username,))
        return self.cursor.fetchone()

    def ajouter_produit(self, produit):
        self.cursor.execute('''INSERT INTO produits (code_barre, nom, categorie, laboratoire, prix_achat, prix_vente, tva, quantite, seuil_alerte, date_peremption, date_entree)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                            (produit['code_barre'], produit['nom'], produit['categorie'], produit['laboratoire'],
                             produit['prix_achat'], produit['prix_vente'], produit['tva'], produit['quantite'],
                             produit['seuil_alerte'], produit['date_peremption'], datetime.now().strftime("%Y-%m-%d")))
        self.conn.commit()
        return self.cursor.lastrowid

    def modifier_produit(self, id, produit):
        self.cursor.execute('''UPDATE produits SET code_barre=?, nom=?, categorie=?, laboratoire=?, 
                               prix_achat=?, prix_vente=?, tva=?, quantite=?, seuil_alerte=?, date_peremption=?
                               WHERE id=?''',
                            (produit['code_barre'], produit['nom'], produit['categorie'], produit['laboratoire'],
                             produit['prix_achat'], produit['prix_vente'], produit['tva'], produit['quantite'],
                             produit['seuil_alerte'], produit['date_peremption'], id))
        self.conn.commit()

    def supprimer_produit(self, id):
        self.cursor.execute("DELETE FROM produits WHERE id=?", (id,))
        self.conn.commit()

    def get_all_produits(self):
        self.cursor.execute("SELECT * FROM produits ORDER BY nom")
        return self.cursor.fetchall()

    def rechercher_produits(self, terme):
        terme = f'%{terme}%'
        self.cursor.execute('''SELECT * FROM produits WHERE nom LIKE ? OR code_barre LIKE ? 
                               OR categorie LIKE ? OR laboratoire LIKE ?''',
                            (terme, terme, terme, terme))
        return self.cursor.fetchall()

    def get_produit_by_code(self, code_barre):
        self.cursor.execute("SELECT * FROM produits WHERE code_barre=?", (code_barre,))
        return self.cursor.fetchone()

    def get_produit_by_id(self, id):
        self.cursor.execute("SELECT * FROM produits WHERE id=?", (id,))
        return self.cursor.fetchone()

    def ajouter_client(self, client):
        self.cursor.execute('''INSERT INTO clients (nom, telephone, email, adresse, points_fidelite, date_inscription)
                               VALUES (?, ?, ?, ?, ?, ?)''',
                            (client['nom'], client['telephone'], client['email'], client['adresse'],
                             0, datetime.now().strftime("%Y-%m-%d")))
        self.conn.commit()
        return self.cursor.lastrowid

    def modifier_client(self, id, client):
        self.cursor.execute("UPDATE clients SET nom=?, telephone=?, email=?, adresse=? WHERE id=?",
                            (client['nom'], client['telephone'], client['email'], client['adresse'], id))
        self.conn.commit()

    def supprimer_client(self, id):
        self.cursor.execute("DELETE FROM clients WHERE id=?", (id,))
        self.conn.commit()

    def get_all_clients(self):
        self.cursor.execute("SELECT * FROM clients ORDER BY nom")
        return self.cursor.fetchall()

    def rechercher_clients(self, terme):
        terme = f'%{terme}%'
        self.cursor.execute("SELECT * FROM clients WHERE nom LIKE ? OR telephone LIKE ?", (terme, terme))
        return self.cursor.fetchall()

    def enregistrer_vente(self, vente, details):
        self.cursor.execute('''INSERT INTO ventes (numero_facture, client_id, date_vente, total_ht, tva_total, total_ttc, type_paiement, remise)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                            (vente['numero_facture'], vente['client_id'], datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                             vente['total_ht'], vente['tva_total'], vente['total_ttc'], vente['type_paiement'],
                             vente['remise']))
        vente_id = self.cursor.lastrowid

        for detail in details:
            self.cursor.execute('''INSERT INTO vente_details (vente_id, produit_id, quantite, prix_unitaire)
                                   VALUES (?, ?, ?, ?)''',
                                (vente_id, detail['produit_id'], detail['quantite'], detail['prix_unitaire']))
            self.cursor.execute("UPDATE produits SET quantite = quantite - ? WHERE id=?",
                                (detail['quantite'], detail['produit_id']))

        self.conn.commit()
        return vente_id

    def get_ventes_journalieres(self):
        aujourdhui = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute('''SELECT v.*, c.nom as client_nom 
                               FROM ventes v 
                               LEFT JOIN clients c ON v.client_id = c.id 
                               WHERE date(v.date_vente) = ?''', (aujourdhui,))
        return self.cursor.fetchall()

    def get_ventes_par_periode(self, date_debut, date_fin):
        self.cursor.execute('''SELECT v.*, c.nom as client_nom 
                               FROM ventes v 
                               LEFT JOIN clients c ON v.client_id = c.id 
                               WHERE date(v.date_vente) BETWEEN ? AND ?''', (date_debut, date_fin))
        return self.cursor.fetchall()

    def get_top_produits(self, limit=10):
        self.cursor.execute('''SELECT p.nom, SUM(vd.quantite) as total_vendu
                               FROM vente_details vd
                               JOIN produits p ON vd.produit_id = p.id
                               GROUP BY p.id
                               ORDER BY total_vendu DESC
                               LIMIT ?''', (limit,))
        return self.cursor.fetchall()

    def get_produits_expirant_bientot(self, jours=30):
        from datetime import datetime, timedelta
        date_limite = (datetime.now() + timedelta(days=jours)).strftime("%Y-%m-%d")
        self.cursor.execute("SELECT * FROM produits WHERE date_peremption <= ? AND date_peremption != ''",
                            (date_limite,))
        return self.cursor.fetchall()

    def get_produits_stock_faible(self):
        self.cursor.execute("SELECT * FROM produits WHERE quantite <= seuil_alerte")
        return self.cursor.fetchall()

    def ajouter_log(self, utilisateur_id, action, details):
        self.cursor.execute('''INSERT INTO logs (utilisateur_id, action, details, date_action)
                               VALUES (?, ?, ?, ?)''',
                            (utilisateur_id, action, details, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.commit()

    def get_logs(self, limit=100):
        self.cursor.execute("SELECT * FROM logs ORDER BY date_action DESC LIMIT ?", (limit,))
        return self.cursor.fetchall()

    def get_statistiques(self):
        self.cursor.execute("SELECT COUNT(*) FROM produits")
        total_produits = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT SUM(quantite) FROM produits")
        total_stock = self.cursor.fetchone()[0] or 0

        self.cursor.execute("SELECT COUNT(*) FROM clients")
        total_clients = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM ventes WHERE date(date_vente) = date('now')")
        ventes_aujourdhui = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT SUM(total_ttc) FROM ventes WHERE date(date_vente) = date('now')")
        chiffre_aujourdhui = self.cursor.fetchone()[0] or 0

        return {
            'total_produits': total_produits,
            'total_stock': total_stock,
            'total_clients': total_clients,
            'ventes_aujourdhui': ventes_aujourdhui,
            'chiffre_aujourdhui': chiffre_aujourdhui
        }

    def close(self):
        self.conn.close()