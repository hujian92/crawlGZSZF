# -*- coding: utf-8 -*- 
# @Time : 2018/11/29 9:16 
# @Author : Allen 
# @Site :  crawl专题服务
from data_example import ZTFUData
from crawl_processor import CrawlProcessor
import re


class ZTFUProcessor(CrawlProcessor):
    '''
    继承CrawlProcessor，爬专题服务
    '''

    def __init__(self, url):
        self.url = url

    def parser_web_left(self, bs):
        '''解析网页左边部分'''

        def regex_url(x):
            '''正则匹配url中包含cjwt（常见问题）'''
            url = ''.join(re.findall(r'var str4 =.+cjwt+.*', str(x)))
            if 'cjwt' in url:
                return url.split('var str4 = ')[-1].strip()[1:-2]
            else:
                return None

        div = bs.find('div', 'Left_Nav_zs')
        li = div.find_all('li')
        dl = div.find_all('dl')
        assert len(li) == len(dl), print("主题:{};URL:{}".format(len(li), len(dl)))
        for i, d in enumerate(dl):
            url = regex_url(d.find_all('script'))
            if url:
                self.parser_web_next(meta={'url': url, 'theme': li[i].span.text})

    def parser_web_right(self, url, meta):
        '''解析网页右边部分'''

        def go_web_detail(url):
            self.get_web_detail(url, meta)

        bs = self.get_url_beautiful_object(url)
        list(map(lambda x: go_web_detail(x.a['href']), bs.find('div', 'NewsList').find_all('li')))

    def get_web_detail(self, url, meta):
        if not self.get_db_session().query_gzszf_data_ztfw_id_by_url(url):
            try:
                '''解析网页详细页面'''
                title, resource, publish_time, content = self.parser_web_detail(url)
                self.insert_data(
                    ZTFUData(theme=meta['theme'], theme_url=meta['url'], detail_url=url, title=title, content=content,
                             publish_time=publish_time, resource=resource))
            except Exception as e:
                print(e)
                print("Error url:{}".format(url))

    def insert_data(self, ExampleData):
        self.get_db_session().insert_gzszf_data_ztfw(ExampleData)

    def parser_web_next(self, meta):
        num_page = int(self.get_num_of_page(meta['url']))
        self.parser_web_right(meta['url'], meta)
        if num_page > 1:
            ([self.parser_web_right(meta['url'] + 'index_' + str(i) + '.html', meta) for i in
              range(1, int(num_page))])

    def parser_web(self, bs):
        self.parser_web_left(bs)

    def get_data_examples(self):
        '''
        获取爬虫数据
        :return:[ZTFWData对象,..]
        '''
        bs = self.get_url_beautiful_object(self.url)
        self.parser_web_left(bs)


def main():
    url = "http://www.guizhou.gov.cn/zwfw/ztfw/jyfw/zcfg/index.html"  # 专题服务网页:url
    processor = ZTFUProcessor(url)  # 初始化专题服务处理器
    processor.get_data_examples()  # 爬取专题服务网站数据


if __name__ == '__main__':
    main()
