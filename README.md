# onnx2mx issue reproduction

This repository reproduces an issue encountered when using `onnx2mx` to import an ONNX model that was originally trained via keras and converted to ONNX format via `keras2onnx`. The problem does not appear to be in the keras to ONNX conversion, because the same onnx file can be loaded and run via `onnxruntime` without issue.

The error encountered is:

```
Traceback (most recent call last):
  File "cerealization/model-to-onnx.py", line 49, in <module>
    sym, arg, aux = mxnet_model = onnx_mxnet.import_model(onnx_file)
  File "/some-path/mxnet-onnx-experiment/venv/lib/python3.6/site-packages/mxnet/contrib/onnx/onnx2mx/import_model.py", line 59, in import_model
    sym, arg_params, aux_params = graph.from_onnx(model_proto.graph)
  File "/some-path/mxnet-onnx-experiment/venv/lib/python3.6/site-packages/mxnet/contrib/onnx/onnx2mx/import_onnx.py", line 115, in from_onnx
    inputs = [self._nodes[i] for i in node.input]
  File "/some-path/mxnet-onnx-experiment/venv/lib/python3.6/site-packages/mxnet/contrib/onnx/onnx2mx/import_onnx.py", line 115, in <listcomp>
    inputs = [self._nodes[i] for i in node.input]
KeyError: 'dense_1/Sigmoid:01'
```

Calling `keras_model.outputs` returns `[<tf.Tensor 'dense_1/Sigmoid:0' shape=(?, 1) dtype=float32>]`. There seems to be a discrepancy between `Sigmoid:01` in the error message and `Sigmoid:0` in the keras output; I'm not sure whether that is part of the issue.

## model

The model is in [cerealization/imdb_sentiment.py](cerealization/imdb_sentiment.py). It is taken almost exactly from the [imdb_lstm.py example](https://github.com/keras-team/keras/blob/master/examples/imdb_lstm.py) from the [keras-team/keras](https://github.com/keras-team/keras) repo. It has been changed slightly to be broken into functions and to work around a numpy compatibility issue.

## model conversion

The model conversion code is in [cerealization/model-to-onnx.py](cerealization/model-to-onnx.py). This is the code that produces the error.

## dependencies

This repo includes a `shell.nix`, so if you use Nix, you can simply run `nix-shell` to drop into a shell with all of the necessary dependencies. Otherwise, you can use your Python (3.6/3.7) environment of choice and `pip install -r requirements.txt` (or equivalent).

## running the code

```sh
python cerealization/model-to-onnx.py
```
