# models/vente.py
from datetime import datetime


class Vente:
    def __init__(self, id=None, numero_facture=None, client_id=None, date_vente=None,
                 total_ht=0, tva_total=0, total_ttc=0, type_paiement=None, remise=0):
        self.id = id
        self.numero_facture = numero_facture
        self.client_id = client_id
        self.date_vente = date_vente or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.total_ht = total_ht
        self.tva_total = tva_total
        self.total_ttc = total_ttc
        self.type_paiement = type_paiement
        self.remise = remise
        self.details = []

    def ajouter_detail(self, produit_id, quantite, prix_unitaire):
        self.details.append({
            'produit_id': produit_id,
            'quantite': quantite,
            'prix_unitaire': prix_unitaire
        })
        self.total_ht += quantite * prix_unitaire
        self.tva_total = self.total_ht * 0.2
        self.total_ttc = self.total_ht + self.tva_total

    def appliquer_remise(self, pourcentage):
        self.remise = pourcentage
        self.total_ttc = self.total_ttc * (1 - pourcentage / 100)

    def to_dict(self):
        return {
            'numero_facture': self.numero_facture,
            'client_id': self.client_id,
            'total_ht': self.total_ht,
            'tva_total': self.tva_total,
            'total_ttc': self.total_ttc,
            'type_paiement': self.type_paiement,
            'remise': self.remise
        }