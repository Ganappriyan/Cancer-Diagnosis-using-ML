import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense

class SegmentationModel(): 
    
    def __init__(self, modelkind, input_shape, classes):
        self.input_shape = input_shape
        self.classes = classes
        if modelkind == "simple":
            self.simple()
        if modelkind == "alexnet":
            self.alexnet()
        if modelkind == "lenet":
            self.lenet()
    
    def simple(self):
        inputData = Input(shape=self.input_shape)
        X = Conv2D(16, (3, 3), activation='relu')(inputData)
        X = MaxPooling2D((2, 2))(X)
        X = Conv2D(32, (3, 3), activation='relu')(X)
        X = MaxPooling2D((2, 2))(X)
        X = Conv2D(64, (3, 3), activation='relu')(X)
        X = MaxPooling2D((2, 2))(X)
        X = Flatten()(X)
        X = Dense(256, activation='relu')(X)
        X = Dense(self.classes, activation=None)(X)
        
        SegmentationModel.model = Model(inputs=inputData, outputs=X)
    
    def alexnet(self):
        inputData = Input(shape=self.input_shape)
        X = Conv2D(96, (11, 11), strides=(4, 4), activation='relu')(inputData)
        X = MaxPooling2D((3, 3), strides=(2, 2))(X)
        X = Conv2D(256, (5, 5), strides=(1, 1), activation='relu')(X)
        X = MaxPooling2D((3, 3), strides=(2, 2))(X)
        X = Conv2D(384, (3, 3), strides=(1, 1), activation='relu')(X)
        X = Conv2D(384, (3, 3), strides=(1, 1), activation='relu')(X)
        X = Conv2D(256, (3, 3), strides=(1, 1), activation='relu')(X)
        X = MaxPooling2D((3, 3), strides=(2, 2))(X)
        X = Flatten()(X)
        X = Dense(4096, activation='relu')(X)
        X = Dense(4096, activation='relu')(X)
        X = Dense(self.classes, activation='softmax')(X)
        
        SegmentationModel.model = Model(inputs=inputData, outputs=X)
    
    def lenet(self):
        inputData = Input(shape=self.input_shape)
        X = Conv2D(6, (5, 5), strides=(1, 1), activation='relu')(inputData)
        X = MaxPooling2D((2, 2), strides=(2, 2))(X)
        X = Conv2D(16, (5, 5), strides=(1, 1), activation='relu')(X)
        X = MaxPooling2D((2, 2), strides=(2, 2))(X)
        X = Flatten()(X)
        X = Dense(120, activation='relu')(X)
        X = Dense(84, activation='relu')(X)
        X = Dense(self.classes, activation='softmax')(X)
        
        SegmentationModel.model = Model(inputs=inputData, outputs=X)