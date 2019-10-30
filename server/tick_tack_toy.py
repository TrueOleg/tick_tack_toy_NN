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
        if board[i][2 - i] == 0:
            break
        if candidate == 0:
            candidate = board[i][2 - i]
        if candidate != board[i][2 - i]:
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
