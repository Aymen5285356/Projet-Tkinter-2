# config.py
import os

BG_MAIN = "#F2F2F2"
BG_SECTION = "#FFFFFF"
TEXT_PRIMARY = "#333333"
TEXT_SECONDARY = "#555555"
BORDER = "#DDDDDD"
BTN_PRIMARY_BG = "#2E86C1"
BTN_DANGER_BG = "#C0392B"
BTN_SUCCESS_BG = "#27AE60"
BTN_WARNING_BG = "#F39C12"
BTN_TEXT = "#FFFFFF"
BTN_HOVER = "#2874A6"
TABLE_HOVER = "#D6EAF8"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DB_PATH = os.path.join(BASE_DIR, "pharmacie.db")
LOG_PATH = os.path.join(BASE_DIR, "logs.txt")

TVA = 20
SEUIL_ALERTE_STOCK = 10
DUREE_ALERTE_EXPIRATION = 30