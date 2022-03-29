import time, json, requests
import demjson
import pandas as pd
import numpy as np

url = 'https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=ChinaVaccineTrendData'
get_data=json.dumps(requests.get(url=url).json()['data'])
data = json.loads(get_data)
print(data)

chinaDayVaccine=[]
for i in range(len(data['ChinaVaccineTrendData'])):
    chinaDayVaccine_dict={}
    chinaDayVaccine_dict['date'] = data['ChinaVaccineTrendData'][i]['y'] + "." + data['ChinaVaccineTrendData'][i]['date']
    chinaDayVaccine_dict['total_vaccinations'] = data['ChinaVaccineTrendData'][i]['total_vaccinations']
    chinaDayVaccine_dict['total_vaccinations_per_hundred'] = data['ChinaVaccineTrendData'][i]['total_vaccinations_per_hundred']
    chinaDayVaccine.append(chinaDayVaccine_dict)

china_day_frame=pd.DataFrame(chinaDayVaccine)
china_day_frame.to_excel(time.strftime("%Y-%m-%d")+"-china_DayVaccine_list.xlsx",index=False)
