# models/produit.py
class Produit:
    def __init__(self, id=None, code_barre=None, nom=None, categorie=None, laboratoire=None,
                 prix_achat=0, prix_vente=0, tva=20, quantite=0, seuil_alerte=10, date_peremption=None,
                 date_entree=None):
        self.id = id
        self.code_barre = code_barre
        self.nom = nom
        self.categorie = categorie
        self.laboratoire = laboratoire
        self.prix_achat = prix_achat
        self.prix_vente = prix_vente
        self.tva = tva
        self.quantite = quantite
        self.seuil_alerte = seuil_alerte
        self.date_peremption = date_peremption
        self.date_entree = date_entree

    def to_dict(self):
        return {
            'code_barre': self.code_barre,
            'nom': self.nom,
            'categorie': self.categorie,
            'laboratoire': self.laboratoire,
            'prix_achat': self.prix_achat,
            'prix_vente': self.prix_vente,
            'tva': self.tva,
            'quantite': self.quantite,
            'seuil_alerte': self.seuil_alerte,
            'date_peremption': self.date_peremption
        }

    def prix_ttc(self):
        return self.prix_vente * (1 + self.tva / 100)

    def est_en_stock(self):
        return self.quantite > 0

    def est_alerte_stock(self):
        return self.quantite <= self.seuil_alerte