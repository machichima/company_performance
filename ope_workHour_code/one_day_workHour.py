import pandas as pd

def one_day_workHour(dataset_FilterErrData_CalDur, emNum):
    # 計算一天工時
    columns_header_total = [emNum, " "]
    dataset_WorkTime_oneWorker = pd.DataFrame(columns=columns_header_total)
    dataset_WorkTime_oneWorker_noFil = pd.DataFrame(columns=columns_header_total)

    currDate = ''
    workTime = 0
    rowIndex = 0
    rowIndex_noFil = 0
    for index, row in dataset_FilterErrData_CalDur.iterrows():
        #print(currDate, ": ", workTime)
        if(currDate != row["入廠日期"]):   #日期變化
            if(currDate != '' and workTime <= 12 and workTime >= 6):
                dataset_WorkTime_oneWorker.loc[rowIndex] = [currDate, workTime]
                rowIndex+=1
            dataset_WorkTime_oneWorker_noFil.loc[rowIndex_noFil] = [currDate, workTime]
            rowIndex_noFil += 1

            workTime = row["工時"]
            currDate = row["入廠日期"]
            continue
        
        
        currDate = row["入廠日期"]
        workTime += row["工時"]
        
    if(currDate != '' and workTime <= 12 and workTime >= 6):
        dataset_WorkTime_oneWorker.loc[rowIndex] = [currDate, workTime]
    dataset_WorkTime_oneWorker_noFil.loc[rowIndex_noFil] = [currDate, workTime]

    max_val_date = dataset_WorkTime_oneWorker_noFil.iloc[pd.to_numeric(dataset_WorkTime_oneWorker_noFil[" "]).idxmax(), 0]
    return [dataset_WorkTime_oneWorker, dataset_WorkTime_oneWorker_noFil, max_val_date]