import firebase_admin
from firebase_admin import credentials, db, firestore

cred = credentials.Certificate("proyecto-pagina-web.json")
firebase_admin.initialize_app(cred,{"databaseURL" : "https://proyecto-pagina-web-9d1c0-default-rtdb.firebaseio.com/"
})
db = firestore.client()

