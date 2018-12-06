# -*- coding: utf-8 -*- 
# @Time : 2018/11/29 9:26 
# @Author : Allen 
# @Site :  crawl 政策解读
from crawl_processor import CrawlProcessor
from data_example import JDHYData


class ZCJDProcessor(CrawlProcessor):
    def __init__(self, url):
        self.url = url

    def parser_web(self, url):
        '''
        解析网页
        :param html:网页代码
        :return:
        '''
        list(map(lambda x: self.get_web_detail(x.h2.a['href']),
                 self.get_url_beautiful_object(url).find('div', 'zcjd_list').ul.find_all('li')))

    def get_web_detail(self, url):
        if not self.get_db_session().query_gzszf_data_jdhy_by_url(url):
            try:
                title, resource, publish_time, content = self.parser_web_detail(url)
                self.insert_data(JDHYData(url, title, content, publish_time, resource))
            except Exception as e:
                print(e)
                print("Error url : {}".format(url))

    def insert_data(self, ExampleData):
        self.get_db_session().insert_gzszf_data_jdhy(ExampleData)

    def get_data_examples(self):
        '''
        获取爬虫数据
        :return:
        '''
        num = int(self.get_num_of_page(self.url))
        self.parser_web(self.url)
        if num > 1:
            ([self.parser_web(self.url + "index_" + str(i) + ".html") for i in
              range(1, num)])

    def display(self, href):
        print(href)


def main():
    url = 'http://www.guizhou.gov.cn/jdhy/zcjd_8115/'
    processor = ZCJDProcessor(url)
    processor.get_data_examples()


if __name__ == '__main__':
    main()
