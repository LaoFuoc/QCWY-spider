# encoding: utf-8
import tkinter.messagebox
import webbrowser
from tkinter import *

import jieba
import pandas as pd
import pymongo
from pyecharts import options as opts
from pyecharts.charts import Bar, Page, Pie, WordCloud, Line, Map


class App:

    def __init__(self, master):
        self.master = master
        self.initWidgets()

    def initWidgets(self):
        def DiQuXinZi():
            webbrowser.open_new('地区薪资分布图.html')

        def XueLiXinZi():
            webbrowser.open_new('学历薪资图.html')

        def JingYanXinZi():
            webbrowser.open_new('经验-薪资对比图.html')

        def GongSiFuLi():
            webbrowser.open_new('公司福利词云图.html')

        def ChaXun():
            Gangwei = self.txt1.get()
            City = self.txt2.get()
            df.drop_duplicates(['职位信息'], inplace=True)
            get_data = df[df['工作岗位'].str.contains('{}'.format(Gangwei), case=False)]
            # self.txt3.set("数据表：" + collection.name + "--包含数据%s条" % len(get_data))
            self.txt3.set('正在生成！')
            City_Salary(get_data, City)
            One_avgs = [One_City(get_data, i, City) for i in edul]
            bar_same_series_gap(edul, City, One_avgs).render('学历薪资图.html')
            Get_Photo(get_data, City)
            FuLiCiYun(get_data, City)
            self.txt3.set('生成完成，请查看！')

        self.txt1 = StringVar()
        self.txt2 = StringVar()
        self.txt3 = StringVar()
        self.txt1.set('java')
        self.txt2.set('重庆')
        # 这里是队名Logo
        global photo
        photo = PhotoImage(file='redafine.png')

        fm = Frame(self.master)
        fm.pack(side=LEFT, fill=BOTH, expand=NO, )
        Button(fm, text='Redafine', image=photo, relief=RIDGE).pack(side=TOP, fill=X, expand=NO, padx=5, pady=5)

        # 顶部
        fmTop = Frame(self.master)
        fmTop.pack(side=TOP, fill=BOTH, expand=NO, padx=150)
        Entry(fmTop, textvariable=self.txt1, width=14, font=('楷体', 16),
              relief=RIDGE).pack(side=LEFT, expand=NO, fill=X, padx=20, pady=10)
        Label(fmTop, text="岗位、关键字", font=('思源黑体')).pack(side=LEFT, expand=NO, fill=Y, padx=0, pady=10)
        Entry(fmTop, textvariable=self.txt2, width=14, font=('楷体', 16),
              relief=RIDGE).pack(side=LEFT, expand=NO, fill=X, padx=20, pady=10)
        Label(fmTop, text="城市选择", font=('思源黑体')).pack(side=LEFT, expand=NO, fill=Y, pady=10)
        Button(fmTop, text='点击查询', command=ChaXun, font=('思源黑体'), height=2, width=10, relief=RIDGE).pack(side=RIGHT,
                                                                                                         fill=X,
                                                                                                         expand=NO,
                                                                                                         padx=20,
                                                                                                         pady=10)

        # 左边导航栏
        fm1 = Frame(fm)
        fm1.pack(side=LEFT, fill=Y, expand=NO, pady=60)
        Button(fm1, text='地区薪资', height=3, command=DiQuXinZi, width=20, font=('思源黑体'), relief=RIDGE).pack(side=TOP,
                                                                                                          fill=X,
                                                                                                          padx=10)
        Button(fm1, text='学历薪资', height=3, command=XueLiXinZi, font=('思源黑体'), relief=RIDGE).pack(side=TOP, fill=X,
                                                                                                 pady=10,
                                                                                                 padx=10)
        Button(fm1, text='经验薪资', height=3, command=JingYanXinZi, font=('思源黑体'), relief=RIDGE).pack(side=TOP, fill=X,
                                                                                                   padx=10)
        Button(fm1, text='公司福利', height=3, command=GongSiFuLi, font=('思源黑体'), relief=RIDGE).pack(side=TOP, fill=X,
                                                                                                 pady=10, padx=10)

        # 这里是主体
        monty = LabelFrame(root, text="数据系统", font=('思源黑体', 16), width=300, padx=30, )
        monty.pack(side=LEFT, fill=Y, expand=NO, padx=30)  # expand，是否随窗体大小改变而改变位置

        can = tkinter.Canvas(monty, bg='#afdfe4')
        can.pack(expand=YES, fill=BOTH)
        Label(can, textvariable=self.txt3, relief='ridge', font=('思源黑体', 12), width=100).grid(row=0, column=1, pady=10,
                                                                                              padx=50)


