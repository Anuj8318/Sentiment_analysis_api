from flask import Flask, jsonify


# entry point 
app = Flask(__name__)


@app.route('/analyze_sentiment', methods=['POST'])

def analyze_sentiment():
    # We'll implement this function later
    return jsonify({"message": "Not implemented yet"}), 501


if __name__=="main":
    app.run(debug=True)

