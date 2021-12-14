import pandas as pd

def one_day_workHour(dataset_FilterErrData_CalDur, emNum):
    # 計算一天工時
    columns_header_total = [emNum, " "]
    dataset_WorkTime_oneWorker = pd.DataFrame(columns=columns_header_total)

    currDate = ''
    workTime = 0
    rowIndex = 0;
    for index, row in dataset_FilterErrData_CalDur.iterrows():
        #print(currDate, ": ", workTime)
        if(currDate != row["入廠日期"]):   #日期變化
            if(currDate != '' and workTime <= 12 and workTime >= 6):
                dataset_WorkTime_oneWorker.loc[rowIndex] = [currDate, workTime]
                rowIndex+=1
                
            workTime = row["工時"]
            currDate = row["入廠日期"]
            continue
        
        
        currDate = row["入廠日期"]
        workTime += row["工時"]
        
    if(currDate != '' and workTime <= 12 and workTime >= 6):
        dataset_WorkTime_oneWorker.loc[rowIndex] = [currDate, workTime]

    return dataset_WorkTime_oneWorker