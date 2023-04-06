from fastapi import FastAPI, File, UploadFile
from cnnmodel import CNNModel
import json

app = FastAPI()

classification_model = CNNModel(modelname="classification", filename="simple_noarg.h5")
grading_model = CNNModel(modelname="grade", filename="simple_noarg.h5")

@app.post("/process/")
async def classify_image(file: UploadFile = File(...)):
    img_bytes = await file.read()
    return {'classification': classification_model.predict(img_bytes), 
            'grading': grading_model.predict(img_bytes),}

@app.post("/classify/")
async def classify_image(file: UploadFile = File(...)):
    return classification_model.predict(file.file)

@app.post("/grade/")
async def grade_images(file: UploadFile = File(...)):
    img_bytes = await file.read()
    return grading_model.predict(img_bytes)
    