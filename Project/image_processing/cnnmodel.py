import tensorflow as tf
import os

from filepaths import modelsDir, trainDir, valDir
from model_definition import SegmentationModel

class CNNModel:
    
    def __init__(self, modelname):
        self.modelname = modelname
        if os.path.exists(modelsDir + self.modelname + ".h5"):
            self.model = tf.keras.models.load_model(modelsDir + self.modelname + ".h5")
        else:
            self.create()
    
    def create(self):
        self.model = SegmentationModel().model
        self.model.summary() # TODO: Remove this Line
        
        self.image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255) # TODO: Remove unwanted method variables
        self.callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss', 
                patience=5, 
                restore_best_weights=True, 
            )
        ]
        self.model.compile(
            optimizer='adam',
            loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
            metrics=['accuracy'],
        )
        
    def train(self, epochs=20):
        train_generator = self.image_generator.flow_from_directory(
            directory=trainDir,
            target_size=(512, 512),
            batch_size=32,
            class_mode='categorical'
        )
        validation_generator = self.image_generator.flow_from_directory(
            directory=valDir,
            target_size=(512, 512),
            batch_size=32,
            class_mode='categorical'
        )
        self.model.fit(
            train_generator,
            validation_data=validation_generator,
            epochs=epochs,
            callbacks=self.callbacks
        )
        
    def predict(self, x):
        return self.model.predict(x)
    
    def save(self):
        self.model.save(modelsDir + self.modelname + ".h5")