from flask import Flask
from semantic_search import output_dict

app = Flask(__name__)

@app.route('/predict')
def predict():
    return output_dict

if __name__ == "__main__":
    app.run(debug=True)