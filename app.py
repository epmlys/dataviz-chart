"""Simple Flask service."""

import os

from flask import (Flask, jsonify, render_template, request, make_response,
                   url_for, redirect)

import db


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/builds', methods=['GET'])
def get_build_history():
    return make_response(jsonify(db.build_history), 200)


@app.route('/durations', methods=['GET'])
def get_builds_duration():
    return make_response(jsonify(db.time_duration), 200)


@app.route('/upload', methods=['POST'])
def upload():
    file_data = request.files['file']
    if file_data:
        file_data.save(os.path.join(app.config['UPLOAD_FOLDER'],
                       'history.csv'))
        import db
        db = reload(db)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
