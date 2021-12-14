import pandas as pd

def time_format(dataset_oneEm):

    dataset_oneEm_modiTime = dataset_oneEm.rename(columns={'刷卡時間': '日期'})
    li = ['']*len(dataset_oneEm.values)
    dataset_oneEm_modiTime.insert(7, "時間", li)

    # 分離日期和時間，並將時間轉為24小時制

    for i in range(len(dataset_oneEm["刷卡時間"].values)):
        dateTimeStr = dataset_oneEm["刷卡時間"].values[i]
        dateTimeList = dateTimeStr.split(' ')

        timeList = dateTimeList[2].split(':')

        if(dateTimeList[1] == "下午"):
            if(int(timeList[0]) == 12): 
                pass
            else:
                timeList[0] = str(int(timeList[0]) + 12)
        dateTimeList[2] = ":".join(timeList)

        dataset_oneEm_modiTime["日期"].values[i] = dateTimeList[0]
        dataset_oneEm_modiTime["時間"].values[i] = dateTimeList[2]

    # 將時間及日期的字串變為時間及日期的格式
    dataset_oneEm_modiTime["時間"] = pd.to_datetime(dataset_oneEm_modiTime["時間"], format="%H:%M:%S").dt.time
    dataset_oneEm_modiTime["日期"] = pd.to_datetime(dataset_oneEm_modiTime["日期"], format="%Y/%m/%d").dt.date
    dataset_oneEm_modiTime = dataset_oneEm_modiTime.sort_values(by=['日期', '時間'])

    return dataset_oneEm_modiTime