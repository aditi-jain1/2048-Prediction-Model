from flask import Flask, render_template, jsonify, request
import random
from gameLogic import *
from gameRunner import getModelInput

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/random-array', methods=['GET'])
def random_array():
    # Create a 4x4 array with random integers between 1 and 100
    array = instantiateBoard()
    return jsonify({'array': array})

@app.route('/add-one', methods=['POST'])
def add_one():
    # Get the array from the POST request
    data = request.get_json()
    board = data.get('array', [])
    value = data.get('value')
    
    if isGameOver(board):
        return jsonify({'game_over': True, 'array': board})

    next_move = getModelInput(board, value)
    moves = {1: "up", 2: "right", 3: "down", 4: "left"}
    board_before_move = [row[:] for row in board]
    board = move(board, moves[int(next_move)])
    board = generateNewTile(board)
    # Return the updated array
    return jsonify({'game_over': False, 'array': board})

if __name__ == '__main__':
    app.run(debug=True)