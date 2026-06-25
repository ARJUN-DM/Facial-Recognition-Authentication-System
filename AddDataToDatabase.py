import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from dotenv import load_dotenv

load_dotenv()

cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIALS"))
firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv("FIREBASE_DB_URL")
})

ref = db.reference('Users')

data = {
    "20022":
        {
            "name": "Arjun Das",
            "ph_no": "9757060494",
            "enc_st": "0c1e02ad2d74e7bafea3250c74f5a171c0e5adc80357d3bd59076a7012499d3e"
        }
}

for key, value in data.items():
    ref.child(key).set(value)