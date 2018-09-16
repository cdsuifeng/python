'''
Created on 2018年9月14日

@author: suifeng
@job: 分析七种语言的平均最低薪资、平均最高薪资,生成柱状图；分析Python语言的招聘要求待遇，生成词云图
@tips: 
'''

import requests
import random
import json
import jieba
import time
from pyecharts import Bar
from wordcloud import WordCloud as WC
from kuaidaili_spider import format_ip
from matplotlib import pyplot as plt # 绘图模块

# 爬虫类
class Spider(object):
    def __init__(self,list_lang):
        self.headers={
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '25',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'www.lagou.com',
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/jobs/list_Python?px=default&city=%E5%85%A8%E5%9B%BD',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
            'X-Anit-Forge-Code': '0',
            'X-Anit-Forge-Token': 'None',
            'X-Requested-With': 'XMLHttpRequest'
            }
        self.ip=random.choice(format_ip())
        self.proxies={
            'http' : 'http://'+self.ip,
#             'https' : 'https://'+self.ip
            }
        self.params={
            'px' : "default",
            'needAddtionalResult' : 'false'
            }
        self.session=requests.session()
        self.url='https://www.lagou.com/jobs/positionAjax.json'
        self.data={}
        self.low_average_salary=[] 
        self.high_average_salary=[]
        self.list_lang=list_lang
        self.text=''
        
    def analyses_salary(self):
        for language in self.list_lang :
            print(language,'--------------start')
            flag='false'
            low_salary_list=[]
            high_salary_list=[]
            for p in range(1,31) :
                if p == 1 :
                    flag='true'
                print(p,'页--------------')
                self.data.update({
                    'first' : flag,
                    'pn' : p ,
                    'kd' : language
                    })
                print('-----休眠5秒--start---')
                time.sleep(5)
                print('-----休眠5秒--end---')
                # 每3页更换一次session和代理ip
                if p%3==0:
                    self.session=requests.session()
                    self.proxies={'http' : 'http://'+random.choice(format_ip()) }#,'https':'https://'+self.ip
                print(self.proxies)
                resp=self.session.post(self.url,headers=self.headers,params=self.params,\
                                       data=self.data,proxies=self.proxies,cookies=self.session.cookies)
                all_data=json.loads(resp.text)
                result=all_data['content']['positionResult']['result']
                for item in range(15) :
                    salary=result[item]['salary'].split('-')
                    if len(salary)>1 :
                        low_salary=salary[0][:-1]
                        high_salary=salary[1][:-1]
                        low_salary_list.append(int(low_salary))
                        high_salary_list.append(int(high_salary))
                    else :
                        low_salary=salary[0].split('k')[0]
                        high_salary=0
                        low_salary_list.append(int(low_salary))
                        high_salary_list.append(0)
                        # 获取完Python的文本注释掉下面
#                     if language=='python' :
#                         company_lable_list=result[item]['companyLabelList']
#                         position_Advantage_list=result[item]['positionAdvantage']
#                         company_lable_list.extend(position_Advantage_list)
#                         for t in company_lable_list :
#                             self.text+=t
#                 self.save_text(self.text)        
            self.low_average_salary.append(self.average(low_salary_list))
            print('low:',self.low_average_salary)
            self.high_average_salary.append(self.average(high_salary_list))
            print('high:',self.high_average_salary)
            print('---------one language--end-----')
        print('-----------开始生成图表--------------')
        self.make_chart(self.low_average_salary, self.high_average_salary)
        
#     求平均数   
    def average(self,lis):
        aver=0
        for i in range(len(lis)) :
            aver+=lis[i]
        return aver//len(lis)
    
#     生成图表
    def make_chart(self,low,high):
        bar = Bar("拉钩七门编程语言的薪资排行")
        bar.add("最低平均工资", 
                self.list_lang, low,
                is_more_utils=True)
        bar.add("最高平均工资", 
                self.list_lang, high,
                is_more_utils=True)
        bar.render('/home/suifeng/文档/chart.html')
        print('-------------图表保存成功---------------')
        
#     保存文本
    def save_text(self,text):
        with open('/home/suifeng/文档/text.txt' , 'w') as f:
            f.write(text)
    
#     生成词云图
    def make_wc(self):
        with open('/home/suifeng/文档/text.txt','r') as f :
            text=f.read()
        text_spilt=''.join(jieba.cut(text))
        wc=WC(
            background_color='black', #背景色
            max_words=100, #最大词数
            max_font_size=80, #最大字体大小
            random_state=35, # 最多的字样随机形态
            font_path='MSYH.TTC' #字体路径，必须有字体，字体文件可以从Windows系统下复制过来
            ).generate(text_spilt)
        plt.imshow(wc)
        plt.axis('off')
        plt.show()
        wc.to_file('/home/suifeng/图片/python词云图.png')
    
if __name__=='__main__' :
    list_lang=['Go','PHP','.NET','区块链','python','Java','C++']
#     ['Go','PHP','.NET','区块链','python','Java','C++']
#     low=[17,13,8,17,15,13,13]
#     high=[31,23,13,31,26,24,24]
    spider=Spider(list_lang)
    spider.analyses_salary()
#     spider.make_chart(low, high)
#     spider.make_wc()