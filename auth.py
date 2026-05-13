# auth.py
import hashlib
import secrets

class AuthSystem:
    def __init__(self, db):
        self.db = db
        self.current_user = None

    def hash_password(self, password):
        salt = secrets.token_hex(16)
        hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}${hash_obj.hex()}"

    def verify_password(self, stored, provided):
        try:
            salt, hash_val = stored.split('$')
            hash_obj = hashlib.pbkdf2_hmac('sha256', provided.encode(), salt.encode(), 100000)
            return hash_obj.hex() == hash_val
        except:
            return False

    def login(self, username, password):
        user = self.db.get_utilisateur(username)
        if user and self.verify_password(user[2], password):
            self.current_user = user
            self.db.ajouter_log(user[0], "Connexion", f"Utilisateur {username} connecté")
            return True
        return False

    def logout(self):
        if self.current_user:
            self.db.ajouter_log(self.current_user[0], "Déconnexion", f"Utilisateur {self.current_user[1]} déconnecté")
            self.current_user = None

    def has_permission(self, required_role):
        if not self.current_user:
            return False
        roles = {'admin': 3, 'pharmacien': 2, 'stagiaire': 1}
        return roles.get(self.current_user[3], 0) >= roles.get(required_role, 0)