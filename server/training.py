from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from tensorflow import keras
from tick_tack_toy import gameStats, getWinner, movesToBoard
from tick_tack_player_nn_model import getModel, gamesToWinLossData, simulateGame, bestMove


def getModelNext():
    model = keras.Sequential()
    model.add(keras.layers.Dense(
        units=9, kernel_initializer='uniform', activation='relu', input_dim=18))
    model.add(keras.layers.Dense(
        units=9, kernel_initializer='uniform', activation='relu'))
    model.add(keras.layers.Dense(
        units=1, kernel_initializer='uniform', activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model


# model = getModelNext()

# games = [simulateGame() for _ in range(10)]
# print(games)
# X_train, X_test, y_train, y_test = gamesToWinLossData(games)
# print("X_train", X_train)
# print("X_test", X_test)
# print("y_train", y_train)
# print("y_test", y_test)

# some = model.fit(X_train, y_train, validation_data=(
#     X_test, y_test), epochs=100, batch_size=100)

# model.save('my_model_v1_sparse.h5')
# games = [[(1, (0, 0)), (2, (1, 1)), (1, (0, 1)), (2, (2, 0)), (1, (0, 2))], [(1, (1, 1)), (2, (0, 0)), (1, (1, 2)), (2, (1, 0)), (1, (0, 2)), (2, (2, 0))], [(1, (1, 1)), (2, (0, 0)), (1, (0, 2)), (2, (2, 0)), (1, (1, 0)), (2, (1, 2)), (1, (0, 1)), (2, (2, 1)), (1, (2, 2))], [(1, (0, 0)), (2, (1, 1)), (1, (0, 1)), (2, (2, 0)), (1, (0, 2))], [(1, (1, 1)), (2, (0, 0)), (1, (0, 1)), (2, (2, 1)), (1, (0, 2)), (2, (2, 0)), (1, (2, 2)), (2, (1, 0))], [(1, (1, 1)), (2, (0, 0)), (1, (0, 2)), (2, (2, 0)), (1, (1, 0)),
#                                                                                                                                                                                                                                                                                                                                                                                                                                                                  (2, (1, 2)), (1, (0, 1)), (2, (2, 1)), (1, (2, 2))], [(1, (0, 0)), (2, (1, 1)), (1, (0, 1)), (2, (2, 0)), (1, (0, 2))], [(1, (0, 0)), (2, (1, 1)), (1, (0, 1)), (2, (2, 0)), (1, (0, 2))], [(1, (0, 0)), (2, (1, 1)), (1, (0, 1)), (2, (2, 0)), (1, (0, 2))], [(1, (0, 0)), (2, (1, 1)), (1, (0, 1)), (2, (2, 0)), (1, (0, 2))], [(1, (0, 0)), (2, (0, 1)), (1, (1, 1)), (2, (2, 2)), (1, (2, 0)), (2, (0, 2)), (1, (1, 0))], [(1, (0, 0)), (2, (0, 1)), (1, (1, 1)), (2, (2, 2)), (1, (2, 0)), (2, (0, 2)), (1, (1, 0))]]
model1 = keras.models.load_model('my_model_v1_next.h5')
model2 = keras.models.load_model('my_model_v1.h5')
games = [simulateGame(x=_, p1=model2, p2=model1) for _ in range(200)]

print("GAMES", games)
gameStats(games, player=1)
print()
gameStats(games, player=2)
# # games = [simulateGame() for _ in range(10)]
# # print(games)
X_train, X_test, y_train, y_test = gamesToWinLossData(games)
print("X_train", X_train)
print("X_test", X_test)
print("y_train", y_train)
print("y_test", y_test)

some = model1.fit(X_train, y_train, validation_data=(
    X_test, y_test), epochs=100, batch_size=100)

model1.save('my_model_v4_next.h5')


# model = getModel()
# X_train, X_test, y_train, y_test = gamesToWinLossData(games)
# history = model.fit(X_train, y_train, validation_data=(
#     X_test, y_test), epochs=100, batch_size=100)

# model.save('my_model_v1.h5')

# model = keras.models.load_model('my_model_v1.h5')

# games = [simulateGame(x=_, p1=model, p2=model) for _ in range(10)]
# print("GAMES", games)
# gameStats(games, player=1)
# print()
# gameStats(games, player=2)

# X_train, X_test, y_train, y_test = gamesToWinLossData(games)
# print('X_train', X_train)
# print('X_test', X_test)
# print('y_train', y_train)
# print('y_test', y_test)

# game = [(1, (1, 1)), (2, (2, 2)), (1, (1, 0)), (2, (1, 2)),
#         (1, (0, 2)), (2, (0, 1)), (1, (2, 0)), (2, (0, 0)), (1, (2, 1))]
# board = movesToBoard(game)
# print('BOARD', board)
# winner = getWinner(board)
# print('WINNER', winner)
# history = model.fit(X_train, y_train, validation_data=(
#     X_test, y_test), epochs=100, batch_size=100)

# model.save('my_model_next.h5')


# def convert(list):
#     return tuple(i for i in list)


# # list = [1, [3, 4]]
# arr = [[1, [3, 4]], [1, [3, 4]]]
# # my_tuple = (list[0], tuple(list[1]))
# # print(my_tuple)
# result = list(map(lambda x: tuple([x[0], tuple(x[1])]), arr))
# print("result", result)
