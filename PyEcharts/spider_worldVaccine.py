import time, json, requests
import pandas as pd

url="https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=VaccineSituationData"
get_data=json.dumps(requests.get(url=url).json()['data'])
data=json.loads(get_data)
print(data)

worldVaccine_list=[]
worldVaccine_data=data['VaccineSituationData']
for i in range(len(worldVaccine_data)):
    worldVaccine_dict={}
    worldVaccine_dict['国家']=worldVaccine_data[i]['country']
    worldVaccine_dict['日期']= worldVaccine_data[i]['date']
    worldVaccine_dict['疫苗']=worldVaccine_data[i]['vaccinations']
    worldVaccine_dict['疫苗总接种数'] = worldVaccine_data[i]['total_vaccinations']
    worldVaccine_dict['每百人疫苗总接种数']=worldVaccine_data[i]['total_vaccinations_per_hundred']
    worldVaccine_list.append(worldVaccine_dict)
worldVaccine_frame=pd.DataFrame(worldVaccine_list)#world_frame为整理好的全球疫情数据dataframe结构
world_name = pd.read_excel("世界各国中英文对照.xlsx")
#将中英文对照的dataframe与world_frame合并
worldVaccine_frame = pd.merge(worldVaccine_frame, world_name, left_on ="国家", right_on ="国家中文名称", how="inner")
worldVaccine_frame = worldVaccine_frame[['国家', '国家英文名称', '日期', '疫苗', '疫苗总接种数','每百人疫苗总接种数',]]
worldVaccine_frame.to_excel(time.strftime("%Y-%m-%d") + '-worldVaccine_list.xlsx', index=False)