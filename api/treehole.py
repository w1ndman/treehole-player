from flask import Flask, render_template, send_from_directory, abort
import os

app = Flask(__name__, static_folder='../treehole.pku.edu.cn/', template_folder='../treehole.pku.edu.cn')

@app.route('/')
@app.route('/web')
def serve_index():
    return render_template('web/index.html')

@app.route('/version')
def version():
    return render_template('version.html')

@app.route('/api/pku/tags')
def tags():
    return render_template('tags.html')

# JS modules must be served with application/javascript or the browser refuses
# to execute <script type="module"> (Strict MIME type checking per HTML spec).
@app.route('/modify.js')
def modify():
    return send_from_directory(app.static_folder, 'modify.js', mimetype='application/javascript')

@app.route('/firebase.js')
def firebase():
    return send_from_directory(app.static_folder, 'firebase.js', mimetype='application/javascript')

@app.route('/import_data.js')
def import_data():
    return send_from_directory(app.static_folder, 'import_data.js', mimetype='application/javascript')


@app.route('/api/pku/manager_spec')
def m_s():
    return render_template('manager_spec.json')

# Files served from the deployed web/ tree at /web/<...>. These are static
# assets whose paths were baked into the built bundle under /web/static/...
@app.route('/web/<path:path>')
def serve_assets(path):
    return send_from_directory(app.static_folder + '/web/', path)


# Catch-all: serve anything else from web/<path>. If the file doesn't exist
# AND the path is not under /api/ (which the frontend intentionally probes with
# the expectation of a 404, per README), fall back to web/index.html so the SPA
# router can take over on a hard refresh.
@app.route('/<path:path>')
def serve_static_files(path):
    target = os.path.join(app.static_folder, 'web', path)
    if not os.path.isfile(target):
        if path.startswith('api/'):
            abort(404)
        return render_template('web/index.html')
    return send_from_directory(app.static_folder + '/web/', path)


# if __name__ == '__main__':
#     app.run(
#         host='0.0.0.0',
#         port=500,
#         debug=False
#     )
