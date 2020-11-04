
import os
import json
from flask import Flask, request, abort, send_file

from db import messages

app = Flask(__name__)


@app.errorhandler(400)
@app.errorhandler(404)
def page_not_found(error):
    return "", 404


@app.route('/list-db', methods=['GET', 'POST'])
def list_database():
    return json.dumps(messages)


@app.route('/get', methods=['GET', 'POST'])
def get():
    doc_id = request.values.get('id') or request.values.get('rc')
    if doc_id:
        if fn := messages.get(doc_id):
            return send_file(fn, mimetype='application/xml')
        else:
            abort(404)
    else:
        abort(400)


if __name__ == '__main__':
    app.run(port=9191, use_reloader=True)
