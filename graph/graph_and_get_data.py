from re import L
from models import Project, Workers, WorkHours
import pandas as pd
from .graph import graph_3D


def graph_and_get_data(project_id, workers):

    project = Project.query.filter_by(id=project_id).first()
    #print(project)
    #print(Workers.worknumber.in_(["C0940050", "E1561600"]))
    w = Workers.query.filter(Workers.worknumber.in_(workers)).all()
    
    if(project == None or w == None):
        return 'error'

    df_all = pd.DataFrame()

    for i in range(len(w)):
        columns_header = [w[i].worknumber, " "]
        df_one = pd.DataFrame(columns=columns_header)
        hours = WorkHours.query.filter_by(worker_id=w[i].id).all()

        rowIndex = 0;
        for j in range(len(hours)):
            df_one.loc[rowIndex] = [hours[j].date, hours[j].workHour]
            rowIndex+=1

        df_all = pd.concat([df_all, df_one], axis=1) 

    graph_3D(df_all, project.id)
    #print(w)