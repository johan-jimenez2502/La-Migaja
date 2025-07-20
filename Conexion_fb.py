
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("proyecto-pagina-web.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
