import time, json, requests
import pandas as pd
from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.charts import Page, WordCloud
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType, ChartType
from bs4 import BeautifulSoup
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts


# url1 = "https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=VaccineTopData"
# get_data = json.dumps(requests.get(url=url1).json()['data'])
# data = json.loads(get_data)
#
# china_total_vaccinations_per_hundred = (Pie().
#             set_global_opts(title_opts=opts.TitleOpts(title="我国每百人疫苗总接种数", pos_left='center', pos_top='center',
#                                                       title_textstyle_opts=opts.TextStyleOpts(color='#000000'))))
# china_total_vaccinations_per_hundred_num = (Pie().
#                    set_global_opts(title_opts=opts.TitleOpts(title=(str(data["VaccineTopData"]["中国"]['total_vaccinations_per_hundred']) + "   "),
#                                                              pos_top='15%', pos_left='center',
#                                                              subtitle=("新增疫苗接种数: " + str(data["VaccineTopData"]["中国"]['new_vaccinations'])),
#                                                              item_gap=1,
#                                                              title_textstyle_opts=opts.TextStyleOpts(color="#00FFFF",
#                                                                                                      font_size=30),
#                                                              subtitle_textstyle_opts=opts.TextStyleOpts(color="#00BFFF")
#                                                              )))
#
# world_total_vaccinations_per_hundred = (Pie().
#             set_global_opts(title_opts=opts.TitleOpts(title="全球每百人疫苗总接种数", pos_left='center', pos_top='center',
#                                                       title_textstyle_opts=opts.TextStyleOpts(color='#000000'))))
# world_total_vaccinations_per_hundred_num = (Pie().
#                    set_global_opts(title_opts=opts.TitleOpts(title=(str(data["VaccineTopData"]["全球"]['total_vaccinations_per_hundred']) + "   "),
#                                                              pos_top='15%', pos_left='center',
#                                                              subtitle=("新增疫苗接种数: " + str(data["VaccineTopData"]["全球"]['new_vaccinations'])),
#                                                              item_gap=1,
#                                                              title_textstyle_opts=opts.TextStyleOpts(color="#00FFFF",
#                                                                                                      font_size=30),
#                                                              subtitle_textstyle_opts=opts.TextStyleOpts(color="#00BFFF")
#                                                              )))
# page = (
#     Page()
#       .add(china_total_vaccinations_per_hundred)
#       .add(china_total_vaccinations_per_hundred_num)
#       .add(world_total_vaccinations_per_hundred)
#       .add(world_total_vaccinations_per_hundred_num)
# ).render("2.html")
#width:220px;height:31px;position:absolute;top:22px;left:920px;
# width:220px;height:62px;position:absolute;top:54px;left:920px;
# width:220px;height:31px;position:absolute;top:116px;left:920px;
# width:220px;height:62px;position:absolute;top:148px;left:920px;

# China_DayVaccine_file = time.strftime("%Y-%m-%d") + '-china_DayVaccine_list.xlsx'
# China_DayVaccine_data=pd.read_excel(China_DayVaccine_file)
# ylist=[i/10000000 for i in list(China_DayVaccine_data["total_vaccinations"])]
# line6=(
#     Line(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
#     .add_xaxis(list(China_DayVaccine_data["date"]))
#     .add_yaxis("全国疫苗总接种数",ylist,is_smooth=True,)
#     .set_global_opts(title_opts=opts.TitleOpts(title="全国每日疫苗接种趋势"))
#     # .set_series_opts(areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
#     #                  label_opts=opts.LabelOpts(is_show=False))
# )
#
# line6.render("全国疫苗接种趋势.html")

lq1 = (
    Liquid()  # 下面确定名称，比例，是否显示轮廓，形状
    .add("lq",
         [0.37],
         color=["#c23531"],background_color="#ff9966",
         outline_itemstyle_opts={"outline-color":"#c23531"},
         label_opts=opts.LabelOpts(font_size=65,color="#c23531",position="inside",border_color="#c23531"))
    .set_global_opts(title_opts=opts.TitleOpts(title="China",pos_left="center",pos_bottom="10%",
                                               title_textstyle_opts=opts.TextStyleOpts(font_size=50,color="#c23531")))

).render("lq1.html")
