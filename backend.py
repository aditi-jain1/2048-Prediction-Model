from flask import Flask, render_template, jsonify, request
import random
from gameLogic import *

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
    array = data.get('array', [])
    
    # Add 1 to each element of the array
    updated_array = [[element + 1 for element in row] for row in array]
    
    # Return the updated array
    return jsonify({'array': updated_array})

if __name__ == '__main__':
    app.run(debug=True)