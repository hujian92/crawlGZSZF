# -*- coding: utf-8 -*- 
# @Time : 2018/11/29 9:13 
# @Author : Allen 
# @Site :数据对象

class ZTFUData(object):
    '''专题服务object'''

    def __init__(self, theme, theme_url, detail_url=None, title=None, content=None, publish_time=None, resource=None):
        self.theme = theme
        self.theme_url = theme_url
        self.detail_url = detail_url
        self.title = title
        self.content = content
        self.publish_time = publish_time
        self.resource = resource


class JDHYData(object):
    '''解读回应object'''

    def __init__(self, url, title, content, publish_time, resource):
        self.url = url
        self.title = title
        self.content = content
        self.publish_time = publish_time
        self.resource = resource


class ZWGKData(object):
    '''政务公开'''

    def __init__(self, url, title, content, publish_time, resource, theme, theme_url, parent_theme):
        self.url = url
        self.title = title
        self.content = content
        self.publish_time = publish_time
        self.resource = resource
        self.theme = theme
        self.theme_url = theme_url
        self.parent_theme = parent_theme


class XWDTData(object):
    def __init__(self, title, url, publish_time):
        self.title = title
        self.url = url
        self.publish_time = publish_time
