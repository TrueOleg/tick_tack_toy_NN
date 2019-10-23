import random
import numpy as np


def initBoard():
    board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    return board


def getMoves(board):
    moves = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                moves.append((i, j))
    return moves


def getWinner(board):
    candidate = 0
    won = 0

    # Check rows
    for i in range(len(board)):
        candidate = 0
        for j in range(len(board[i])):
            # Make sure there are no gaps
            if board[i][j] == 0:
                break

            # Identify the front-runner
            if candidate == 0:
                candidate = board[i][j]

            # Determine whether the front-runner has all the slots
            if candidate != board[i][j]:
                break
            elif j == len(board[i]) - 1:
                won = candidate

    if won > 0:
        return won

    # Check columns
    for j in range(len(board[0])):
        candidate = 0
        for i in range(len(board)):

            # Make sure there are no gaps
            if board[i][j] == 0:
                break

            # Identify the front-runner
            if candidate == 0:
                candidate = board[i][j]

            # Determine whether the front-runner has all the slots
            if candidate != board[i][j]:
                break
            elif i == len(board) - 1:
                won = candidate

    if won > 0:
        return won

    # Check diagonals
    candidate = 0
    for i in range(len(board)):
        if board[i][i] == 0:
            break
        if candidate == 0:
            candidate = board[i][i]

        if candidate != board[i][i]:
            break
        elif i == len(board) - 1:

            won = candidate

    if won > 0:
        return won

    candidate = 0
    for i in range(len(board)):
        if board[2 - i][2 - i] == 0:
            break
        if candidate == 0:
            candidate = board[2 - i][2 - i]
        if candidate != board[2 - i][2 - i]:
            break
        elif i == len(board) - 1:
            won = candidate

    if won > 0:
        return won

    # Still no winner?
    if (len(getMoves(board)) == 0):
        # It's a draw
        return 0
    else:
        # Still more moves to make
        return -1


def printBoard(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            mark = ' '
            if board[i][j] == 1:
                mark = 'X'
            elif board[i][j] == 2:
                mark = 'O'
            if (j == len(board[i]) - 1):
                print(mark)
            else:
                print(str(mark) + "|", end='')
        if (i < len(board) - 1):
            print("-----")


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


# history = simulateGame()
# print(history)


def movesToBoard(moves):
    board = initBoard()
    for move in moves:
        player = move[0]
        coords = move[1]
        board[coords[0]][coords[1]] = player
    return board


# board = movesToBoard(history)
# printBoard(board)
# print(getWinner(board))

# games = [simulateGame() for _ in range(10000)]


def gameStats(games, player=1):
    stats = {"win": 0, "loss": 0, "draw": 0}
    for game in games:
        result = getWinner(movesToBoard(game))
        if result == -1:
            continue
        elif result == player:
            stats["win"] += 1
        elif result == 0:
            stats["draw"] += 1
        else:
            stats["loss"] += 1

    winPct = stats["win"] / len(games) * 100
    lossPct = stats["loss"] / len(games) * 100
    drawPct = stats["draw"] / len(games) * 100

    print("Results for player %d:" % (player))
    print("Wins: %d (%.1f%%)" % (stats["win"], winPct))
    print("Loss: %d (%.1f%%)" % (stats["loss"], lossPct))
    print("Draw: %d (%.1f%%)" % (stats["draw"], drawPct))


# gameStats(games)
# print()
# gameStats(games, player=2)

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
