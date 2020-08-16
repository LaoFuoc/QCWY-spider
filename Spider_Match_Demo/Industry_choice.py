#encoding: utf-8
from pyecharts import options as opts
from pyecharts.charts import Bar,  Page ,Pie


def Industry_choice(get_data):
    Software = get_data[get_data['行业'].str.contains('计算机软件', case=False)]
    Hardware = get_data[get_data['行业'].str.contains('计算机硬件', case=False)]
    Service = get_data[get_data['行业'].str.contains('计算机服务', case=False)]
    Communication = get_data[get_data['行业'].str.contains('通信', case=False)]
    Internet = get_data[get_data['行业'].str.contains('互联网', case=False)]

    # 统计行业占比，制作饼图
    Industry = ['计算机软件', '计算机硬件', '计算机服务', '通信', '互联网\n电子商务']
    value = [len(Software), len(Hardware), len(Service), len(Communication), len(Internet)]

    # 统计行业平均薪资,制作柱状图
    attrs = [Software, Hardware, Service, Communication, Internet]
    Avg_sala = []
    for attr in attrs:
        sums = [sala for sala in attr['平均薪资'] if type(sala) == int]  # 工资列表
        avg = int(sum(sums) / int(len(sums)))  # 平均工资
        Avg_sala.append(avg)

    # print(Avg_sala)#行业所对应的平均薪资

    def pie_base() -> Pie:
        c = (
            Pie()
                .add("", [list(z) for z in zip(Industry, value)], center=["50%", "50%"],  # 相对容器的宽度，高度，百分比
                     )
                # .set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"])
                .set_global_opts(title_opts=opts.TitleOpts(title="行业数量占比图", pos_left='center'),
                                 legend_opts=opts.LegendOpts(pos_left="2%", pos_top="25%", orient="vertical")  # 设置图例的属性
                                 )
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )

        return c

    def overlap_bar_line() -> Bar:
        bar = (
            Bar()
                .add_xaxis(Industry)
                .add_yaxis("平均薪资", Avg_sala, category_gap="50%")
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(
                title_opts=opts.TitleOpts(title="平均薪资"),
                yaxis_opts=opts.AxisOpts(
                    axislabel_opts=opts.LabelOpts(formatter="{value} /月")),
            )
                .set_series_opts(
                itemstyle_opts={'color': '#00a6ac'},
                label_opts=opts.LabelOpts(is_show=False),
                markline_opts=opts.MarkPointOpts(
                    data=[
                        opts.MarkPointItem(type_="max", name="最大值"),
                        opts.MarkLineItem(type_="average", name="平均值")])
            )
        )

        return bar

    page = Page()
    page.add(pie_base(), overlap_bar_line())
    page.render('行业选择-招聘薪资对比图.html')

