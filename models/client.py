# models/client.py
class Client:
    def __init__(self, id=None, nom=None, telephone=None, email=None, adresse=None, points_fidelite=0,
                 date_inscription=None):
        self.id = id
        self.nom = nom
        self.telephone = telephone
        self.email = email
        self.adresse = adresse
        self.points_fidelite = points_fidelite
        self.date_inscription = date_inscription

    def to_dict(self):
        return {
            'nom': self.nom,
            'telephone': self.telephone,
            'email': self.email,
            'adresse': self.adresse
        }

    def ajouter_points(self, points):
        self.points_fidelite += points

    def utiliser_points(self, points):
        if points <= self.points_fidelite:
            self.points_fidelite -= points
            return True
        return False