#encoding: utf-8
from tkinter import *
import tkinter.messagebox
import pandas as pd
import pymongo
import webbrowser
import jieba
import random
from pyecharts import options as opts
from pyecharts.charts import Bar,  Page , Pie, Geo, WordCloud, Radar, Scatter, Line, Map
from pyecharts.globals import ChartType
from Gui_One_City import main

class App:

    def __init__(self, master):
        self.master = master
        self.initWidgets()

    def initWidgets(self):

        def HangYe():
            webbrowser.open_new('行业选择-招聘薪资对比图.html')

        def GangWei():
            webbrowser.open_new('全国岗位分布薪资分布图.html')

        def TiSheng():
            webbrowser.open_new('专业能力提升技能雷达图.html')

        def FaZhanDiDian():
            webbrowser.open_new('发展地点-平均薪资对比图.html')

        def ChaXun():
            hangye = self.txt1.get()
            Gangwei = self.txt2.get()
            self.txt3.set("数据表：" + collection.name + "--包含数据%s条" % len(df))
            get_data = df[df['工作岗位'].str.contains('{}'.format(Gangwei), case=False)]
            if hangye!='':
                get_data = df[df['行业'].str.contains('{}'.format(hangye), case=False)]
                tkinter.messagebox.showinfo('提示', "正在查询\n--" + Gangwei + '--\n--' + hangye + '--行业,' + "相关职位，\n请耐心等候")
                self.txt3.set("查找到--%s--%s行业--有效数据%s条" % (Gangwei, hangye, len(get_data)))
                Industry_choice(get_data)
                Post_distribution(get_data)
                Lifting_direction(get_data, city='')
                Location_development(get_data)

            else:
                tkinter.messagebox.showinfo('提示', "正在查询\n--" + Gangwei + '--\n--' + hangye + '--行业,' + "相关职位，\n请耐心等候")
                self.txt3.set("查找到--%s--%s行业--有效数据%s条" % (Gangwei, hangye, len(get_data)))
                Industry_choice(get_data)
                Post_distribution(get_data)
                Lifting_direction(get_data,city='')
                Location_development(get_data)

            self.txt3.set('查询完成，点击查看!')


        self.txt1 = StringVar()
        self.txt2 = StringVar()
        self.txt3 = StringVar()
        self.txt2.set('java')
        #这里是队名Logo
        global photo
        photo = PhotoImage(file='redafine.png')

        fm = Frame(self.master)
        fm.pack(side=LEFT, fill=BOTH, expand=NO, )
        Button(fm, text='Redafine', image=photo,relief=RIDGE).pack(side=TOP, fill=X, expand=NO,padx=5,pady=5)

        #顶部
        fmTop = Frame(self.master)
        fmTop.pack(side=TOP, fill=BOTH, expand=NO, padx=150)
        Entry(fmTop, textvariable=self.txt1, width=14, font=('楷体', 16),
              relief=RIDGE).pack(side=LEFT, expand=NO, fill=X, padx=20, pady=10)
        Label(fmTop, text="行业方向", font=('思源黑体')).pack(side=LEFT, expand=NO, fill=Y,padx=0, pady=10)
        Entry(fmTop, textvariable=self.txt2, width=14, font=('楷体', 16),
              relief=RIDGE).pack(side=LEFT, expand=NO, fill=X, padx=20, pady=10)
        Label(fmTop, text="岗位关键字", font=('思源黑体')).pack(side=LEFT, expand=NO, fill=Y,pady=10)
        Button(fmTop, text='点击查询',command=ChaXun,font=('思源黑体'), height=2,width=10,relief=RIDGE).pack(side=RIGHT,
                                                 fill=X, expand=NO,padx=20,pady=10)

        # 左边导航栏
        fm1 = Frame(fm)
        fm1.pack(side=LEFT, fill=Y, expand=NO,pady=60)
        # Button(fm1, text='专业选择',    height=3,command=ZhuanYe,width=20,font=('思源黑体'),relief=RIDGE).pack(side=TOP, fill=X,pady=10,padx=10)
        Button(fm1, text='行业选择',height=3,command=HangYe,width=20,font=('思源黑体'),relief=RIDGE).pack(side=TOP, fill=X,padx=10 )
        Button(fm1, text='岗位分布',    height=3,command=GangWei,font=('思源黑体'),relief=RIDGE).pack(side=TOP, fill=X, pady=10 ,padx=10)
        Button(fm1, text='提升方向',    height=3,command=TiSheng,font=('思源黑体'),relief=RIDGE).pack(side=TOP, fill=X, padx=10 )
        Button(fm1, text='发展地点选择',    height=3,command=FaZhanDiDian,font=('思源黑体'),relief=RIDGE).pack(side=TOP, fill=X,pady=10,padx=10 )
        Button(fm1, text='单个城市分析', height=3, command=main, font=('思源黑体'), relief=RIDGE).pack(side=TOP, fill=X, pady=0,padx=10)

        #这里是主体
        monty = LabelFrame(root, text="数据系统",font=('思源黑体',16), width=300,padx=30)
        monty.pack(side=LEFT, fill=Y, expand=NO,padx=30)#expand，是否随窗体大小改变而改变位置

        can = tkinter.Canvas(monty, bg='#afdfe4')
        can.pack(expand=YES, fill=BOTH)
        Label(can, textvariable=self.txt3, relief='ridge', font=('思源黑体',12),width=100).grid(row=0,column=1,pady=10,padx=50)

