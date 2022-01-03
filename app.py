from flask import Flask, jsonify, request, send_file
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from ope_workHour_code.main import workHour
from models import db, Project, Workers
from flask_migrate import Migrate

# your app config  

UPLOAD_FOLDER = '/file'

app = Flask(__name__)
#api = Api(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config.from_object('config')
db.init_app(app)

migrate = Migrate()
migrate.init_app(app, db)

# get performance of company
@app.route('/performance', methods=['GET', 'POST'])
def upload_csv():
    if(request.method == "POST"):
        file = request.files['file']
        a = workHour(file, db)
        global file_temp 
        file_temp = a[0]
        json_file = a[1]
        return jsonify(json_file)
    else:
        return 'none'

@app.route('/get', methods=['GET'])
def get_txt():
    global file_temp
    print(file_temp)
    return 'Hi'

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
