import tensorflow as tf
import os
import json

from filepaths import modelsDir, dataDir
from model_definition import SegmentationModel

class CNNModel:
    
    def __init__(self, modelname, filename, modelkind='simple', image_argumentation=True):
        self.modelkind = modelkind
        self.modelname = modelname
        self.filename = filename
        
        if not os.path.exists(dataDir):
            os.mkdir(dataDir)
        if not os.path.exists(modelsDir):
            os.mkdir(modelsDir)
        if not os.path.exists(dataDir + self.modelname):
            os.mkdir(dataDir + self.modelname)
        if not os.path.exists(modelsDir + self.modelname):
            os.mkdir(modelsDir + self.modelname)
        
        if image_argumentation:
            self.image_generator = tf.keras.preprocessing.image.ImageDataGenerator(
                rescale=1/255,
                validation_split=0.2,
                rotation_range=30,
                horizontal_flip=True,
                brightness_range=[0.6,1.0],
                zoom_range=[0.7,1.0],
            )
        else:
            self.image_generator = tf.keras.preprocessing.image.ImageDataGenerator(
                rescale=1/255,
                validation_split=0.2,
            )
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
        
        if os.path.exists(modelsDir + modelname + "/" + filename):
            print("Loading model from file")
            self.model = tf.keras.models.load_model(modelsDir + modelname + "/" + filename)
            if os.path.exists(modelsDir + modelname + "/" + filename[:-3] + '_history.json'):
                self.history = json.load(open(modelsDir + modelname + "/" + filename[:-3] + '_history.json'))
        elif os.path.exists(modelsDir + modelname + "/" + filename[:-3] + '_checkpoint.h5'):
            print("Loading model from checkpoint")
            self.model = tf.keras.models.load_model(modelsDir + modelname + "/" + filename[:-3] + '_checkpoint.h5')
        else:
            print("Creating new model")
            self.create()
            
    def create(self):
        img_shape = self.train_generator.image_shape
        
        self.model = SegmentationModel(modelkind=self.modelkind, 
                                       input_shape=(img_shape[0], img_shape[1], 3), 
                                       classes=len(self.classes)).model
        
        self.model.compile(
            optimizer='adam',
            loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
            metrics=['accuracy'],
        )
        
    def train(self, epochs=20, callback_patience=5, save_historyname=None):
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=callback_patience,
                restore_best_weights=True,
            ),
            tf.keras.callbacks.ModelCheckpoint(
                modelsDir + self.modelname + "/" + self.filename[:-3]+'_checkpoint.h5', 
                monitor='val_loss', 
                save_best_only=True
            ),
        ]
        self.history = self.model.fit(
            self.train_generator,
            validation_data=self.validation_generator,
            epochs=epochs,
            callbacks=callbacks
        )
        return self.history
    
    def predict(self, img_bytes):
        img = tf.image.decode_image(img_bytes)
        img = tf.expand_dims(img, axis=0)
        img = tf.image.resize(img, (512, 512))
        predictions = self.model.predict(img)
        dict_obj = {k: float(predictions[0][v]) for k, v in self.classes.items()}
        # print(dict_obj)
        dict_obj['maxlabel'] = max(dict_obj, key=dict_obj.get)
        return dict_obj
    
    def save(self, filename=None):
        if not os.path.exists(modelsDir + self.modelname):
            os.mkdir(modelsDir + self.modelname)
        
        if filename:
            self.model.save(modelsDir + self.modelname + "/" + filename)
            with open(modelsDir + self.modelname + "/" + filename[:-3] + '_history.json', 'w') as f:
                json.dump(self.history.history, f)
        else:
            self.model.save(modelsDir + self.modelname + "/" + self.filename)
            with open(modelsDir + self.modelname + "/" + self.filename[:-3] + '_history.json', 'w') as f:
                json.dump(self.history.history, f)