def Industry_choice(get_data):

    Software = get_data[get_data['行业'].str.contains('软件', case=False)]
    Hardware = get_data[get_data['行业'].str.contains('硬件', case=False)]
    Service = get_data[get_data['行业'].str.contains('服务', case=False)]
    Communication = get_data[get_data['行业'].str.contains('通信', case=False)]
    Internet = get_data[get_data['行业'].str.contains('互联网', case=False)]

    # 统计行业占比，制作饼图
    Industry = ['软件', '硬件', '服务', '通信', '互联网\n电子商务']
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
                                 legend_opts=opts.LegendOpts(pos_left="2%", pos_top="25%", orient="vertical")
                                 # 设置图例的属性
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


def Post_distribution(get_data):
    def Get_Top_attr_value(name):
        Data = get_data['{}'.format(name)].str.lower().value_counts()
        attr = list(Data.index)  # 列表形式，统计名称
        value = [int(i) for i in list(Data.values)]

        return attr, value

    """城市-平均薪资"""

    def City_Salary(City_name):
        work_salas = get_data[get_data['城市'].str.contains('{}'.format(City_name))]
        sums = [sala for sala in work_salas['平均薪资'] if type(sala) == int]  # 工资列表
        avg = int(sum(sums) / int(len(sums)))  # 平均工资

        def Area_Salary():
            Data = work_salas['地区'].value_counts()
            attr = list(Data.index)
            value = [int(i) for i in list(Data.values)]
            print(attr)  # 统计地区
            print(value)  # 统计地区的数量

            return attr, value  # 返回地区以及对应的数量


        return avg  # 返回平均薪资

    citys, values = Get_Top_attr_value('城市')
    citys = [i.replace('省','') for i in citys  ]
    print(citys)  # 各城市
    print(values)  # 城市招聘信息数量
    print(len(citys))
    if int(len(citys)) >120:
        citys = citys[:120]
        values = values[:120]
    else:
        citys = citys
        values = values
    City_Avg_Salary = []  # 各城市平均薪资
    for i in citys:
        try:
            Avg = City_Salary(i)
            if i == '异地招聘':
                continue
            else:
                City_Avg_Salary.append(Avg)
        except:
            Avg = 0
            City_Avg_Salary.append(Avg)

    def geo_base() -> Geo:
        c = (
            Geo()
                .add_schema(maptype="china", )
                .add('', [list(z) for z in zip(citys, values)], symbol_size=16,
                     type_=ChartType.EFFECT_SCATTER, )
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(visualmap_opts=opts.VisualMapOpts(is_calculable=True, min_=0, max_=2000,
                                                                   pos_top='center',
                                                                   ),  # 调整图例参数
                                 title_opts=opts.TitleOpts(title="全国Java招聘数量分布图", pos_left='center')
                                 )
        )

        return c

    def geo_heatmap() :
        c = (
            Geo()
                .add_schema(maptype="china")
                .add(
                "",
                [list(z) for z in zip(citys[:120], City_Avg_Salary[:120])],
                type_=ChartType.HEATMAP,
            )
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(pos_top='center', min_=0, max_=15000, ),
                title_opts=opts.TitleOpts(title="全国Java薪资分布图", pos_left='center'),
            )
        )
        # c = (
        #     Map()
        #         .add("", [list(z) for z in zip(citys[:120], City_Avg_Salary[:120])], "china")
        #         .set_global_opts(
        #         title_opts=opts.TitleOpts(title="全国Java薪资分布图", pos_left='center'),
        #         visualmap_opts=opts.VisualMapOpts(max_=15000),
        #     )
        # )
        return c

    page = Page()
    page.add(geo_base(), geo_heatmap())
    page.render('全国岗位分布薪资分布图.html')


