# -*- coding: utf-8 -*- 
# @Time : 2018/11/30 9:34 
# @Author : Allen 
# @Site :  crawl 新闻动态

from crawl_processor import CrawlProcessor
from data_example import XWDTData


class XWDTProcessor(CrawlProcessor):
    def __init__(self, url):
        self.url = url

    def parser_web(self, url):
        '''
        解析网页
        :param html:网页代码
        :return:
        '''
        print(url)
        list(map(self.get_web_detail, self.get_url_beautiful_object(url).find('div', 'right-list-box').find_all('li')))

    def get_web_detail(self, li):
        url = li.a['href']
        if not self.get_db_session().query_gzszf_data_xwdt_id_by_url(url):
            title = li.a['title']
            publish_time = self.str_to_datetime(li.span.text, '%Y-%m-%d %H:%M')
            self.insert_data(XWDTData(title, url, publish_time))

    def get_data_examples(self):
        '''
        获取爬虫数据
        :return:
        '''
        num = int(self.get_num_of_page(self.url))
        self.parser_web(self.url)
        if num > 1:
            ([self.parser_web(self.url + 'index_' + str(i) + '.html') for i in range(994, 1366)])

    def insert_data(self, ExampleData):
        '''
        数据插入数据库
        :param ExampleData:数据对象
        :return:
        '''
        self.get_db_session().insert_gzszf_data_xwdt(ExampleData)


def main():
    url = 'http://www.guizhou.gov.cn/xwdt/gzyw/'
    processor = XWDTProcessor(url)
    processor.get_data_examples()


if __name__ == '__main__':
    main()
