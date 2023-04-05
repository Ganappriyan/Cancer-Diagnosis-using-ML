import tensorflow as tf
import os
import json

from filepaths import modelsDir, dataDir
from model_definition import SegmentationModel

class CNNModel:
    
    def __init__(self, modelname, filename, modelkind='simple'):
        self.modelkind = modelkind
        self.modelname = modelname
        self.filename = filename
        self.image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255, validation_split=0.2)
        self.callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=5,
                restore_best_weights=True,
            )
        ]
        self.train_generator = self.image_generator.flow_from_directory(
            directory=dataDir+self.modelname+"/",
            target_size=(512, 512),
            batch_size=32,
            class_mode='categorical',
            subset='training',
        )
        self.validation_generator = self.image_generator.flow_from_directory(
            directory=dataDir+self.modelname+"/",
            target_size=(512, 512),
            batch_size=32,
            class_mode='categorical',
            subset='validation',
        )
        self.classes = self.train_generator.class_indices
        print("Classes: " + str(self.classes)) # TODO: Remove this print
        
        if os.path.exists(modelsDir + modelname + "/" + filename):
            print("Loading model: " + filename) # TODO: Remove this print
            self.model = tf.keras.models.load_model(modelsDir + modelname + "/" + filename)
        else:
            print("Creating new model") # TODO: Remove this print
            self.create()
            
    def create(self):
        if not os.path.exists(dataDir + self.modelname):
            os.mkdir(dataDir + self.modelname)
        if not os.path.exists(modelsDir + self.modelname):
            os.mkdir(modelsDir + self.modelname)
        
        img_shape = self.train_generator.image_shape
        print("Image shape: " + str(img_shape)) # TODO: Remove this print
        
        self.model = SegmentationModel(modelname=self.modelkind, 
                                       input_shape=(img_shape[0], img_shape[1], 3), 
                                       classes=len(self.classes)).model
        
        self.model.compile(
            optimizer='adam',
            loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
            metrics=['accuracy'],
        )
        
    def train(self, epochs=20):
        self.model.fit(
            self.train_generator,
            validation_data=self.validation_generator,
            epochs=epochs,
            callbacks=self.callbacks
        )
    
    def predict(self, img_bytes):
        img = tf.image.decode_image(img_bytes)
        img = tf.expand_dims(img, axis=0)
        img = tf.image.resize(img, (512, 512))
        predictions = self.model.predict(img)
        return {k: float(predictions[0][v]) for k, v in self.classes.items()}
    
    def save(self, filename=None):
        if not os.path.exists(modelsDir + self.modelname):
            os.mkdir(modelsDir + self.modelname)
        
        if filename:
            self.model.save(modelsDir + self.modelname + "/" + filename)
        self.model.save(modelsDir + self.modelname + "/" + self.filename)
