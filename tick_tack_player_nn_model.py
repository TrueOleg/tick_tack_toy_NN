import tensorflow as tf
import numpy as np
from tensorflow import keras
from tick_tack_toy import getWinner, movesToBoard


def getModel():
    numCells = 9
    outcomes = 3
    model = keras.Sequential()
    model.add(keras.layers.Dense(200, activation='relu', input_shape=(9, )))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Dense(125, activation='relu'))
    model.add(keras.layers.Dense(75, activation='relu'))
    model.add(keras.layers.Dropout(0.1))
    model.add(keras.layers.Dense(25, activation='relu'))
    model.add(keras.layers.Dense(outcomes, activation='softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop', metrics=['acc'])
    return model


def gamesToWinLossData(games):
    X = []
    y = []
    for game in games:
        winner = getWinner(movesToBoard(game))
        for move in range(len(game)):
            X.append(movesToBoard(game[:(move + 1)]))
            y.append(winner)

    X = np.array(X).reshape((-1, 9))
    y = keras.utils.to_categorical(y)

    # Return an appropriate train/test split
    trainNum = int(len(X) * 0.8)
    return (X[:trainNum], X[trainNum:], y[:trainNum], y[trainNum:])
