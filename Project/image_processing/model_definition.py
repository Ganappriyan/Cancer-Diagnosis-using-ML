import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense

class SegmentationModel(): 
    
    def __init__(self): 
        inputData = Input(shape=(512, 512, 3))
        X = Conv2D(16, 3, activation='relu', padding='same')(inputData)
        X = Conv2D(16, 3, activation='relu', padding='same')(X)
        X = MaxPooling2D(3)(X)
        
        X = Conv2D(32, 3, activation='relu', padding='same')(X)
        X = Conv2D(32, 3, activation='relu', padding='same')(X)
        X = MaxPooling2D(3)(X)
        
        X = Conv2D(64, 3, activation='relu', padding='same')(X)
        X = Conv2D(64, 3, activation='relu', padding='same')(X)
        X = MaxPooling2D(3)(X)
        
        X = Conv2D(32, 3, activation='relu', padding='same')(X)
        X = Conv2D(32, 3, activation='relu', padding='same')(X)
        X = MaxPooling2D(3)(X)
        
        X = Flatten()(X)
        
        X = Dense(256, activation='relu')(X)
        X = Dense(128, activation='relu')(X)
        X = Dense(5, activation='relu')(X)

        SegmentationModel.model = Model(inputs=inputData, outputs=X)
        