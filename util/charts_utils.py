# encoding: utf-8
"""
@author: zhou
@time: 2021/12/1 11:03
@file: charts_utils.py
@desc: 绘图相关的方法
"""

from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Sunburst
from pyecharts.charts import Graph as LinkGraph


# 旭日图绘制方法
def sunburst_draw(data, title=""):
    sun_charts = (
        # theme=ThemeType.DARK
        # width="1500px", height="1000px"
        Sunburst(init_opts=opts.InitOpts(width="800px", height="800px"))
            .add(
            "",
            data_pair=data,  # 数据Sequence
            highlight_policy="self",  # 当鼠标移动到一个扇形块时，可以高亮相关的扇形块。
            # 'ancestor'：高亮该扇形块和祖先元素
            radius=[0, "90%"],  # 图的半径,第一项是内半径，第二项是外半径
            levels=[
                {
                    "itemStyle": {},
                    "label": {"rotate": "tangential"},
                },
                {
                    "itemStyle": {},
                    "label": {"rotate": "tangential"},
                },
                {
                    "itemStyle": {},
                },
                {
                    "itemStyle": {},
                },
                {"label": {"align": "right"}},
                {
                    # "label": {"position": "outside", "padding": 2, "silent": False},
                    # "itemStyle": {"borderWidth": 3},
                },
            ],
        )
            .set_global_opts(title_opts=opts.TitleOpts(title=title))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}"))
    )
    sun_charts.render(title + ".html")


# 柱状图绘制方法
def line_draw(data_dict, title=""):
    columns = list(data_dict.keys())
    data = list(data_dict.values())

    bar = (
        Bar()
            .add_xaxis(columns)
            .add_yaxis("数量", data)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
            .set_global_opts(title_opts=opts.TitleOpts(title=title
                                                       , pos_left='50%'  # 标题的位置 距离左边20%距离
                                                       ),
                             xaxis_opts=opts.AxisOpts(name_rotate=60
                                                      , axislabel_opts={"rotate": 30}),  # x轴设置
                             legend_opts=opts.LegendOpts(is_show=False  # 关闭图例
                                                         , type_=None  # 'plain'：普通图例。缺省就是普通图例。
                                                         # 'scroll'：可滚动翻页的图例。当图例数量较多时可以使用。
                                                         , pos_left='right'  # 图例横向的位置,right表示在右侧，也可以为百分比
                                                         , pos_top='middle'  # 图例纵向的位置，middle表示中间，也可以为百分比
                                                         , orient='vertical'  # horizontal #图例方式的方式
                                                         ),
                             # datazoom_opts=opts.DataZoomOpts(),  # 横轴滚动
                             )
    )
    # ThemeType.DARK
    Grid().add(
        bar,  # 图表实例，仅Chart类或者其子类
        # 直角坐标系网格配置项
        # grid 组件离容器左侧的距离。
        # left 的值可以是像 20 这样的具体像素值，可以是像 '20%' 这样相对于容器高宽的百分比，
        # 也可以是 'left', 'center', 'right'。
        # 如果 left 的值为'left', 'center', 'right'，组件会根据相应的位置自动对齐。
        grid_opts=opts.GridOpts(pos_left="10%", is_contain_label=True)).render("grid.html")
    # make_snapshot(snapshot, grid.render(), "test.png")  # 仅支持中文路径


# 节点图绘制方法
def graph_draw(nodes, links, title=""):
    graph = (
        LinkGraph(init_opts=opts.InitOpts(width="800px", height="800px"))
            .add("", nodes, links, repulsion=1500, edge_symbol=['', 'arrow'], symbol_size=30,
                 # edge_label=opts.LabelOpts(is_show=True, position="middle", formatter="{c}"),
                 linestyle_opts=opts.LineStyleOpts(width=0.5, curve=0.2, opacity=0.7),
                 is_roam=True,
                 is_focusnode=True,
                 )
            .set_global_opts(title_opts=opts.TitleOpts(title=title))
    ).render(title + ".html")
