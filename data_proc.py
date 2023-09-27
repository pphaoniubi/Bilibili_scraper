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
def data_cleaning():
    """"""



def get_top_IP(outfile):
    df = pd.read_csv(outfile)

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




def get_sex_stats(outfile):
    df = pd.read_csv(outfile)

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

def get_popular_comments(outfile):
    df = pd.read_csv(outfile)
    df['点赞数'] = pd.to_numeric(df['点赞数'], errors='coerce', downcast='integer')
    most_like = df.nlargest(10, '点赞数')
    most_like.to_csv('{}_like.csv'.format(outfile.replace('.csv','')), encoding = 'utf_8_sig')
    print(most_like)
    



if __name__ =='__main__':
    start_time = datetime.now()
    outfile = '{}/{}.csv'.format(folder_name,folder_name)
    get_top_IP(outfile)
    get_sex_stats(outfile)
    get_popular_comments(outfile)

    #数据清洗

    #统计总行数

    end_time = datetime.now()

    print(end_time - start_time)