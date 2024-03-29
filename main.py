import click
import json
from flask import Flask, request, abort, send_file, jsonify
from db import messages

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

app = Flask(__name__)


@app.errorhandler(400)
@app.errorhandler(404)
def page_not_found(error):
    return "", 404


@app.route('/list-db', methods=['GET', 'POST'])
def list_database():
    return jsonify(messages)


@app.route('/get', methods=['GET', 'POST'])
def get_resource():
    doc_id = request.values.get('id') or request.values.get('rc')
    if doc_id:
        fn = messages.get(doc_id)
        if fn:
            return send_file(fn, mimetype='application/xml')
        else:
            abort(404)
    else:
        abort(400)


@app.route('/fnusa/push', methods=['POST'])
def fnusa_push_resource():
    if not request.headers.get("Content-Type").lower().startswith("multipart/form-data"):
        return 'Bad Content-Type header', 400
    if not request.headers.get("Authorization"):
        return 'Bad Authorization header', 400

    if request.files:
        print("FILES: ...")
        for f in request.files:
            uploaded = request.files[f]
            uploaded_file_name = f"uploaded/{f}"
            print(f"UPLOADED: name='{f}', content-type='{uploaded.content_type}', mimetype='{uploaded.mimetype}', save-to='{uploaded_file_name}'")
            uploaded.save(uploaded_file_name)
        print("-" * 40)
        return ""
    else:
        print(">>>>>")
        return 'No Request Body exists', 400


@app.route('/artiis/senddoc', methods=['POST'])
def artiis_senddoc():
    if request.headers.get("Content-Type").lower() != "application/xml; charset=utf-8":
        return 'Bad Content-Type header', 400
    if not request.headers.get("Authorization"):
        return 'Bad Authorization header', 400

    if request.data:
        return ""
    else:
        return 'No Request Body exists', 400


@app.route('/artiis/patsum', methods=['GET'])
def artiis_patsum():
    if request.headers.get("Accept").lower() != "application/xml":
        return 'Bad Accept header', 400
    if request.headers.get("Accept-Charset").lower() != "utf-8":
        return 'Bad Accept-Charset header', 400
    if not request.headers.get("Authorization"):
        return 'Bad Authorization header', 400

    doc_id = request.values.get('rc')
    if doc_id:
        fn = messages.get(doc_id)
        if fn:
            return send_file(fn, mimetype='application/xml')
        else:
            abort(404)
    else:
        abort(400)


@app.route('/artiis/beds', methods=['GET'])
def artiis_beds():
    if request.headers.get("Accept", "").lower() != "application/xml":
        return 'Bad Accept header', 400
    if request.headers.get("Accept-Charset", "").lower() != "utf-8":
        return 'Bad Accept-Charset header', 400
    if not request.headers.get("Authorization"):
        return 'Bad Authorization header', 400

    fn = messages.get('beds')
    if fn:
        return send_file(fn, mimetype='application/xml')
    else:
        abort(404)


@app.route('/sos/rescconfirm', methods=['POST'])
def sos_rescconfirm():
    if request.headers.get("Content-Type").lower() != "application/xml; charset=utf-8":
        return 'Bad Content-Type header', 400
    if not request.headers.get("Authorization"):
        return 'Bad Authorization header', 400

    if request.data:
        print(request.data)
        return ""
    else:
        return 'No Request Body exists', 400


@app.route('/trans/get', methods=['POST'])
def trans_get():
    if request.headers.get("Content-Type").lower() != "application/json":
        return 'Bad Content-Type header', 400
    if not request.headers.get("Authorization"):
        return 'Bad Authorization header', 400

    if request.data:
        params = json.loads(request.json)
        fn = messages.get(params['RodneCislo'])
        if fn:
            with open(fn) as f:
                return jsonify({'DastaResponse': f.read()})
        else:
            abort(404)
    else:
        return 'No Request Body exists', 400


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-p', '--port', default=9191, show_default=True, help='Port number the server should run on')
@click.option('--reload', is_flag=True, default=False, show_default=True, help='Reload the server when source code change')
def main(port, reload):
    app.run(port=port, use_reloader=reload)


if __name__ == '__main__':
    main()
