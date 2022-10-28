import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime

class FirebaseUtils():
    def __init__(self, credential, db_url):
        self.__cred = credentials.Certificate(f'../{credential}')
        self.__app = firebase_admin.initialize_app(self.__cred, {
            'databaseURL': db_url
        })
        self.ref = db.reference("data")

    def add(self, id, data):
        self.ref.child(id).set(data)

    def update(self, id, data):
        self.ref.child(id).update(data)

    def remove(self, id):
        self.ref.child(id).delete()

    def read(self, id):
        return self.ref.child(id).get()

    def get_all(self):
        return self.ref.get()

    def build_db_unit(self, st, predict, prob):
        # using now() to get current time
        pre_json_object = {
            "id": str(st),
            "prediction": str(predict),
            "time": str(datetime.datetime.now()),
            "prob": str(prob)
        }
        return pre_json_object

if __name__ == "__main__":

    firebase = FirebaseUtils('firebase-adminsdk.json', 'https://robust-cooler-320801-default-rtdb.asia-southeast1.firebasedatabase.app/')

    data0 = {"id": 0, "prediction": "1",
            "time": "2022-07-29T19:30:03.283Z", "prob": "0.95"}
    data1 = {"id": 1, "prediction": "0",
            "time": "2022-07-30T19:30:03.283Z", "prob": "0.45"}
    data2 = {"id": 2, "prediction": "0",
            "time": "2022-07-31T19:30:03.283Z", "prob": "0.35"}
    data3 = {"id": 3, "prediction": "1",
            "time": "2022-08-01T19:30:03.283Z", "prob": "0.96"}
    #init_json = firebase.build_db_unit(st=1, predict=True, prob=0.956)
    #firebase.add("1", data=init_json)
# create
# add("1",data1)

# update
# update("2",data3)

# delete
# remove("1")

# read
# read("1")

# read full
# print(ref.get())
