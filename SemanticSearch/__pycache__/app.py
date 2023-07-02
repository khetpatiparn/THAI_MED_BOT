from flask import Flask, request, jsonify
from .semantic import process



app = Flask(__name__)

@app.route('/api/process', methods=['POST'])
def process_api():
    input_data = request.json.get('input')
    result = process(input_data)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
