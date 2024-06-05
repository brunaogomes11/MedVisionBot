import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

import tensorflow as tf
import numpy as np

from PIL import Image
from io import BytesIO


class KneeXRayClassifier():
    def __init__(self, model_path="./app/models/KneeXRayClassifier/best.h5"):
        super().__init__()

        self.model = tf.keras.models.load_model(model_path)

        self.class_names = {
            0: "Anormal",
            1: "Normal"
        }
        

    def transforms(self, x):
        image = Image.open(BytesIO(x)).convert('RGB').resize((64, 64))
        
        # Loading as numpy array
        image_array = np.asarray(image)

        # If the image has 4 color channels
        if image_array.shape[-1] == 4:
            image_array = image_array[:, :, :3]
        # If the image is grayscale, convert to RGB
        elif len(image_array.shape) == 2:
            image_array = np.expand_dims(image_array, axis=-1)
            image_array = np.concatenate([image_array] * 3, axis=-1)

        image_array = image_array / 255.0
        image_array = np.expand_dims(image_array, axis=0)

        return image_array
    

    def forward(self, x):
        image_array = self.transforms(x)

        return self.model.predict(image_array, verbose=0)
    

if __name__ == "__main__":
    net = KneeXRayClassifier()