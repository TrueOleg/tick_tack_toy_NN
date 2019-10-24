from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from tensorflow import keras
from tick_tack_toy import gameStats
from tick_tack_player_nn_model import getModel, gamesToWinLossData, simulateGame, bestMove

# games = [simulateGame() for _ in range(10000)]

# model = getModel()
# X_train, X_test, y_train, y_test = gamesToWinLossData(games)
# history = model.fit(X_train, y_train, validation_data=(
#     X_test, y_test), epochs=100, batch_size=100)

# model.save('my_model.h5')

model = keras.models.load_model('my_model.h5')

# model.summary()

# games2 = [simulateGame(x=_, p1=model) for _ in range(10)]

# gameStats(games2)

# games4 = [simulateGame(x=_, p1=model, p2=model, rnd=0.6) for _ in range(1)]
# gameStats(games4, player=1)
# print()
# gameStats(games4, player=2)

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
