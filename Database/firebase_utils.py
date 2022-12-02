import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime

class FirebaseUtils():
    def __init__(self, credential: str, db_url):
        self.__cred = credentials.Certificate(credential)
        self.__app = firebase_admin.initialize_app(self.__cred, {
            'databaseURL': db_url
        })
        self.ref = db.reference("data")

    # fix push
    def add(self, data):
        self.ref.push().set(data)

    def update(self, id, data):
        self.ref.child(id).update(data)

    def remove(self, id):
        self.ref.child(id).delete()

    def read(self, id):
        return self.ref.child(id).get()

    def get_all(self):
        return self.ref.get()

    def build_db_unit(self, predict, prob):
        # using now() to get current time
        now = datetime.now()
        
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        
        pre_json_object = {
            "prediction": str(predict),
            "time": dt_string,
            "prob": str(prob)
        }
        return pre_json_object
