# -*- coding: utf-8 -*- 
# @Time : 2018/11/28 9:39 
# @Author : Allen 
# @Site :  爬取省政府网站
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from model.models_service import ModelService
import re


class CrawlProcessor(object):
    @classmethod
    def crawl_url(clf, url):
        '''
        requests请求url
        :param url:url
        :return:html
        '''
        headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                   'Accept - Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
                   'Connection': 'Keep-Alive',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
                   }
        return requests.get(url, params=headers, timeout=30).content.decode('utf-8')

    @classmethod
    def get_url_beautiful_object(clf, url):
        '''
        html转为BeautifulSoup对象
        :param url:url
        :return:beautifulSoup对象
        '''
        return BeautifulSoup(clf.crawl_url(url), 'html.parser')

    @classmethod
    def get_db_session(clf):
        '''得到 数据库 session'''
        return ModelService()

    @classmethod
    def str_to_datetime(clf, str, time_type='%Y-%m-%d %H:%M:%S'):
        '''
        字符串转为datetime类型
        :param str:
        :return:
        '''
        str = str.strip()
        return datetime.strptime(str, time_type)

    @classmethod
    def get_num_of_page(clf, url):
        def regex_num(x):
            return re.findall(r'[\d]+', x)[0]

        bs = clf.get_url_beautiful_object(url)
        return regex_num(str(bs.find('div', 'page').find('script')))

    @classmethod
    def parser_web_detail(cls, url):
        def regex_resource(x):
            '''正则匹配第一个中文'''
            return re.findall(r'[\u4e00-\u9fa5]+', str(x))[0]

        '''解析网页详细页面'''
        bs = cls.get_url_beautiful_object(url)
        title = bs.find('div', 'Article_bt').h1.text
        _tag = bs.find('div', 'Article_ly').find_all('span')
        resource = regex_resource(_tag[0].find('script'))
        publish_time = cls.str_to_datetime(_tag[1].text[5:])
        content = ''.join(list(map(lambda x: x.text, bs.find('div', 'zw-con').find_all('p')))).strip()
        return (title, resource, publish_time, content)

    def parser_web(self, bs):
        '''
        解析网页
        :param html:网页代码
        :return:
        '''
        raise NotImplementedError()

    def get_data_examples(self):
        '''
        获取爬虫数据
        :return:
        '''
        raise NotImplementedError()

    def insert_data(self, ExampleData):
        '''
        数据插入数据库
        :param ExampleData:数据对象
        :return:
        '''
        raise NotImplementedError()
