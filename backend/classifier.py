import numpy as np


import tensorflow as tf # TF2


import base64
from PIL import Image
from io import BytesIO


class FlowerClassifier:

    _instance = None

    def __init__(self, model_file, label_file, mean, std):

        self.interpreter = tf.lite.Interpreter(model_path=model_file)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.floating_model = self.input_details[0]['dtype'] == np.float32
        self.input_mean = mean
        self.input_std = std
        self.labels = FlowerClassifier.load_labels(label_file)

    @classmethod
    def instance(cls):
        if cls._instance == None:
            print("loading")
            cls._instance = FlowerClassifier("new_mobile_model.tflite", "class_labels.txt", 0, 255)
        return cls._instance

    @staticmethod
    def load_labels(filename):
        with open(filename, 'r') as f:
            return [line.strip() for line in f.readlines()]

    def invoke(self, data):

        height = self.input_details[0]['shape'][1]
        width = self.input_details[0]['shape'][2]

        img = Image.open(BytesIO(base64.b64decode(data))).resize((width, height))

        input_data = np.expand_dims(img, axis=0)

        if self.floating_model:
            input_data = (np.float32(input_data) - self.input_mean) / self.input_std

        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)

        self.interpreter.invoke()

        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        results = np.squeeze(output_data)

        top_k = results.argsort()[-5:][::-1]
        
        return [{"label": self.labels[i], "score": float(results[i])} for i in top_k]

