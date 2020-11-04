import click
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
        if fn := messages.get(doc_id):
            return send_file(fn, mimetype='application/xml')
        else:
            abort(404)
    else:
        abort(400)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-p', '--port', default=9191, show_default=True, help='Port number the server should run on')
@click.option('--reload', is_flag=True, default=False, show_default=True, help='Reload the server when source code change')
def main(port, reload):
    app.run(port=port, use_reloader=reload)


if __name__ == '__main__':
    main()
