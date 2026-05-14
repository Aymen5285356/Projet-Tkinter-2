# models/utilisateur.py
class Utilisateur:
    def __init__(self, id=None, username=None, password=None, role=None, nom_complet=None, date_creation=None):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
        self.nom_complet = nom_complet
        self.date_creation = date_creation

    def est_admin(self):
        return self.role == 'admin'

    def est_pharmacien(self):
        return self.role in ['admin', 'pharmacien']

    def peut_modifier_stock(self):
        return self.role in ['admin', 'pharmacien']

    def peut_supprimer(self):
        return self.role == 'admin'