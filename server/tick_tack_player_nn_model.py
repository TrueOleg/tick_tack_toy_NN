import random
import tensorflow as tf
import numpy as np
from tensorflow import keras
from tick_tack_toy import getWinner, movesToBoard, getMoves, initBoard, printBoard


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


def bestMove(board, model, player, rnd=0):
    scores = []
    moves = getMoves(board)

    # Make predictions for each possible move
    for i in range(len(moves)):
        future = np.array(board)
        future[moves[i][0]][moves[i][1]] = player
        prediction = model.predict(future.reshape((-1, 9)))[0]
        if player == 1:
            winPrediction = prediction[1]
            lossPrediction = prediction[2]
        else:
            winPrediction = prediction[2]
            lossPrediction = prediction[1]
        drawPrediction = prediction[0]
        if winPrediction - lossPrediction > 0:
            scores.append(winPrediction - lossPrediction)
        else:
            scores.append(drawPrediction - lossPrediction)

    # Choose the best move with a random factor
    bestMoves = np.flip(np.argsort(scores))
    for i in range(len(bestMoves)):
        if random.random() * rnd < 0.5:
            return moves[bestMoves[i]]

    # Choose a move completely at random
    return moves[random.randint(0, len(moves) - 1)]


def simulateGame(x=0, p1=None, p2=None, rnd=0):
    print('!', x)
    history = []
    board = initBoard()
    playerToMove = 1

    while getWinner(board) == -1:
        print('Winner', getWinner(board))
        # Chose a move (random or use a player model if provided)
        move = None
        if playerToMove == 1 and p1 != None:
            move = bestMove(board, p1, playerToMove, rnd)
        elif playerToMove == 2 and p2 != None:
            move = bestMove(board, p2, playerToMove, rnd)
        else:
            moves = getMoves(board)
            move = moves[random.randint(0, len(moves) - 1)]

        # Make the move
        board[move[0]][move[1]] = playerToMove
        print(move)
        # Add the move to the history
        history.append((playerToMove, move))
        movesToBoard(history)
        printBoard(board)
        # Switch the active player
        playerToMove = 1 if playerToMove == 2 else 2

    return history
