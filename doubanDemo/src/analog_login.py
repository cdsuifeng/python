# -*- coding=utf-8 -*-
'''
Created on 2018年8月21日

@author: suifeng
'''

import requests
import random
import re
from bs4 import BeautifulSoup as bs # 解析网页的库
import jieba # 生成分词的库
from wordcloud import WordCloud # 绘制词云的库
from matplotlib import pyplot as plt # 可视化第三方库
from PIL import Image

User_Agent=[
    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36',
    ]

headers={
    'Host' : 'accounts.douban.com',
    'Referer' : 'https://accounts.douban.com/login',
    'User-Agent':random.choice(User_Agent)}
session=requests.session() # session() 和 Session()有同样的效果
 
#模拟登录
def login(username,password):
    login_url='https://accounts.douban.com/login'
    #表单内容
    form_data={
        'form_email':username,
        'form_password': password,
        'login': '登录' ,
        'redir': 'https://movie.douban.com/',
        'source' : 'movie'
        }
    #先get下一网址，为了获得验证码，若有
    captcha=session.get(url=login_url,headers=headers,timeout=30)
    soup=bs(captcha.content,'html.parser')
    #查看发现验证码保存在标签为img，id为captcha_image
    img=soup.find('img',id='captcha_image')
    if img:
        captcha_url=img['src']
        a=captcha_url.split('&')[0]
        capid=a.split('=')[1]
        #获得二进制文件
        cap=session.get(captcha_url,headers=headers).content
        with open('captcha.jpg','wb') as f:
            f.write(cap)
            f.close()
            im = Image.open('captcha.jpg')
            im.show()
        check = input("请输入验证码：")
        new_form_data={
            'captcha-id' :capid,
            'captcha-solution' : check
            }   
        form_data.update(new_form_data)
    else:
        print('没有验证码！')
    req=session.post(login_url,data=form_data,headers=headers)
    
#请求网页
def get_html(url):
    p=0
    str1='' 
    while(True):
        params={'start': p}
        p+=20
#         封装请求头
        #headers={'Connection':'keep-alive', 'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'}
        resp = session.get(url, params=params)
        soup=bs(resp.text,'html.parser')
#         拼接所有短片字符串
        for ps in soup.findAll('span',class_='short'):
            str1=str1+ps.text
        if p==480:
            break
    return str1

#保存短评   
def save_short(stri):
    f=open('short.txt','w+')
    f.write(stri)
    
#生成词云图
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
 
if  __name__=='__main__':
    login_url='https://accounts.douban.com/login'
    object_url='https://movie.douban.com/subject/24852545/comments?limit=20&sort=new_score&status=P'
    login('YourEmail' ,'YourPassWord')
    short_str=get_html(object_url)
    save_short(short_str)
    make_cword(short_str)
    
    
