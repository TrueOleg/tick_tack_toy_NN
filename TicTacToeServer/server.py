# importing Flask
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import json
# import tic tac toe game 
from Train_TicTacToe_NW import *

import numpy as np


# setting up session
sess = tf.InteractiveSession()
prediction = neural_network_model(x)
saver = tf.train.Saver()
saver.restore(sess,"./model/model.ckpt")
graph = tf.get_default_graph()

app = Flask(__name__)
CORS(app)

def  bestmove(input):
    global graph
    with graph.as_default():
        data = (sess.run(tf.argmax(prediction.eval(session = sess,feed_dict={x:[input]}),1)))
    return data

@app.route('/api/ticky', methods=['POST'])
def ticky_api():
    data = request.get_json(force=True)
    data = np.array(data)
    data = data.tolist()
    return jsonify(np.asscalar(bestmove(data)[0]))


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)

