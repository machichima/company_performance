from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255),nullable=False)
    rel_p = db.relationship('Workers', backref='project', lazy=True)
    

class Workers(db.Model):
    __tablename__ = 'workers'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key = True)
    worknumber = db.Column(db.String(255),nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    rel_w = db.relationship('WorkHours', backref='worker', lazy=True)


class WorkHours(db.Model):
    __tablename__ = 'workHours'
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Date(), nullable=False)
    workHour = db.Column(db.Time(), nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'), nullable=False)
