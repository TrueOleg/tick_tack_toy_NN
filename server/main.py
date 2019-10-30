from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from tensorflow import keras
from tick_tack_toy import gameStats
from tick_tack_player_nn_model import getModel, gamesToWinLossData, simulateGame, bestMove

model = keras.models.load_model('my_model_v1.h5')
games = []

app = Flask(__name__)
CORS(app)


@app.route('/nn_move', methods=['POST'])
def nn_move():
    data = request.get_json(force=True)
    print(data)
    move = bestMove(data, model, 2, 0)
    print("MOVE", move)
    return jsonify(move)


@app.route('/history', methods=['POST'])
def history():
    data = request.get_json(force=True)
    print("=================", data)
    result = list(map(lambda x: tuple([x[0], tuple(x[1])]), data))
    print("=================", result)
    games.append(result)
    print("+++++games", games)
    # X_train, X_test, y_train, y_test = gamesToWinLossData(games)
    # print("X_train", X_train)
    # print("X_test", X_test)
    # print("y_train", y_train)
    # print("y_test", y_test)

    # some = model.fit(X_train, y_train, validation_data=(
    #     X_test, y_test), epochs=100, batch_size=100)

    # model.save('my_model_v1_sparse.h5')
    return 'OK'


if __name__ == "__main__":
    app.run(debug=True)
