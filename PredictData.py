import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

from enum import Enum

class CancerType(Enum):
    DYSKERATOTIC = 0
    KOILOCYTOTIC = 1
    METAPLASTIC = 2
    PARABASAL = 3
    SUPERFICIALINTERMEDIAT = 4

class PredictData:
    def __init__(self) -> None:
        self.model = tf.keras.models.load_model('Model/modelc.h5')
        
    def predict(self, img) -> CancerType:
        img = image.load_img(img, target_size=(512,512))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        images = np.vstack([x])
        classes = self.model.predict(images, batch_size=10)
        print(classes)
        print(np.argmax(classes))
        return CancerType(np.argmax(classes))
