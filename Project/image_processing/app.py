from fastapi import FastAPI, File
from typing import List
from cnnmodel import CNNModel

app = FastAPI()

classification_model = CNNModel(modelname="classification", filename="lenet.h5")
grading_model = CNNModel(modelname="grade", filename="simple_nosoftmax.h5")

@app.post("/classification/")
def classify_image(file: bytes = File(...)):
    filename = "temp.jpg"
    with open(filename, 'wb') as f:
        f.write(file)
    predictions = classification_model.predict(filename)
    print(predictions)
    return predictions

@app.post("/grading/")
def grade_images(file: bytes = File(...)):
    
    filename = "temp.jpg"
    with open(filename, 'wb') as f:
        f.write(file)
    predictions = grading_model.predict(filename)
    print(predictions)
    return predictions
