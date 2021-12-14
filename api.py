from flask import Flask, jsonify, request, send_file
from flask_restful import Resource
from ope_workHour_code.main import workHour

UPLOAD_FOLDER = '/file'

app = Flask(__name__)
#api = Api(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# get performance of company
@app.route('/performance', methods=['GET', 'POST'])
def upload_csv():
    if(request.method == "POST"):
        file = request.files['file']
        return jsonify(workHour(file))
    else:
        return 'none'

@app.route('/images/<int:pid>.png')
def get_image(pid):
    return send_file(
            '%s.png' % pid,
            mimetype='image/jpeg',
            as_attachment=True,
            attachment_filename='%s.png' % pid)

if __name__ == '__main__':
    app.debug = True
    app.run()