def Lifting_direction(get_data,city):
    def Skills(City_name):
        get_data = df[df['工作岗位'].str.contains('java', case=False)]
        Data = get_data[get_data['城市'].str.contains('{}'.format(City_name))]
        print("得到有效数据%s条" % len(Data))
        max = len(Data)
        information = Data['职位信息']
        txtl = jieba.cut(' '.join(information), cut_all=False)  # jieba分词
        txt = ' '.join(txtl).replace('\n', ' ').lower()

        # for i in '!"#$%&()*+, ，、：。-./:;<=>?@[\\]^_‘{|}~':
        #     Txtx = txt.replace(i, "")  # 将文本中特殊字符替换为空格

        china = re.sub('[0-9a-zA-Z_]', '', txt)  # 保留汉字
        text = re.sub('[\u4e00-\u9fa5]', '', txt)  # 去除汉字
        for i in '!"#$%&()*+, （）【】，；0．！、：。-./:;<=>?@[\\]^_‘{|}~':
            china = china.replace(i, " ")  # 将文本中特殊字符替换为空格
            text = text.replace(i, ' ')
        print("请稍等，正在生成")

        Idioms = china.split()
        Icounts = {}
        for Idiom in Idioms:
            if len(Idiom) < 2:  # 过滤掉单个字
                continue
            else:
                Icounts[Idiom] = Icounts.get(Idiom, 0) + 1
        Idiom = {'工作', '相关', '以及', '能力', '使用', '以上', '职能', '类别', '要求', '具有',
                 '进行', '产品', '任职', '具备', '关键', '关键字', '岗位', '资格', '内容', '参与', '编写', '以上学历', '公司', '岗位职责'}
        for i in Idiom:
            try:
                del (Icounts[i])
            except:
                continue
        chinas = list(Icounts.items())
        chinas.sort(key=lambda x: x[1], reverse=True)
        # for i in range(50):
        #     china, counts = chinas[i]
        #     print("{0:<5}->{1:>5}".format(china, counts))

        words = text.split()  # 对字符串进行分割，获得单词列表
        counts = {}
        for word in words:
            if len(word) < 2:  # 过滤掉单个字母
                continue
            else:
                counts[word] = counts.get(word, 0) + 1
        word = {'and', 'the', 'with', 'in', 'by', 'for', 'of', 'an', 'to'}  # 排除特定的单词
        for i in word:
            try:
                del (counts[i])
            except:
                continue
        # 生成元组列表，并进行降序排列
        items = list(counts.items())
        items.sort(key=lambda x: x[1], reverse=True)

        for i in range(20):
            word, count = items[i]
            print("{0:<5}->{1:>5}".format(word, count))

        return items, max, chinas

    def radar_selected_mode() -> Radar:
        DaLuan = lists[1:10]
        print(lists[:10])
        random.shuffle(DaLuan)
        print(DaLuan)
        c = (
            Radar()
                .add_schema(textstyle_opts={'color': '#c7a252', "fontSize": 16, },  # 文字样式的颜色
                            schema=[
                                opts.RadarIndicatorItem(name=lists[0][0], max_=max),
                                opts.RadarIndicatorItem(name=DaLuan[0][0], max_=max),
                                opts.RadarIndicatorItem(name=DaLuan[1][0], max_=max),
                                opts.RadarIndicatorItem(name=DaLuan[2][0], max_=max),
                                opts.RadarIndicatorItem(name=DaLuan[3][0], max_=max),
                                opts.RadarIndicatorItem(name=DaLuan[4][0], max_=max),
                                opts.RadarIndicatorItem(name=DaLuan[5][0], max_=max),
                                opts.RadarIndicatorItem(name=DaLuan[6][0], max_=max),
                                opts.RadarIndicatorItem(name=DaLuan[7][0], max_=max),
                                opts.RadarIndicatorItem(name=DaLuan[8][0], max_=max),
                            ],
                            )
                .add("Top10能力要求", [[max] + [DaLuan[i][1] for i in range(0, 9)]],
                     areastyle_opts={"color": '#009ad6'}, linestyle_opts={"color": '#009ad6'})
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(
                legend_opts=opts.LegendOpts(selected_mode="single"),
                title_opts=opts.TitleOpts(title="岗位技能雷达图"),
            )
        )
        return c

    def wordcloud_base() -> WordCloud:
        c = (
            WordCloud()
                .add("", chinas[:100], word_size_range=[20, 100])
                .set_global_opts(title_opts=opts.TitleOpts(title="岗位要求"))
        )
        return c

    lists, max, chinas = Skills('{}'.format(city))
    page = Page()
    page.add(wordcloud_base(), radar_selected_mode())
    page.render('专业能力提升技能雷达图.html')


