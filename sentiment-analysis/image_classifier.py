# sentiment-analysis/image_classifier.py (Final, Corrected Version)

import os
import numpy as np
import base64
import io
import logging

from tensorflow.keras.models import Sequential, load_model # type: ignore
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout # type: ignore
from tensorflow.keras.optimizers import Adam # type: ignore
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array # type: ignore

class ImageClassifier:
    def __init__(self, data_dir, img_width=100, img_height=100, batch_size=32, epochs=10):
        self.data_dir = data_dir
        self.train_dir = os.path.join(data_dir, 'train')
        self.img_width = img_width
        self.img_height = img_height
        self.batch_size = batch_size
        self.epochs = epochs
        self.model = None
        self.class_indices = {}
        self.labels_from_index = {}

    def _build_model(self, num_classes):
        # MERGED: Using your more robust model architecture
        self.model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(self.img_width, self.img_height, 3)),
            MaxPooling2D(2, 2),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D(2, 2),
            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D(2, 2),
            Flatten(),
            Dense(512, activation='relu'),
            Dropout(0.5), # Dropout is great for preventing overfitting
            Dense(num_classes, activation='softmax')
        ])
        self.model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])
        print("✅ Model built successfully.")

    def train(self):
        # MERGED: Using your more robust data augmentation
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=40,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest'
        )
        train_generator = train_datagen.flow_from_directory(
            self.train_dir,
            target_size=(self.img_width, self.img_height),
            batch_size=self.batch_size,
            class_mode='categorical'
        )
        self.class_indices = train_generator.class_indices
        self.labels_from_index = {v: k for k, v in self.class_indices.items()} # Create the reverse map

        num_classes = len(self.class_indices)
        self._build_model(num_classes)
        
        print("Starting model training...")
        self.model.fit(
            train_generator,
            steps_per_epoch=train_generator.samples // self.batch_size,
            epochs=self.epochs
        )
        print("✅ Model training complete.")

    def load_existing_model(self, model_path):
        # NEW: Method to load a pre-trained model and set up class labels
        self.model = load_model(model_path)
        # We must still determine the class indices from the directory structure
        # to ensure predictions are mapped to the correct labels.
        try:
            train_datagen = ImageDataGenerator(rescale=1./255)
            train_generator = train_datagen.flow_from_directory(
                self.train_dir,
                target_size=(self.img_width, self.img_height),
                class_mode='categorical',
                shuffle=False # No need to shuffle when just getting labels
            )
            self.class_indices = train_generator.class_indices
            self.labels_from_index = {v: k for k, v in self.class_indices.items()}
            print("✅ Class labels loaded and mapped successfully.")
        except Exception as e:
            logging.error(f"Failed to load class indices from directory: {e}")
            raise

    def predict_from_base64(self, base64_string):
        # NEW: Method to predict from a base64 string, as required by the API
        if "base64," in base64_string:
            base64_string = base64_string.split("base64,")[1]
        
        img_data = base64.b64decode(base64_string)
        img = load_img(io.BytesIO(img_data), target_size=(self.img_width, self.img_height))
        img_array = img_to_array(img) / 255.0
        img_batch = np.expand_dims(img_array, axis=0)
        
        predictions = self.model.predict(img_batch)[0]
        predicted_index = np.argmax(predictions)
        confidence = float(predictions[predicted_index])
        
        # Use the reverse map for a safe lookup
        predicted_label = self.labels_from_index[predicted_index]
        
        return predicted_label, confidence
   