import matplotlib.pyplot as plt
import numpy as np
from Read_Data import read_data, calc_climb_rate


colors = ['#b00758', '#c80d44', '#de0c2f', '#d31014', '#da2713', '#e53422',
          '#e84b14', '#db3f0e', '#e8450e', '#e05325', '#da5c21', '#d56830',
          '#f3790c', '#ed8222', '#ee980f', '#f3a328', '#db942c', '#deb92d',
          '#dbcf2b', '#c5dc29', '#acdd2c', '#79dc27', '#3dcd20', '#28d44a',
          '#32cd4e', '#38ca5d', '#39bd5a', '#4bb27d', '#49a284', '#5bbaa4',
          '#59a49f', '#578a8d', '#577b93']


def plot_rose_0(data=None):
    plot_data = data.head(20)
    # 数据计算，这里只取前20个国家
    radius = np.array(plot_data['Confirmed'].tolist())
    n = len(radius)
    theta = np.arange(0, 2 * np.pi, 2 * np.pi / n) + 2 * np.pi / (2 * n)  # 360度分成20分，外加偏移
    # 在画图时用到的 plt.cm.spring_r(r)   r的范围要求时[0,1]
    radius_normalized = (radius - radius.min()) / (radius.max() - radius.min())  # x-min/max-min   归一化
    radius_normalized -= 0.1

    # 画图
    fig = plt.figure(figsize=(30, 30), dpi=300)
    ax = fig.add_subplot(projection='polar')  # 启用极坐标
    bar = ax.bar(theta, radius, width=2 * np.pi / n, bottom=64)
    ax.set_theta_zero_location('N')  # 分别为N, NW, W, SW, S, SE, E, NE
    ax.set_rgrids([])  # 用于设置极径网格线显示
    ax.set_thetagrids([])  # 用于设置极坐标角度网格线显示
    ax.set_title('COVID-19 2020-4-27')  # 设置标题
    # 设置扇形各片的颜色
    for r, bar in zip(radius_normalized, bar):
        bar.set_facecolor(plt.cm.spring_r(r))
        bar.set_alpha(0.8)
    # 设置边框显示
    for key, spine in ax.spines.items():
        if key == 'polar':
            spine.set_visible(False)
    plt.show()
    # 保存图片
    # fig.savefig('COVID.png')