# edu = ['本科', '大专', '不限', '硕士', '中专', '中技']
def Location_development(get_data):
    """学历要求-平均薪资"""
    # 全国部分
    def Edu_Salary(Edu_name):
        work_salas = get_data[get_data['学历要求'].str.contains('{}'.format(Edu_name))]
        sums = [sala for sala in work_salas['平均薪资'] if type(sala) == int]  # 工资列表
        avg = int(sum(sums) / int(len(sums)))

        return avg

    # 单个城市
    def One_City(Edu_name, city):
        work_salas = get_data[get_data['学历要求'].str.contains('{}'.format(Edu_name))]
        ChongQing = work_salas[work_salas['城市'].str.contains('{}'.format(city))]
        CQ_sum = [sala for sala in ChongQing['平均薪资'] if type(sala) == int]  # 工资列表
        try:
            if len(CQ_sum) < 10:  # 过滤掉只包含个职位的学历
                avg = 0
            else:
                avg = int(sum(CQ_sum) / int(len(CQ_sum)))
        except:
            avg = 0
        return avg

    edul = ['不限', '中技', '中专', '大专', '本科', '硕士']

    # 单个城市，招聘数量统计
    def A_Ctiys(city):
        value_edul = []
        A_City = get_data[get_data['城市'].str.contains('{}'.format(city))]
        Data1 = A_City['学历要求'].value_counts()
        for i in edul:
            try:
                value_edul.append(int(Data1[i]))
                # if int(Data1[i]) == 1:
                #     value_edul.append(0)
                # else:
                #     value_edul.append(int(Data1[i]))
            except:
                value_edul.append(0)
        return value_edul

    value_edu1 = A_Ctiys('重庆')
    value_edu2 = A_Ctiys('北京')
    value_edu3 = A_Ctiys('上海')
    value_edu4 = A_Ctiys('广州')
    value_edu5 = A_Ctiys('深圳')
    value_edu6 = A_Ctiys('成都')
    print(edul)
    print('重庆', value_edu1, '\n', '北京', value_edu2, '\n', '上海', value_edu3,
          '\n', '广州', value_edu4, '\n', '深圳', value_edu5, '\n', '成都', value_edu6)

    All_avgs = [Edu_Salary(i) for i in edul]  # 所有城市平均薪资
    One_avgs = [One_City(i, '重庆') for i in edul]  # 单个城市平均薪资
    Two_avgs = [One_City(i, '北京') for i in edul]
    Three_avgs = [One_City(i, '上海') for i in edul]
    Four_avgs = [One_City(i, '广州') for i in edul]
    Five_avgs = [One_City(i, '深圳') for i in edul]
    Six_avgs = [One_City(i, '成都') for i in edul]

    def bar_markline_type() -> Bar:
        c = (
            Bar()
                .add_xaxis(edul)
                .add_yaxis("全国", All_avgs, category_gap="50%")
                .add_yaxis("重庆", One_avgs, category_gap="50%")
                .reversal_axis()
                .set_global_opts(title_opts=opts.TitleOpts(title="Java岗位学历平均薪资"))
                .set_series_opts(
                label_opts=opts.LabelOpts(position="right"),
                markline_opts=opts.MarkLineOpts(
                    # data=[
                    #     opts.MarkLineItem(type_="min", name="最小值"),
                    #     opts.MarkLineItem(type_="max", name="最大值"),
                    #     opts.MarkLineItem(type_="average", name="平均值"),
                    # ]
                )
            )
        )
        return c

    def line_smooth() -> Line:
        c = (
            Line()
                .add_xaxis(edul)
                .add_yaxis("重庆", value_edu1, is_smooth=True)
                .add_yaxis("北京", value_edu2, is_smooth=True)
                .add_yaxis("上海", value_edu3, is_smooth=True)
                .add_yaxis("广州", value_edu4, is_smooth=True)
                .add_yaxis("深圳", value_edu5, is_smooth=True)
                .add_yaxis("成都", value_edu6, is_smooth=True)
                .set_global_opts(title_opts=opts.TitleOpts(title="一线城市招聘数量对比图"))
        )
        return c

    def scatter_visualmap_color() -> Scatter:
        c = (
            Scatter()
                .add_xaxis(edul)
                .add_yaxis("重庆", One_avgs)
                .add_yaxis("北京", Two_avgs)
                .add_yaxis("上海", Three_avgs, is_selected=False)
                .add_yaxis("广州", Four_avgs, is_selected=False)
                .add_yaxis("深圳", Five_avgs, is_selected=False)
                .add_yaxis("成都", Six_avgs, is_selected=False)
                .set_global_opts(
                title_opts=opts.TitleOpts(title="一线城市平均薪资对比图"),
                visualmap_opts=opts.VisualMapOpts(type_="size", max_=22000, min_=0),
            )
        )
        return c

    page = Page()
    page.add(bar_markline_type(), line_smooth(), scatter_visualmap_color())
    page.render('发展地点-平均薪资对比图.html')


root = Tk()
root.title("全国招聘网站数据分析")
root.geometry("1200x800")
display = App(root)

client = pymongo.MongoClient()
collection = client['51Job']['Scrapy']
data = collection.find()
df = pd.DataFrame(data)
df.drop_duplicates(['职位链接'], inplace=True)

root.mainloop()