def bar_same_series_gap(edul, City, One_avgs) -> Bar:
    c = (
        Bar()
            .add_xaxis(edul)
            .add_yaxis("{}".format(City), One_avgs, category_gap="50%")
            .set_global_opts(title_opts=opts.TitleOpts(title="{}地区-学历薪资".format(City)))
    )
    return c


def City_Salary(get_data, City_name):
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

    attr, value = Area_Salary()
    sala = []
    for i in attr:
        work_sa = work_salas[work_salas['地区'].str.contains('{}'.format(i))]
        sums = [sala for sala in work_sa['平均薪资'] if type(sala) == int]
        avg = int(sum(sums) / int(len(sums)))
        sala.append(avg)

    print(sala)

    def map_guangdong() -> Map:
        c = (
            Map()
                .add("{}".format(City_name), [list(z) for z in zip(attr, value)], "{}".format(City_name))
                .set_global_opts(
                title_opts=opts.TitleOpts(title="{}地区-岗位分布".format(City_name)),
                visualmap_opts=opts.VisualMapOpts(),
            )
        )
        return c

    def bar_same_series_gap() -> Bar:
        c = (
            Bar()
                .add_xaxis(attr)
                .add_yaxis("{}".format(City_name), sala, category_gap="50%")
                .set_global_opts(title_opts=opts.TitleOpts(title="{}地区-薪资分布".format(City_name)))
                .set_series_opts(
                label_opts=opts.LabelOpts(is_show=False),
                markpoint_opts=opts.MarkPointOpts(
                    data=[
                        opts.MarkPointItem(type_="max", name="最大值"),
                        opts.MarkPointItem(type_="min", name="最小值"),
                        opts.MarkPointItem(type_="average", name="平均值"),
                    ])
            )
        )
        return c

    page = Page()
    page.add(map_guangdong(), bar_same_series_gap())
    page.render('地区薪资分布图.html')

    return sala, attr, value


def One_City(get_data, Edu_name, City):
    One_City = get_data[get_data['城市'].str.contains('{}'.format(City))]
    work_salas = One_City[One_City['学历要求'].str.contains('{}'.format(Edu_name))]
    CQ_sum = [sala for sala in work_salas['平均薪资'] if type(sala) == int]  # 工资列表
    try:
        if len(CQ_sum) < 3:  # 过滤掉只包含三个职位的学历
            avg = 0
        else:
            avg = int(sum(CQ_sum) / int(len(CQ_sum)))
    except:
        avg = 0
    return avg


