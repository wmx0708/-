import time, json, requests
import pandas as pd

url="https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoCountryConfirmAdd,WomWorld,WomAboard"
get_data=json.dumps(requests.get(url=url).json()['data'])
data=json.loads(get_data)
print(data)

world_list=[]
world_data=data['WomAboard']
for i in range(len(world_data)):
    world_dict={}
    world_dict['国家']=world_data[i]['name']
    world_dict['所属洲']=world_data[i]['continent']
    world_dict['日期']= world_data[i]['y'] + world_data[i]['date']
    world_dict['confirm']=world_data[i]['confirm']
    world_dict['confirmAdd'] = world_data[i]['confirmAdd']
    world_dict['suspect']=world_data[i]['suspect']
    world_dict['dead']=world_data[i]['dead']
    world_dict['heal']=world_data[i]['heal']
    world_dict['nowConfirm']=world_data[i]['nowConfirm']
    world_dict['confirmCompare'] = world_data[i]['confirmCompare']
    world_dict['nowConfirmCompare'] = world_data[i]['nowConfirmCompare']
    world_dict['healCompare'] = world_data[i]['healCompare']
    world_dict['deadCompare'] = world_data[i]['deadCompare']
    world_list.append(world_dict)
world_frame=pd.DataFrame(world_list)#world_frame为整理好的全球疫情数据dataframe结构
world_name = pd.read_excel("世界各国中英文对照.xlsx")
#将中英文对照的dataframe与world_frame合并
world_frame = pd.merge(world_frame,world_name,left_on ="国家",right_on = "国家中文名称",how="inner")
world_frame = world_frame[['国家','国家英文名称', '所属洲','日期', 'nowConfirm','confirm', 'confirmAdd',  'suspect', 'dead',
                                           'heal','confirmCompare','nowConfirmCompare','deadCompare','healCompare']]
world_frame.to_excel(time.strftime("%Y-%m-%d")+'-world_list.xlsx',index=False)