# -*- coding: utf-8 -*- 
# @Time : 2018/11/29 10:47 
# @Author : Allen 
# @Site :  crawl 政务公开
from crawl_processor import CrawlProcessor
from data_example import ZWGKData
import re


class ZWGKProcessor(CrawlProcessor):
    def __init__(self, url):
        self.url = url

    def insert_data(self, ExampleData):
        self.get_db_session().insert_gzszf_data_zwgk(ExampleData)

    def parser_web_left(self, url):
        def parser_url_from_script(x):
            def regex_theme(x):
                return re.findall(r"var str3 = '[\u4e00-\u9fa5]+'", str(x))[0]

            def regex_theme_url(x):
                return re.findall(r"var str4 = .+", str(x))[0]

            theme = regex_theme(x)[12:-1]
            theme_url = regex_theme_url(x)[15:-2]
            if not theme_url:
                theme_url = url
            if theme == '省政府文件':
                self.parser_web_left(r'http://www.guizhou.gov.cn/zwgk/fgwj/szfwj_8191/szfl_8192/index.html')
            else:
                if 'szfwj' in url:
                    if len(theme_url) < 30:
                        meta = {'省政府文件': {theme: r'http://www.guizhou.gov.cn/zwgk/fgwj/szfwj_8191/' + theme_url}}
                    else:
                        meta = {'省政府文件': {theme: theme_url}}
                    self.parser_web_right(meta)
                else:
                    if len(theme_url) < 20:
                        meta = {theme: r'http://www.guizhou.gov.cn/zwgk/fgwj/' + theme_url}
                    else:
                        meta = {theme: theme_url}
                    self.parser_web_right(meta)

        list(map(parser_url_from_script,
                 self.get_url_beautiful_object(url).find('div', 'left-nav').ul.find_all('script')))

    def parser_web_right(self, meta):
        for k, v in meta.items():
            try:
                if isinstance(v, dict):
                    for _k, _v in v.items():
                        if _k == '文件修改废止情况':
                            self.get_web_right(_v + 'xgfzqk/', meta)
                        elif _k != '规范性文件备案审查':
                            self.get_web_right(_v, meta)
                else:
                    self.get_web_right(v, meta)
            except Exception as e:
                print(e)
                print(meta)

    def get_web_right_url(self, url, meta):
        list(
            map(lambda x: self.get_web_example(x.a['href'], meta),
                self.get_url_beautiful_object(url).find('div', 'right-list-box').find_all('li')))

    def get_web_example(self, url, meta):
        if not self.get_db_session().query_gzszf_data_zwgk_id_by_url(url):
            try:
                title, resource, publish_time, content = self.parser_web_detail(url)
                for k, v in meta.items():
                    if isinstance(v, dict):
                        parent_theme = k
                        for _k, _v in v.items():
                            theme = _k
                            theme_url = _v
                    else:
                        theme = k
                        theme_url = v
                        parent_theme = ''
                self.insert_data(ZWGKData(url, title, content, publish_time, resource, theme, theme_url, parent_theme))
            except Exception as e:
                print(e)
                print("Error url : {}".format(url))

    def get_web_right(self, url, meta):
        num = int(self.get_num_of_page(url))
        self.get_web_right_url(url, meta)
        if num > 1:
            ([self.get_web_right_url(url + 'index_' + str(i) + '.html', meta) for i in range(1, num)])

    def get_data_examples(self):
        '''
        获取爬虫数据
        :return:
        '''
        self.parser_web_left(self.url)


def main():
    url = 'http://www.guizhou.gov.cn/zwgk/fgwj/gfxwj/'
    processor = ZWGKProcessor(url)
    processor.get_data_examples()


if __name__ == '__main__':
    main()
