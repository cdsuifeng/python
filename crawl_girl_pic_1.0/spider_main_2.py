'''
Created on 2018年9月11日

@author: suifeng
@vesion : 1.1
@tips：
    1.经过改善，程序实现了面向对象，并利用xpth来获取信息
    2.使用伪多线程，并没有实现真的多线程下载，只是用来迭代生成器，一个线程的简单应用，并且判退出没有实现
    3.没有多线程和面向对象的话，程序还是比较简洁的，只有50行代码左右
    4.如果有更好的方法实现真多线程下载，请大佬与我联系，还请不吝赐教。关注公众号--o2o2
    5.本人Python小白，如果您有更好的建议和意见改进程序，可关注公众号与我讨论。关注公众号--o2o2
'''
import requests #网络库
from lxml import etree # 解析利器 在查找元素信息的时候比bs4好用的多 简洁，方便
import re 
import os 
import threading # 线程模块 ，thread已弃用
import time 

# 爬虫类
class Spider(object):
#     初始化
    def __init__(self,url,page_start=1,page_end=10):
        self._url=url # 主页
        self._page_start=page_start # 开始爬取的页
        self._page_end=page_end # 结束爬取的页
        self._path='/home/suifeng/图片/mm/' # 保存的根路径
        self._headers={
            'Referer': 'http://www.mmjpg.com/',
            'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10'
            }
        self._session=requests.session() 
        self._girl_msg={} # 每个picture的url和alt
#         self._girl_pro={} # 
        self._lock=threading.Lock() # 线程锁
        self._gen=self.generator_util() # 生成器
        
#     检查并设置开始页
    def set_page_start(self,start,m):
        start=int(start)
        m=int(m)
        if start>0 and start<=m:
            self._page_start=start
        else :
            print('start error')
            print('please again')
            exit()
            
#     get开始页
    def get_page_start(self):
        return self._page_start
    
#     检查并设置结束页
    def set_page_end(self,end,m):
        end=int(end)
        m=int(m)
        start=self.get_page_start()
        if end>=start and end <=m:
            self._page_end=end
        else :
            print('end error')
            print('please again')
            exit()
    
#     get结束页
    def get_page_end(self):
        return self._page_end
        
#     检查网站当前最大的页    
    def check_max_page(self):
        resp=self._session.get(self._url,headers=self._headers)
        resp.encoding='utf-8'
        select=etree.HTML(resp.text)
        max_url=select.xpath('/html/body/div[2]/div[1]/ul/li[1]/a/@href')
        max_page=re.search(r'\d.+',max_url[0])
        if max_page :
            return max_page.group(0)
        else :
            print('error!')
        
#     生成器
    def generator_util(self):
        for i in range(self._page_start,self._page_end+1) :
            url2=self._url+'mm/'+str(i)+'/%d'
            p=1
            self._girl_msg.clear()
            while True:
                url3=url2 % p
                p+=1
                resp=self._session.get(url3,headers=self._headers)
                resp.encoding='urf-8'
                selector=etree.HTML(resp.text) # lxml选择器
                img=selector.xpath('//*[@id="content"]/a/img/@src') # 提取url路径
                alt=selector.xpath('//*[@id="content"]/a/img/@alt') # 提取alt路径
                if img== [] and alt==[] : #判断是否到尾，img和alt是一个list
                    break
                else :
                    self._girl_msg[img[0]]=alt[0] # 暂存dict
                    print('one record',p-1)
            print('one page')
            yield self._girl_msg # 构建生成器函数，yield相当于暂停，开始
        
#     下载器
    def downloader_util(self,dic):
        file_name=''
        file_path=''
#         判断路径是否存在
        if not os.path.exists(self._path) :
            os.mkdir(self._path)
        for value in dic.values() :
            file_name=value
            break
        file_name=file_name.split(' ')[0]
        file_path=self._path+file_name
        if not os.path.exists(file_path):
            os.mkdir(file_path)
#         迭代dic，保存到本地
        for url,title in dic.items():
            with open(file_path+'/'+title,'wb') as f :
                f.write(self._session.get(url,headers=self._headers).content)
            print('Successfully Saved!',threading.current_thread())
            
#     工作流
    def job_stream(self): 
#         获得锁
        self._lock.acquire() 
#         获取生成器的结果 ， 使用线程迭代
        dic = next(self._gen)
        self.downloader_util(dic)
#         释放锁
        self._lock.release()
        
#     线程调度器
    def thread_control_util(self,num_thread=2):
        num_thread=int(num_thread)
#         线程池
        thread_list=[]
#         初始化线程
        for th in range(num_thread):
            var='thread_down'+str(th)
            thread_list.append(var)
            thread_list[th]=threading.Thread(target=self.job_stream,\
                                                         name='job-'+str(th))
            thread_list[th].start()
#         循环判断线程是否一直是指定值
        while True :
            if threading.active_count()<num_thread+1:
                for th in range(num_thread):
                    if not thread_list[th].isAlive():
                        thread_list[th]=threading.Thread(target=self.job_stream,\
                                                         name='job-'+str(th))
                        print(thread_list[th],'创建线程成功')
                        thread_list[th].start()
# 调试入口
if __name__ == '__main__' :
    url='http://www.mmjpg.com/'
    spider=Spider(url) 
    max_page=spider.check_max_page()
    print('当前网站最大的页数：',max_page)
    page_s=input('start_page:')
    spider.set_page_start(page_s,max_page)
    page_e=input('end_page:')
    spider.set_page_end(page_e,max_page)
    num=input('最大下载线程(默认为2):')
    spider.thread_control_util(num)
    