def plot_rose_1(data=None, date=None):

    # 数据计算
    # radius为要绘制的扇形半径，即plt.bar()的参数height
    # 64为中心空心圆环的半径，需要减去
    plot_data = data.iloc[0: 11]
    radius = np.array(plot_data['Confirmed'].tolist())
    countries = plot_data['Country_Region'].tolist()
    radius_normalized = 1000 * (radius - radius.min()) / (radius.max() - 0)  # x-min/max-min   归一化
    # radius_normalized -= 20
    # n为扇形个数，即国家数，本例中为33，在分别求左右半圆的个数时会用到
    n = len(radius_normalized)

    # 判断n的奇偶性
    # 本例中n为奇数，为使此绘图脚本更具通用性，应针对n的奇偶性分别判断，此处略
    # 本例中含有33个国家，33为奇数，为了制图美观，使得左半圆和右半圆之间刚好被一条垂直直线平分，
    # 将左半圆放置前16个国家，右半圆放置后17个国家，即int(n/2)和int(n/2)+1。
    # 如果n为偶数，则左半圆和右半圆扇形数量相同，直接n/2即可。

    # 取radius前一半的数据，即前16个国家的扇形半径
    radius1 = radius_normalized[:int(n / 2)]
    # 取radius后一半的数据，即后17个国家的扇形半径
    radius2 = radius_normalized[int(n / 2):]

    # theta为每个扇形的起始角度，即plt.bar()的参数x，x坐标(极坐标下即为扇形的起始角度)
    # 左半圆每个扇形的起始角度，即把左半圆的pi分成16份，从0到pi，间隔pi/16
    theta1 = np.arange(0, np.pi, np.pi / int(n / 2))
    # 右半圆每个扇形的起始角度，先把右半圆的pi分成17份，位置从0到pi，间隔pi/17，再加上左半圆的角度偏移pi，即从pi到2pi，间隔pi/17
    theta2 = np.arange(0, np.pi, np.pi / (int(n / 2) + 1)) + np.pi

    # width为每个扇形的宽度，即plt.bar()的参数width(极坐标下即为扇形的角度)
    # 左半圆每个扇形的角度，即把pi分成16份
    width1 = np.pi / int(n / 2)
    # 右半圆每个扇形的角度，即把pi分成17份
    width2 = np.pi / (int(n / 2) + 1)

    # color 为每个扇形的填充颜色，从人民日报原图中取色得到
    color = colors
    # 左半圆每个扇形的颜色值，即color中第1个到第16个值
    color1 = color[:int(n / 2)]
    # 右半圆每个扇形的颜色值，即color中第17个到第33个值
    color2 = color[int(n / 2):]

    # 绘制扇形
    # 设置画布大小和分辨率
    # 画布大小单位为英寸，1英寸=2.54厘米；分辨率若用于打印则为300，屏幕显示则为72
    fig = plt.figure(figsize=(30, 30), dpi=300)

    # 启用极坐标
    ax = fig.add_subplot(111, projection='polar')
    ax.set_title('COVID-19 ' + date.strftime('%Y-%m-%d') + '南丁格尔玫瑰图', fontdict={'weight': 'bold', 'size': 20})

    # 设置极坐标0°位置为'N'
    ax.set_theta_zero_location('N')

    # 绘制左半圆
    ax.bar(x=theta1, height=radius1, width=width1,
           color=color1, edgecolor=color1, linewidth=0.15,
           align='edge', bottom=20)

    # 绘制右半圆
    ax.bar(x=theta2, height=radius2, width=width2,
           color=color2, edgecolor=color2, linewidth=0.15,
           align='edge', bottom=20)
    # 参数解释：
    # edgecolor: 用填充形状的颜色作为边框颜色
    # linewidth: 设置边框宽度。如果不画边框，扇形会出现白边
    # align: 从指定角度开始绘图。设置为'edge'可从0度开始(默认值'center’会居中)
    # bottom: 条形的起始位置，也是y轴的起始坐标，即中心空心圆环的半径

    # 绘制中心的两个半透明圆
    # 内圆起始角度为0，角度2pi，半径122，白色，透明度0.15(内圆的透明度会叠加外圆的透明度)
    ax.bar(x=0, height=50, width=2 * np.pi, color='white', alpha=0.15)
    # 外圆起始角度为0，角度2pi，半径162，白色，透明度0.1
    ax.bar(x=0, height=70, width=2 * np.pi, color='white', alpha=0.1)

    for i in range(len(theta1)):
        plt.text(theta1[i] + width1 * 2 / 3, radius1[i] * 8 / 9, countries[i],
                 rotation=np.rad2deg(theta1[i] + width1 / 2),
                 color='white', fontdict={'size': 30 * radius1[i] / radius1[0]})

    # 显示图形
    # 关闭边框显示
    plt.axis('off')
    # 当画布尺寸较大时，可关闭显示图形，直接输出png图片，否则无响应
    # plt.show()
    plt.savefig(date.strftime('%Y-%m-%d_') + 'COVID-19.png', transparent=True)


def plot_climb_rate(data0, data1=None, data2=None):
    plot_marker = ['v', 'o', '3', '+', 'D',
                   'p', 'x', '|', ',', '.']
    plot_color = colors[0: 30: 3]

    fig = plt.figure(figsize=(9, 8))
    fig.subplots_adjust(hspace=0.35)

    fig.add_subplot(311)
    plt.title('确诊人数周环比增幅')
    plot_datas = data0.head(10).values.tolist()
    plt.xticks(range(len(plot_datas[0]) - 1), data0.columns.values.tolist()[1::])
    for i in range(5):
        current_data = plot_datas[i]
        country_name = current_data[0]
        climb_rates = np.array(current_data[1::]) - 1.
        plt.plot(climb_rates, marker=plot_marker[i], color=plot_color[i], label=country_name, linewidth=1)
    plt.grid(axis='y', ls='--')
    plt.legend()

    fig.add_subplot(312)
    plt.title('死亡人数周环比增幅')
    plot_datas = data1.head(10).values.tolist()
    plt.xticks(range(len(plot_datas[0]) - 1), data1.columns.values.tolist()[1::])
    for i in range(5):
        current_data = plot_datas[i]
        country_name = current_data[0]
        climb_rates = np.array(current_data[1::]) - 1.
        plt.plot(climb_rates, marker=plot_marker[i], color=plot_color[i], label=country_name, linewidth=1)
    plt.grid(axis='y', ls='--')
    plt.legend()

    fig.add_subplot(313)
    plt.title('治愈人数周环比增幅')
    plot_datas = data2.head(10).values.tolist()
    plt.xticks(range(len(plot_datas[0]) - 1), data2.columns.values.tolist()[1::])
    for i in range(5):
        current_data = plot_datas[i]
        country_name = current_data[0]
        climb_rates = np.array(current_data[1::]) - 1.
        plt.plot(climb_rates, marker=plot_marker[i], color=plot_color[i], label=country_name, linewidth=1)
    plt.grid(axis='y', ls='--')
    plt.legend()