def Get_Photo(get_data, City_name):
    work = ['3-4年经验', '无工作经验', '5-7年经验', '2年经验', '1年经验', '8-9年经验', '10年以上经验']
    workyear = ['无工作经验', '1年经验', '2年经验', '3-4年经验', '5-7年经验', '8-9年经验', '10年以上经验']
    Data = get_data[get_data['城市'].str.contains('{}'.format(City_name))]
    print("得到有效数据%s条" % len(Data))
    """计算不同工作经验对应的平均薪资"""

    def Work_Salary(Work_name):

        work_salas = Data[Data['工作经验'].str.contains('{}'.format(Work_name))]
        sums = [sala for sala in work_salas['平均薪资'] if type(sala) == int]  # 工资列表
        try:
            avg = int(sum(sums) / int(len(sums)))
        except:
            avg = 0

        return avg

    All_avgs = [Work_Salary(i) for i in workyear]
    print('平均薪资', All_avgs)

    # 工作经验部分,排序处理
    def workyear_ChuLi(Data):
        value_workyear = []
        for i in workyear:
            try:
                value_workyear.append(int(Data[i]))
            except:
                value_workyear.append(0)
        return value_workyear

    # 统计工作经验对应得岗位数量
    Data1 = Data['工作经验'].value_counts()
    value_workyear1 = workyear_ChuLi(Data1)
    print(workyear)
    print(value_workyear1)

    """工作经验文本饼图"""

    def pie_rich_label() -> Pie:
        c = (
            Pie()
                .add(
                "",
                [list(z) for z in zip(workyear, value_workyear1)],
                radius=["40%", "55%"],
                label_opts=opts.LabelOpts(
                    position="outside",
                    formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                    background_color="#eee",
                    border_color="#aaa",
                    border_width=1,
                    border_radius=4,
                    rich={
                        "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                        "abg": {
                            "backgroundColor": "#e3e3e3",
                            "width": "100%",
                            "align": "right",
                            "height": 22,
                            "borderRadius": [4, 4, 0, 0],
                        },
                        "hr": {
                            "borderColor": "#aaa",
                            "width": "100%",
                            "borderWidth": 0.5,
                            "height": 0,
                        },
                        "b": {"fontSize": 16, "lineHeight": 33},
                        "per": {
                            "color": "#eee",
                            "backgroundColor": "#334455",
                            "padding": [2, 4],
                            "borderRadius": 2,
                        },
                    },
                ),
            )
                .set_global_opts(
                title_opts=opts.TitleOpts(title="{}Java岗位-工作经验需求占比".format(City_name), pos_left='center'),
                legend_opts=opts.LegendOpts(
                    orient="vertical", pos_top="5%", pos_left="1%")
                )
        )
        return c

    def overlap_bar_line() -> Bar:
        bar = (
            Bar()
                .add_xaxis(workyear)
                .add_yaxis("岗位数量", value_workyear1, category_gap="50%")
                .extend_axis(
                yaxis=opts.AxisOpts(
                    axislabel_opts=opts.LabelOpts(formatter="{value} /月"), interval=5000
                )
            )
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(
                title_opts=opts.TitleOpts(title="{}岗位数量-平均薪资对比图".format(City_name)),
                yaxis_opts=opts.AxisOpts(
                    axislabel_opts=opts.LabelOpts(formatter="{value} 个")
                ),
            )
        )

        line = Line().add_xaxis(workyear).add_yaxis("平均薪资", All_avgs, yaxis_index=1, is_smooth=True) \
            .set_global_opts(title_opts=opts.TitleOpts(title="Line-smooth"))

        bar.overlap(line)
        return bar

    page = Page()
    page.add(pie_rich_label(), overlap_bar_line())
    page.render('经验-薪资对比图.html'.format(City_name))


def FuLiCiYun(get_data, City_name):
    Data = get_data[get_data['城市'].str.contains('{}'.format(City_name))]
    max = len(Data)
    information = Data['公司福利']
    txtl = jieba.cut(' '.join(information), cut_all=False)  # jieba分词
    txt = ' '.join(txtl).replace('\n', ' ').lower()
    china = re.sub('[0-9a-zA-Z_]', '', txt)  # 保留汉字
    for i in '!"#$%&()*+, （）【】，；0．！、：。-./:;<=>?@[\\]^_‘{|}~':
        china = china.replace(i, " ")  # 将文本中特殊字符替换为空格
    print("请稍等，正在生成")

    Idioms = china.split()
    Icounts = {}
    for Idiom in Idioms:
        if len(Idiom) < 2:  # 过滤掉单个字
            continue
        else:
            Icounts[Idiom] = Icounts.get(Idiom, 0) + 1
    chinas = list(Icounts.items())
    chinas.sort(key=lambda x: x[1], reverse=True)

    def wordcloud_base() -> WordCloud:
        c = (
            WordCloud()
                .add("", chinas, word_size_range=[20, 100])
                .set_global_opts(title_opts=opts.TitleOpts(title="岗位要求"))
        )
        return c

    wordcloud_base().render(('公司福利词云图.html'))


def main():
    global root, df, edul, collection, df
    root = Toplevel()
    root.title("单个城市岗位数据分析")
    root.geometry("1200x800")
    display = App(root)

    client = pymongo.MongoClient()
    collection = client['51Job']['Scrapy']
    data = collection.find()
    df = pd.DataFrame(data)
    edul = ['不限', '中技', '中专', '大专', '本科', '硕士']

    root.mainloop()


if __name__ == '__main__':
    main()
