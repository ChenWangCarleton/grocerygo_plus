import os

import flask
from flask import request, send_file, jsonify

from api_util import *

#print(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html'))
app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def index():
    if 'search' in request.args:
        query = request.args['search']
        return generate_response(query)
    else:
        return send_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html'))

@app.route('/api/v1/byid', methods=['GET'])
def search_by_id():
    if 'id' in request.args:
        query = request.args['id']
        return jsonify(generate_response_id(query))
    else:
        return send_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html'))



app.run()