def plot_country_data(confirmed_data, deaths_data, recovered_data, country='US'):
    data0 = confirmed_data[(confirmed_data['Country/Region'] == country)].values.tolist()[0]
    data1 = deaths_data[(deaths_data['Country/Region'] == country)].values.tolist()[0]
    data2 = recovered_data[(recovered_data['Country/Region'] == country)].values.tolist()[0]

    plt.figure(figsize=(9, 8))
    plt.title('某国疫情发展折线图')
    plt.plot(data0[1::7], marker='x', color='red', label=country + ' confirmed', linewidth=1)
    plt.plot(data1[1::7], marker='o', color='blue', label=country + ' death', linewidth=1)
    plt.plot(data2[1::7], marker='+', color='green', label=country + ' recovered', linewidth=1)
    plt.xticks(range(len(data0[1::7])), confirmed_data.columns.values.tolist()[1::7])

    plt.grid(axis='y', ls='--')
    plt.legend()


def plot_country_data_candlestick(confirmed_data, deaths_data, recovered_data, country='US'):
    data0 = confirmed_data[(confirmed_data['Country/Region'] == country)].values.tolist()[0]
    data1 = deaths_data[(deaths_data['Country/Region'] == country)].values.tolist()[0]
    data2 = recovered_data[(recovered_data['Country/Region'] == country)].values.tolist()[0]

    tmp_last_confirmed_data = np.array([0] + data0[1::])
    tmp_today_confirmed_data = np.array(data0[1::] + [0])
    tmp_delta_confirmed_data = tmp_today_confirmed_data - tmp_last_confirmed_data
    # tmp_confirmed_data = np.array(data0[1::])

    tmp_last_death_data = np.array([0] + data1[1::])
    tmp_today_death_data = np.array(data1[1::] + [0])
    tmp_delta_death_data = tmp_today_death_data - tmp_last_death_data

    tmp_last_recovered_data = np.array([0] + data2[1::])
    tmp_today_recovered_data = np.array(data2[1::] + [0])
    tmp_delta_recovered_data = tmp_today_recovered_data - tmp_last_recovered_data

    x = range(len(data0[0::7]))

    plt.figure(figsize=(9, 8))
    plt.title('某国疫情发展烛形图')
    plt.xticks(x, confirmed_data.columns.values.tolist()[1::7])
    plt.plot(tmp_delta_confirmed_data[0::7], marker='*', color='red', label=country + ' new confirmed', linewidth=1)
    plt.bar(x=x, height=tmp_delta_death_data[0::7],
            label=country + ' new death', color='red', width=0.5,
            bottom=tmp_delta_confirmed_data[0::7], alpha=0.5)
    plt.bar(x=x, height=tmp_delta_recovered_data[0::7],
            label=country + ' new recovered', color='blue', width=0.5,
            bottom=tmp_delta_confirmed_data[0::7] - tmp_delta_recovered_data[0::7], alpha=0.5)

    plt.grid(axis='y', ls='--')
    plt.legend()


if __name__ == '__main__':
    # for i in range(4):
    #     data_date = datetime.date(2020, i + 1, 25)
    #     world_data_pd = read_data(date=data_date, use_daily=True)
    #     sorted_world_data_pd = world_data_pd.sort_values(by='Confirmed', ascending=False)
    #     plot_rose_1(sorted_world_data_pd, date=data_date)

    world_ts_confirmed_data_pd, world_ts_deaths_data_pd, world_ts_recovered_data_pd = read_data(use_daily=False)
    world_sorted_ts_confirmed_data_pd = \
        world_ts_confirmed_data_pd.sort_values(by=world_ts_confirmed_data_pd.columns[-1], ascending=False)
    world_sorted_ts_deaths_data_pd = \
        world_ts_deaths_data_pd.sort_values(by=world_ts_deaths_data_pd.columns[-1], ascending=False)
    world_sorted_ts_recovered_data_pd = \
        world_ts_recovered_data_pd.sort_values(by=world_ts_recovered_data_pd.columns[-1], ascending=False)

    world_sorted_week_confirmed_climb_rate_pd = calc_climb_rate(world_sorted_ts_confirmed_data_pd)
    world_sorted_week_deaths_climb_rate_pd = calc_climb_rate(world_sorted_ts_deaths_data_pd)
    world_sorted_week_recovered_climb_rate_pd = calc_climb_rate(world_sorted_ts_recovered_data_pd)

    plot_climb_rate(
        world_sorted_week_confirmed_climb_rate_pd,
        world_sorted_week_deaths_climb_rate_pd,
        world_sorted_week_recovered_climb_rate_pd
    )
    plot_country_data(
        world_sorted_ts_confirmed_data_pd,
        world_sorted_ts_deaths_data_pd,
        world_sorted_ts_recovered_data_pd
    )
    plot_country_data_candlestick(
        world_sorted_ts_confirmed_data_pd,
        world_sorted_ts_deaths_data_pd,
        world_sorted_ts_recovered_data_pd
    )

    plt.show()

