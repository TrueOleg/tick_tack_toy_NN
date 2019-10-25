from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from tensorflow import keras
from tick_tack_toy import gameStats
from tick_tack_player_nn_model import getModel, gamesToWinLossData, simulateGame, bestMove

# model = keras.models.load_model('my_model.h5')

# games = [simulateGame(x=_, p1=model, p2=model, rnd=0.6) for _ in range(10)]
# print("GAMES", games)
# gameStats(games, player=1)
# print()
# gameStats(games, player=2)

# X_train, X_test, y_train, y_test = gamesToWinLossData(games)
# history = model.fit(X_train, y_train, validation_data=(
#     X_test, y_test), epochs=100, batch_size=100)

# model.save('my_model_next.h5')


# def convert(list):
#     return tuple(i for i in list)


# list = [1, [3, 4]]
arr = [[1, [3, 4]], [1, [3, 4]]]
# my_tuple = (list[0], tuple(list[1]))
# print(my_tuple)
result = list(map(lambda x: tuple([x[0], tuple(x[1])]), arr))
print("result", result)
