'''
Created on 2018年9月10日

@author: suifeng
@version: 1.0
@tips：
    1.尽量夜间或清晨爬取，不然运行一会就报连接超时的错误.修改代码第38行，看目录下有多少个子目录，然后range的开始值+1
    2.此网站虽然没有爬虫协议，但还是要适可而止
    3.cookies的参数不能加，否则会报错，目前不知为什么
    4.此脚本采用单线程，无模块化，非面向对象
    5.count.py脚本是计数已下载的子文件
    5.如果有问题，请联系我
'''

import requests #网络库，进行网络请求，资源的获取
from bs4 import BeautifulSoup as bs #网页解析库
import os #内置的库

#封装请求头，用于获取每个picture的url，其中user-agent和referer是必须有的
headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'www.mmjpg.com',
        'Referer': 'http://www.mmjpg.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10'
        }  
#用于下载的请求头      
headers2={
    'Referer': 'http://www.mmjpg.com/',
    'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10'
    }
#用session对象来进行资源的获取
session=requests.session()

#获取每一pic的url和名字，并临时保存至dict，然后调用save_pic函数来进行图片下载
def get_html(url):
#     这里我先get了一下主页，可有可无的
    session.get(url)
#     通过查看网页，可以发现暂时一共1468页，所以来个迭代
    for i in range(1,1469) :
#         拼接字符串封装url
        url2=url[:25]+str(i)+'/%d'
        p=1 # 循环变量
        url_src={} # 存储url ：alt的dict
#         循环每一页
        while True:
            url3=url2 % p # 封装url
            p+=1 
#             请求服务器，获得响应
            resp=session.get(url3,headers=headers) 
#             设置编码，不设置的话可能会乱码
            resp.encoding='utf-8'
            soup=bs(resp.text,'html.parser') # 解析
#             url ： alt信息都放在了这里 所以find
            n=soup.find('div', class_='content') 
#             用于判断内容是否存在
            if n==None:
                break
#             将获取到的信息临时保存到dict
            url_src[n.find('img')['src']]=n.find('img')['alt']
#             判跳出，是否是最后页面
            tag_a=soup.find('a', class_='ch next')
            if tag_a==None :
                break
        print('开始保存图片')
        save_pic(url_src)
    print('爬取完毕，尽情奔放吧！')

# 保存图片信息到本地
def save_pic(dic):
#     保存的绝对路径
    path='/home/suifeng/图片/mm/'
#     获得第一个value，并进行切割，获取标题，作为子文件夹
    first_value=''
    for va in dic.values() :
        first_value=va
        break
    title = first_value.split(' ')[0]
    ch_path=path+title
#     子文件夹不存在则创建
    if not os.path.exists(ch_path) :
        os.mkdir(ch_path)
#     迭代dict，保存到本地
    for url,title in dic.items():
#         注意，要以wb的方式打开文件，或者wb+也可以
        with open(ch_path+'/'+title,'wb') as f :
#             写入二进制文件
            f.write(session.get(url,headers=headers2).content)
        print('保存成功')
        
# 程序入口      
if __name__=='__main__':
    url='http://www.mmjpg.com/mm/'
    get_html(url)  
    