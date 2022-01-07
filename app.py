from flask import Flask, jsonify, request, send_file, url_for, make_response
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from ope_workHour_code.main import workHour
from models import db, Project, Workers
from flask_migrate import Migrate
from graph.graph_and_get_data import graph_and_get_data

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
        json_file = workHour(file, db)
        return jsonify(json_file)
    else:
        return 'none'

@app.route('/get', methods=['GET'])
def get_txt():
    #global file_temp
    #print(file_temp)
    worker = Workers.query.filter_by(project_id=13).all()
    print(worker[0].worknumber) 
    return 'Hi'

@app.route('/graph', methods=['POST'])
def graph():
    json = request.get_json()
    project_id = json['project']
    workers = json['workers']
    m = graph_and_get_data(project_id, workers)
    if(m == 'error'):
        return make_response(jsonify("error"), 400)
    return {'project_id': project_id, 'image': url_for('static', filename="images/"+str(project_id)+'.png')}

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
