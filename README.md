Based on this example:

[https://github.com/tensorflow/hub/tree/master/tensorflow_hub/tools/make_image_classifier](https://github.com/tensorflow/hub/tree/master/tensorflow_hub/tools/make_image_classifier)

To install dependencies:

```
pip install "tensorflow~=2.0"
pip install "tensorflow-hub[make_image_classifier]~=0.6"
```

To download training data:

```
curl http://download.tensorflow.org/example_images/flower_photos.tgz -O
```

To train the classifier:

```
make_image_classifier   --image_dir flower_photos   --tfhub_module https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4   --image_size 224   --saved_model_dir model   --labels_output_file class_labels.txt   --tflite_output_file new_mobile_model.tflite
```

Then the file [https://github.com/amaurs/flowers/blob/master/backend/classifier.py](https://github.com/amaurs/flowers/blob/master/backend/classifier.py) was written inspired in [https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/examples/python/label_image.py](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/examples/python/label_image.py)


With the classifier in place I built a simple backend with [chalice](https://chalice.readthedocs.io/en/latest/). It creates an instance of the classifier and keeps it in memory for inference to start it:

```
cd backend
pip install -r requirements.txt
chalice local
```


It will start listening in `http://127.0.0.1:8000`.


Once the server is up and running you can run the client:

```
cd frontend
npm install
npm start
```

It will start running in `http://localhost:3000/` and launch a broswer automatically. You can use one of the images to test.





