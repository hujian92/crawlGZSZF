# -*- coding: utf-8 -*-
# @Time : 2018/11/28 17:37
# @Author : Allen
# @Site :  orm链接数据库
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base


class GzszfDataZtfw(declarative_base()):
    __tablename__ = 'gzszf_data_ztfw'
    id = Column(String(32), primary_key=True)
    theme_id = Column(String(32))
    title = Column(String(255))
    content = Column(Text)
    publish_time = Column(DateTime)
    resource = Column(String(255))
    url = Column(String(255))
    create_time = Column(DateTime)
    update_time = Column(DateTime)


class GzszfDataZtfwTheme(declarative_base()):
    __tablename__ = 'gzszf_data_ztfw_theme'
    id = Column(String(32), primary_key=True)
    theme = Column(String(100))
    url = Column(String(150))
    create_time = Column(DateTime)
    update_time = Column(DateTime)


class GzszfDataJdhy(declarative_base()):
    __tablename__ = 'gzszf_data_jdhy'
    id = Column(String(32), primary_key=True)
    url = Column(String(150))
    title = Column(String(150))
    content = Column(Text)
    publish_time = Column(DateTime)
    resource = Column(String(100))
    create_time = Column(DateTime)
    update_time = Column(DateTime)


class GzszfDataZwgk(declarative_base()):
    __tablename__ = 'gzszf_data_zwgk'
    id = Column(String(32), primary_key=True)
    theme_id = Column(String(32))
    title = Column(String(150))
    content = Column(Text)
    publish_time = Column(DateTime)
    resource = Column(String(100))
    url = Column(String(255))
    create_time = Column(DateTime)
    update_time = Column(DateTime)


class GzszfDataZwgkTheme(declarative_base()):
    __tablename__ = 'gzszf_data_zwgk_theme'
    id = Column(String(32), primary_key=True)
    parent_id = Column(String(32))
    theme = Column(String(100))
    url = Column(String(150))
    create_time = Column(DateTime)
    update_time = Column(DateTime)


class GzszfDataXwdt(declarative_base()):
    __tablename__ = 'gzszf_data_xwdt'
    id = Column(String(32), primary_key=True)
    title = Column(String(150))
    publish_time = Column(DateTime)
    url = Column(String(150))
    create_time = Column(DateTime)
    update_time = Column(DateTime)
