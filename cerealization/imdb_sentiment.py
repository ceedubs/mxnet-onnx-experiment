from __future__ import print_function

from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Activation, Dense, Embedding
from keras.layers import LSTM
from keras.datasets import imdb

max_features = 20000
# cut texts after this number of words (among top max_features most common words)
maxlen = 80
batch_size = 32
epochs = 1


def load_data():
    print('Loading data...')
    # 😞 https://stackoverflow.com/questions/55890813/how-to-fix-object-arrays-cannot-be-loaded-when-allow-pickle-false-for-imdb-loa/56062555
    import numpy as np
    # save np.load
    np_load_old = np.load

    # modify the default parameters of np.load
    np.load = lambda *a, **k: np_load_old(*a, allow_pickle=True, **k)

    # call load_data with allow_pickle implicitly set to true
    (x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=max_features)

    # restore np.load for future normal usage
    np.load = np_load_old
    print(len(x_train), 'train sequences')
    print(len(x_test), 'test sequences')

    print('Pad sequences (samples x time)')
    x_train = sequence.pad_sequences(x_train, maxlen=maxlen)
    x_test = sequence.pad_sequences(x_test, maxlen=maxlen)
    print('x_train shape:', x_train.shape)
    print('x_test shape:', x_test.shape)
    return (x_train, y_train), (x_test, y_test)


def build_model(max_features):
    print('Build model...')
    model = Sequential()
    model.add(Embedding(max_features, 128))
    model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(1, activation='sigmoid'))

    # try using different optimizers and different optimizer configs
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model


def train_model(model, x_train, y_train, x_test, y_test):
    print('Train...')
    model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              validation_data=(x_test, y_test))
    score, acc = model.evaluate(x_test, y_test,
                                batch_size=batch_size)
    print('Test score:', score)
    print('Test accuracy:', acc)
    return (score, acc)


def load_data_and_train_model():
    (x_train, y_train), (x_test, y_test) = load_data()
    model = build_model(max_features)
    return (model, train_model(model, x_train, y_train, x_test, y_test))
