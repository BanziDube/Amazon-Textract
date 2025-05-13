from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data')
def get_data():
    # Load the JSON data
    with open('build/data.json') as f:
        data = json.load(f)

    # Reformat data as a dictionary of filenames and labels
    formatted_data = {}
    for item in data:
        filename = item["Filename"]
        labels = item["Labels"]
        formatted_data[filename] = labels

    return jsonify(formatted_data)


if __name__ == '__main__':
    app.run(debug=True)
