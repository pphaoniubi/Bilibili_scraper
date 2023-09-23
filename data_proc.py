import matplotlib.pyplot as plt
import pandas as pd
from snownlp import SnowNLP
from wordcloud import WordCloud
import numpy as np
from PIL import Image
import jieba.analyse
import matplotlib.dates as mdates


from Scraper import *

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
    plt.savefig('IP属地排名.png')
    plt.close()




def get_sex_stats():
    """"""



if __name__ =='__main__':
    get_top_IP(outfile)