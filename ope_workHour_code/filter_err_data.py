import pandas as pd
import datetime

def filter_err(dataset_oneEm_modiTime):
    columns_header = ["廠區", "工號", "姓名", "主承商", "次承商", "下包商", "入廠日期", "入廠時間", "出廠日期","出廠時間","工時"]
    dataset_FilterErrData_CalDur = pd.DataFrame(columns=columns_header)


    currDate = ''
    SkipDayData = False
    isInFac = False;   # False 為出廠; True 為進廠
    inFacTime = ''
    outFacTime = ''
    rowIndex = 0

    # 刪除錯誤資料並計算工時，放入新的dataset中
    for index, row in dataset_oneEm_modiTime.iterrows():
        if(currDate != row["日期"]):   #日期變化
            SkipDayData = False
            if(not isInFac and inFacTime != '' and outFacTime != ''):
                dataset_FilterErrData_CalDur.loc[rowIndex] = [row["廠區"], row["工號"], row["姓名"], row["主承商"], 
                                                                row["次承商"], row["下包商"], inFacTime.date(), inFacTime.time(),
                                                                outFacTime.date(), outFacTime.time(), (outFacTime - inFacTime).seconds/3600]
                outFacTime = ''
                inFacTime = ''
            if(row["入離廠"] == "入廠"):
                if(isInFac):
                    inFacTime=datetime.datetime.combine(row["日期"], time=row["時間"])
                else:
                    isInFac = True
                    inFacTime=datetime.datetime.combine(row["日期"], time=row["時間"])
            else:
                if(not isInFac):   #前一筆資料為離廠, 不為隔夜班
                    SkipDayData = True
                    inFacTime = ''  
                    outFacTime = ''
                    pass   #刪除當天所有資料
                else:   # 隔夜班
                    outFacTime = datetime.datetime.combine(row["日期"], time=row["時間"])

                    if(inFacTime.date()+datetime.timedelta(days=1) != outFacTime.date()):
                        continue

                    dataset_FilterErrData_CalDur.loc[rowIndex] = [row["廠區"], row["工號"], row["姓名"], row["主承商"], 
                                                                row["次承商"], row["下包商"], inFacTime.date(), inFacTime.time(),
                                                                outFacTime.date(), outFacTime.time(), (outFacTime - inFacTime).seconds/3600]
                    outFacTime = ''
                    inFacTime = ''
                    isInFac = False
        
        else:   #日期沒變化
            if(SkipDayData):
                continue
            if(row["入離廠"] == "離廠"):
                if(isInFac):
                    outFacTime = datetime.datetime.combine(row["日期"], time=row["時間"])
                    isInFac = False
                else:
                    outFacTime = datetime.datetime.combine(row["日期"], time=row["時間"])
            else:
                if(not isInFac):
                    isInFac = True
                    if(inFacTime != '' and outFacTime != ''):   #前一筆資料為離廠
                        
                        #print((outFacTime - inFacTime).seconds/3600)
                        dataset_FilterErrData_CalDur.loc[rowIndex] = [row["廠區"], row["工號"], row["姓名"], row["主承商"], 
                                                                    row["次承商"], row["下包商"], inFacTime.date(), inFacTime.time(),
                                                                    outFacTime.date(), outFacTime.time(), (outFacTime - inFacTime).seconds/3600]
                    inFacTime=datetime.datetime.combine(row["日期"], time=row["時間"])
                    outFacTime = ''
        
        currDate = row["日期"]
        rowIndex+=1

    if(not isInFac and inFacTime != '' and outFacTime != ''):
        #print((outFacTime - inFacTime).seconds/3600)
        dataset_FilterErrData_CalDur.loc[rowIndex] = [row["廠區"], row["工號"], row["姓名"], row["主承商"], 
                                                                row["次承商"], row["下包商"], inFacTime.date(), inFacTime.time(),
                                                                outFacTime.date(), outFacTime.time(), (outFacTime - inFacTime).seconds/3600]

    return dataset_FilterErrData_CalDur                                                            