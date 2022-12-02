# Import modules

import sys
sys.path.append('../')
from fastapi.middleware.cors import CORSMiddleware

from predictor.predict import predict_by_video_path

from Database.firebase_utils import FirebaseUtils
from urllib.request import Request
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable
from keras.models import load_model

# import utils

# Declaring our FastAPI instance
app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Declare firebase
firebase = FirebaseUtils('firebase-adminsdk.json',
                         'https://robust-cooler-320801-default-rtdb.asia-southeast1.firebasedatabase.app/')


# Defining model for root endpoint
MODEL = load_model('../models/model.h5')


ACCEPTED_PREFIX = ['.mp4', '.avi']


@app.middleware("http")
async def errors_handling(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        return JSONResponse(status_code=500, content={'reason': str(exc)})

# Defining path operation for /name endpoint
# Creating an Endpoint to receive the data
# to make prediction on.



@app.post("/predict/")
async def create_prediction(file: UploadFile):
    suffix = Path(file.filename).suffix
    if (suffix not in ACCEPTED_PREFIX):
        raise HTTPException(
            status_code=400, detail="Only .mp4 or .avi is acceptable")
    result = handle_upload_file(file, errors_handling)  # type: ignore

    # insert to realtime firebase
    # No effect result
    insert_to_firebase(result)
    # Response result json
    return {"prediction": str(result[0])}

def insert_to_firebase(result):
    id = "4"
    init_json = firebase.build_db_unit(id, result[0], result[1])
    firebase.add(id, init_json)

############################################################################################
def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()


def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        upload_file.file.close()
    return tmp_path


def handle_upload_file(
        upload_file: UploadFile, handler: Callable[[Path], None]) -> tuple:
    tmp_path = save_upload_file_tmp(upload_file)
    result = ""
    try:
        print("Loading model ...")
        # Do something with the saved temp file
        result = predict_by_video_path(MODEL, str(tmp_path), limit=30)
        print("OK done--------------------")
    finally:
        tmp_path.unlink()  # Delete the temp file
    return result
