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


if __name__ == "__main__":
    app.run(debug=True)
