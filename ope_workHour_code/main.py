'''
去除部份錯誤打卡資料(進出廠邏輯錯誤)
將資料以日期時間進行排序，並將日期和時間分開成不同欄位
計算當天整天工時
將一間廠商中所有工人的工時放在一個sheet中
'''

import pandas as pd
from flask import url_for
from models import Project, Workers, WorkHours

from .time_format import time_format
from .filter_err_data import filter_err
from .one_day_workHour import one_day_workHour
from .slope import slope
from .graph import graph_3D

def workHour(file, db):

    sheets = pd.read_excel(file, sheet_name=None)

    slope_li = []
    img_count = 1

    WorkHours.query.delete()
    Workers.query.delete()
    Project.query.delete()

    for name, sheet in sheets.items():

        project = Project(name=name)
        db.session.add(project)
        db.session.commit()
        db.session.refresh(project)

        dataset = sheet.sort_values(by=['工號'])
        dataset_workNum = dataset["工號"]
        dataset_workNum = dataset_workNum.drop_duplicates()

        data_modify = dataset
        dataset_WorkTime_all = pd.DataFrame()

        for emNum in dataset_workNum:

        # emNum = "D8682880"
            if(emNum == "工號"): break

            worker = Workers(worknumber=emNum, project_id=project.id)
            db.session.add(worker)
            db.session.commit()
            db.session.refresh(worker)

            dataset_oneEm = data_modify.loc[data_modify['工號'] == emNum]

            dataset_oneEm_modiTime = time_format(dataset_oneEm)   # 分離日期和時間，並將時間轉為24小時制, 變為時間及日期的格式

            dataset_FilterErrData_CalDur = filter_err(dataset_oneEm_modiTime)   # 刪除錯誤資料並計算工時，放入新的dataset中

            dataset_WorkTime_oneWorker = one_day_workHour(dataset_FilterErrData_CalDur, emNum)   # 計算一天工時

            for index, row in dataset_WorkTime_oneWorker.iterrows():
                workhour = WorkHours(date=row[emNum], workHour=row[" "], worker_id=worker.id)
                db.session.add(workhour)
            db.session.commit()
            
            dataset_WorkTime_all = pd.concat([dataset_WorkTime_all, dataset_WorkTime_oneWorker], axis=1) 

        graph_3D(dataset_WorkTime_all, img_count)

        slope_li.append({'name': name, 'slope': slope(dataset_WorkTime_all), 'image': url_for('static', filename="images/"+str(img_count)+'.png')})
        print(slope_li)
        img_count+=1
            #dataset_FilterErrData_CalDur.to_excel(writer, sheet_name=emNum, index=False)
    slope_li_sorted = sorted(slope_li, key=lambda d: d['slope'])  #{k: v for k, v in sorted(slope_li.items(), key=lambda item: item[1])}
    return [dataset_WorkTime_all, slope_li_sorted]
