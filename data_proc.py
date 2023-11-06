import matplotlib.pyplot as plt
import pandas as pd
from snownlp import SnowNLP
from wordcloud import WordCloud
import numpy as np
from PIL import Image
import jieba.analyse
import matplotlib.dates as mdates
from datetime import datetime

from Scraper import folder_name


#去重和去空值
def data_cleaning(df):
    df = df.drop_duplicates(subset=['评论内容'])

    print('IP属地： ',df['IP属地'].isnull().value_counts())
    print('检查重复： ', df['评论时间'].duplicated().value_counts())
    df.to_csv('{}/{}.csv'.format(folder_name,folder_name), mode = 'w', encoding = 'utf_8_sig', index = False, header = True)
    return df


def get_top_IP(outfile, df):

    plt.style.use('seaborn')

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    print(df['IP属地'].value_counts().nlargest(15))
    df['IP属地'].value_counts().nlargest(15).plot.bar(figsize=(12,6))

    plt.title('评论者IP来源')
    plt.xlabel('省')
    plt.ylabel('人数')
    plt.legend()
    plt.savefig('{}_IP.png'.format(outfile.replace('.csv', '')))
    plt.close()




def get_sex_stats(outfile, df):

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签  # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

    labels = ['男', '女']
    
    sizes = df['性别'].value_counts().nlargest(2)

    print(sizes)


    plt.figure(figsize=(6,6))

    plt.pie(sizes, labels=labels, autopct = '%1.1f%%' )

    plt.title('男女分布')
    plt.axis('equal')
    plt.legend()
    plt.annotate(f'Total: {sizes}', xy=(-0.9, 1), fontsize=12, ha='center', va='center')
    plt.savefig('{}_性别'.format(outfile.replace('.csv','')))

def get_popular_comments(outfile, df):

    print('数据形状: ', df.shape)
    df['点赞数'] = pd.to_numeric(df['点赞数'], errors='coerce', downcast='integer')
    most_like = df.nlargest(10, '点赞数')
    most_like.to_csv('{}_like.csv'.format(outfile.replace('.csv','')), encoding = 'utf_8_sig')
    print(most_like)


def time_line_graph(outfile, df):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签  # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    try:
        df['评论时间2'] = pd.to_datetime(df['评论时间'], errors='coerce')
    except ValueError as e:
        print(e)
    df['评论日期'] = df['评论时间2'].dt.date # extract date
    df_cmt_date = df['评论日期'].value_counts()
    df_cmt_date = df_cmt_date.reset_index()
    df_cmt_date.columns = ['评论日期','评论数量']

    print(df_cmt_date)

    df_cmt_date.plot(x='评论日期',y='评论数量', figsize=(50,6))
    plt.title('评论时间线')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.savefig('{}_评论时间线.png'.format(outfile.replace('.csv','')))
    plt.close()
    print('已生成评论时间线')



if __name__ =='__main__':
    start_time = datetime.now()

    outfile = '{}/{}.csv'.format(folder_name,folder_name)
    df = pd.read_csv(outfile)

    df = data_cleaning(df)
    get_top_IP(outfile, df)
    get_sex_stats(outfile, df)
    time_line_graph(outfile, df)
    get_popular_comments(outfile, df)
    

    #统计总行数

    end_time = datetime.now()

    print(end_time - start_time)