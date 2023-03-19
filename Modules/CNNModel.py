import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os

from enum import Enum

class CancerType(Enum):
    DYSKERATOTIC = 'Dyskeratotic'
    KOILOCYTOTIC = 'Koilocytic'
    METAPLASTIC = 'Metaplastic'
    PARABASAL = 'Parabasal'
    SUPERFICIALINTERMEDIATE = 'Superficial-Intermediate'

class ModelType(Enum):
    CLASSIFICATION = 'Classification'
    DETECTION = 'Detection'

class CNNModel:    
    
    def __init__(self, model_path: str, dataset_path: str) -> None:
        self.dataset_path = dataset_path
        self.model = tf.keras.models.load_model(model_path)
        self.image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255)
        self.callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss', 
                patience=5, 
                restore_best_weights=True, 
            )
        ]
    
    def load_training_data(self) -> None:
        self.train_dataset = self.image_generator.flow_from_directory(
            batch_size=32, 
            directory=self.dataset_path+'/Training', 
            shuffle=True, 
            target_size=(512,512), 
            subset='training', 
            class_mode='categorical'
        )
    
    def load_validation_data(self) -> None:
        self.validation_dataset = self.image_generator.flow_from_directory(
            batch_size=32, 
            directory=self.dataset_path+'/Validation', 
            shuffle=True, 
            target_size=(512,512), 
            class_mode='categorical'
        )
    
    def load_dataset(self) -> None:
        self.load_training_data()
        self.load_validation_data()
    
    def train_model(self, epochs: int=30) -> None:
        self.model.fit(
            self.train_dataset, 
            validation_data = self.validation_dataset, 
            epochs = epochs, 
            callbacks = self.callbacks, 
        )
    
    def save_model(self, model_type: ModelType) -> None:
        model_name = f'{model_type.lower()}_modelv{len(os.listdir(path=f"Model/{model_type}"))+1}.h5'
        self.model.save(f'Model/{model_type}/{model_name}')
        
    def predict(self, img_path: str) -> CancerType:
        img = image.load_img(img_path, target_size=(512,512))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        images = np.vstack([x])
        classes = self.model.predict(images, batch_size=10)
        print(classes)
        print(np.argmax(classes))
        return CancerType(np.argmax(classes))
    