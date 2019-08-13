import keras
import onnx
import os
import mxnet.contrib.onnx as onnx_mxnet
import keras2onnx
# import onnxmltools
import imdb_sentiment
import onnxruntime
import numpy

trained_models_dir = "trained-models"

if not os.path.exists(trained_models_dir):
    os.makedirs(trained_models_dir)

keras_file = f"{trained_models_dir}/imdb-keras-model.h5"
onnx_file = f"{trained_models_dir}/imdb-onnx-model.onnx"

((x_train, y_train), (x_test, y_test)) = imdb_sentiment.load_data()

# toggle comments on below lines to switch between training and loading model
(keras_model, (score, acc)) = imdb_sentiment.load_data_and_train_model()
keras_model.save(keras_file)

# keras_model = keras.models.load_model(keras_file)

keras_model.summary()
print("inputs: ", keras_model.inputs)
print("outputs: ", keras_model.outputs)

# I saw the same failure using keras2onnx directly or using onnxmltools
# onnx_model = onnxmltools.convert_keras(keras_model)

onnx_model = keras2onnx.convert_keras(keras_model)

sess_content = onnx_model.SerializeToString()
sess = onnxruntime.InferenceSession(sess_content)

input_name = sess.get_inputs()[0].name
label_name = sess.get_outputs()[0].name
pred_onnx = sess.run([label_name], {input_name: x_test.astype(numpy.float32)})

# this works fine
print("first prediction from onnx rumtime: ", pred_onnx[0][0])

onnx.save_model(onnx_model, onnx_file)

# this fails with KeyError: 'activation_1/Sigmoid:01'
sym, arg, aux = mxnet_model = onnx_mxnet.import_model(onnx_file)
