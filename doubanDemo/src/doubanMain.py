# -*- coding=utf-8 -*-
'''
Created on 2018年8月20日

@author: suifeng
'''

import requests # 有关url的库
from bs4 import BeautifulSoup as bs # 解析网页的库
import jieba # 生成分词的库
from wordcloud import WordCloud # 绘制词云的库
from matplotlib import pyplot as plt # 可视化第三方库
# 目标地址
url='https://movie.douban.com/subject/24852545/comments?limit=20&sort=new_score&status=P'
# 获取所有短片的文本内容
def get_html():
    p=0
    str1='' 
    while(True):
        params={'start': p}
        p+=20
#         封装请求头
        headers={'Connection':'keep-alive', 'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'}
        resp = requests.get(url, params=params, headers=headers)
        soup=bs(resp.text,'html.parser')
#         拼接所有短片字符串
        for ps in soup.findAll('span',class_='short'):
            str1=str1+ps.text
        if p==220:
            break
    make_cword(str1)
    
# 生成词云图
def make_cword(string):
#     用jieba进行文本切割
    text_spilt=' '.join(jieba.cut(string))
    pic=plt.imread('../images/love.jpg')
    wcd=WordCloud(
        background_color='white', # 背景色
        mask=pic, # 模板图片
        max_words=500, # 最大词数
        max_font_size=80, # 最大字体大小
        random_state=30, # 随机形态
        font_path='../fonts/MSYH.TTC', #字体路径
        ).generate(text_spilt)
    plt.imshow(wcd)
    plt.axis('off')
#     展示
    plt.show()
#     保存图片
    wcd.to_file('/home/suifeng/图片/爱情公寓.png')
if __name__ == '__main__' :
    get_html()
    
    
