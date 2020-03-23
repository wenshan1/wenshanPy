# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 15:31:16 2018

@author: Bin Lan
@email: jetlan@live.cn

爬取妹子图
"""

import requests
import os
import time
#import threading
from bs4 import BeautifulSoup


def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)
        
def download_page(url):
    '''
    用于下载页面
    '''
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    r = requests.get(url, headers=headers)
    r.encoding = 'gb2312'
    return r.text

def get_pic(link, text):
    '''
    获取当前页面的图片,并保存
    '''
    html = download_page(link)  # 下载界面
    soup = BeautifulSoup(html, 'html.parser')
    pic_list = soup.find('div', id="picture").find_all('img')  # 找到界面所有图片
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    create_dir('pic/{}'.format(text))
    for i in pic_list:
        pic_link = i.get('src')  # 拿到图片的具体 url
        r = requests.get(pic_link, headers=headers)  # 下载图片，之后保存到文件
        with open('pic/{}/{}'.format(text, pic_link.split('/')[-1]), 'wb') as f:
            f.write(r.content)
            time.sleep(1)   # 休息一下，不要给网站太大压力，避免被封
            
def get_pic_list(html):
    '''
    获取每个页面的套图列表,之后循环调用get_pic函数获取图片
    '''
    soup = BeautifulSoup(html, 'html.parser')
    pic_list = soup.find_all('li', class_='wp-item')
    for i in pic_list:
        a_tag = i.find('h3', class_='tit').find('a')
        link = a_tag.get('href')
        text = a_tag.get_text()
        get_pic(link, text)
        
def main():
    create_dir ('pic')
    queue = [i for i in range (1, 70)] #构造url
 
    while len (queue) > 0:
        cur_page = queue.pop(0)
        url = 'http://meizitu.com/a/more_{}.html'.format(cur_page)
        page_html = download_page(url)
        get_pic_list(page_html)
        
        
if __name__ == '__main__':
    main()    
    

