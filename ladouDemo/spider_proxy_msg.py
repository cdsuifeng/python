'''
Created on 2018年9月10日

@author: suifeng
'''

import requests
from lxml import etree 
import xlrd # 读取表格信息
import xlwt # 信息写入表格
import time


def spider(url):
    headers={
        'Host': 'www.kuaidaili.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.kuaidaili.com/free/inha/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
        }
    session=requests.session()
    p=1
    proxies_msg={}
    while True :
        url2=url +'/'+str(p)+'/'
        p+=1
        time.sleep(5) # 这是必须要有的，否则会返回-10，获取不到数据
        resp=session.get(url2,headers=headers,timeout=5)
        selector=etree.HTML(resp.text)
        ip=selector.xpath('//*[@id="list"]/table/tbody//tr/td[1]/text()') #['+str((i+1))+']
        port=selector.xpath('//*[@id="list"]/table/tbody//tr/td[2]/text()') #['+str((i+1))+']
        for i in range(15) :
            proxies_msg[ip[i]]=port[i]
        print(p-1,'页')
        if p==6:
            break
    print('------------开始保存------------')
    save_table(proxies_msg)
    
    
def save_table(dic):
    workbook=xlwt.Workbook(encoding='utf-8')
    booksheet=workbook.add_sheet('sheet 1', cell_overwrite_ok=True)
    row,col=0,0
    for i in dic.items():
        for j in i :
            booksheet.write(row,col,j)
            col+=1
        row+=1
        col=0
    workbook.save('/home/suifeng/文档/proxies.xls')
    print('----------------保存成功---------------')
    
def read_table():
    wk=xlrd.open_workbook('/home/suifeng/文档/proxies.xls')
    sheet=wk.sheet_by_index(0)
    rows=sheet.nrows
    cols=sheet.ncols
    dic={}
    for row in range(rows) :
        value=sheet.row_values(row)
        dic[value[0]]=value[1]
    return dic

def iter_dic():
    dic=read_table()
    for ip , port in dic.items() :
        test_download(ip, port)
    
    
# 测试代理是否可用，然后进行相应的操作，这里我设置延迟为5秒。
def test_download(ip,port):
    proxies={
        'http' :  '%s:%d' % (ip,port)                      #'http://219.234.181.194:33695'
        }
    headers={
        'user-agent' :'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36\
         (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
    #     'referer' : ''
        }
    url='http://www.baidu.com'
    resp=requests.get(url,headers=headers,proxies=proxies,timeout=5)
    
    if resp.status_code== 200:
        print('succeeded')
    else :
        print(ip,':',port)
        print('failed')
        
if __name__=='__main__' :
    url='https://www.kuaidaili.com/free/inha'
    spider(url)
