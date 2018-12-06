# -*- coding: utf-8 -*- 
# @Time : 2018/11/28 17:38 
# @Author : Allen 
# @Site :  数据库操作
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.models import *
from datetime import datetime
import uuid


def get_datetime():
    return datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S')


def get_uuid():
    return str(uuid.uuid4()).replace('-', '')


class ModelService(object):
    def __init__(self):
        self.db_session = sessionmaker(
            bind=create_engine('mysql+pymysql://root:gzszf@172.16.205.69:3306/gzszf_db?charset=utf8'))

    def insert_gzszf_data_ztfw_theme(self):
        pass

    def insert_gzszf_data_ztfw(self, ZTFWData):
        session = self.db_session()
        theme_id = self.query_gzszf_data_ztfw_theme_id_by_theme(ZTFWData.theme)
        if theme_id:
            session.add(
                GzszfDataZtfw(
                    id=get_uuid(),
                    theme_id=theme_id[0],
                    title=ZTFWData.title,
                    content=ZTFWData.content,
                    publish_time=ZTFWData.publish_time,
                    resource=ZTFWData.resource,
                    url=ZTFWData.detail_url,
                    create_time=get_datetime(),
                    update_time=get_datetime()
                )
            )
            print("Success insert : {}".format(ZTFWData.title))
            session.commit()
            session.close()
        else:
            session.add(
                GzszfDataZtfwTheme(
                    id=get_uuid(),
                    theme=ZTFWData.theme,
                    url=ZTFWData.theme_url,
                    create_time=get_datetime(),
                    update_time=get_datetime(),
                )
            )
            session.commit()
            print("Success insert theme: {}".format(ZTFWData.theme))
            self.insert_gzszf_data_ztfw(ZTFWData)

    def query_gzszf_data_ztfw_theme_id_by_theme(self, theme):
        session = self.db_session()
        id = session.query(GzszfDataZtfwTheme.id).filter(GzszfDataZtfwTheme.theme == theme).first()
        session.close()
        return id

    def query_gzszf_data_ztfw_id_by_url(self, url):
        session = self.db_session()
        id = session.query(GzszfDataZtfw.id).filter(GzszfDataZtfw.url == url).first()
        session.close()
        return id

    def insert_gzszf_data_jdhy(self, JUHYData):
        session = self.db_session()
        session.add(
            GzszfDataJdhy(
                id=get_uuid(),
                url=JUHYData.url,
                title=JUHYData.title,
                content=JUHYData.content,
                publish_time=JUHYData.publish_time,
                resource=JUHYData.resource,
                create_time=get_datetime(),
                update_time=get_datetime(),
            )
        )
        session.commit()
        print("Success insert :{}".format(JUHYData.title))
        session.close()

    def query_gzszf_data_jdhy_by_url(self, url):
        session = self.db_session()
        id = session.query(GzszfDataJdhy.id).filter(GzszfDataJdhy.url == url).first()
        session.close()
        return id

    def insert_gzszf_data_zwgk(self, ZWGKData):
        session = self.db_session()
        if ZWGKData.parent_theme:
            parent_id = self.query_gzszf_data_zwgk_theme_id_by_theme(ZWGKData.parent_theme)
            if parent_id:
                theme_id = self.query_gzszf_data_zwgk_theme_id_by_theme(ZWGKData.theme)
                if theme_id:
                    session.add(
                        GzszfDataZwgk(
                            id=get_uuid(),
                            theme_id=theme_id[0],
                            title=ZWGKData.title,
                            content=ZWGKData.content,
                            publish_time=ZWGKData.publish_time,
                            resource=ZWGKData.resource,
                            url=ZWGKData.url,
                            create_time=get_datetime(),
                            update_time=get_datetime()
                        )
                    )
                    session.commit()
                    session.close()
                    print("Success insert :{}".format(ZWGKData.title))
                else:
                    self.insert_gzszf_data_zwgk_theme(ZWGKData.theme, ZWGKData.theme_url, parent_id[0])
                    self.insert_gzszf_data_zwgk(ZWGKData)
            else:
                self.insert_gzszf_data_zwgk_theme(ZWGKData.parent_theme, ZWGKData.theme_url, '')
                self.insert_gzszf_data_zwgk(ZWGKData)
        else:
            theme_id = self.query_gzszf_data_zwgk_theme_id_by_theme(ZWGKData.theme)
            if theme_id:
                session.add(
                    GzszfDataZwgk(
                        id=get_uuid(),
                        theme_id=theme_id[0],
                        title=ZWGKData.title,
                        content=ZWGKData.content,
                        publish_time=ZWGKData.publish_time,
                        resource=ZWGKData.resource,
                        url=ZWGKData.url,
                        create_time=get_datetime(),
                        update_time=get_datetime()
                    )
                )
                session.commit()
                session.close()
                print("Success insert :{}".format(ZWGKData.title))
            else:
                self.insert_gzszf_data_zwgk_theme(ZWGKData.theme, ZWGKData.theme_url, '')
                self.insert_gzszf_data_zwgk(ZWGKData)

    def insert_gzszf_data_zwgk_theme(self, theme, theme_url, parent_id):
        session = self.db_session()
        session.add(
            GzszfDataZwgkTheme(
                id=get_uuid(),
                theme=theme,
                url=theme_url,
                parent_id=parent_id,
                create_time=get_datetime(),
                update_time=get_datetime(),
            )
        )
        session.commit()
        session.close()
        print("Success insert :{}".format(theme))

    def query_gzszf_data_zwgk_theme_id_by_theme(self, theme):
        session = self.db_session()
        id = session.query(GzszfDataZwgkTheme.id).filter(GzszfDataZwgkTheme.theme == theme).first()
        session.close()
        return id

    def query_gzszf_data_zwgk_id_by_url(self, url):
        session = self.db_session()
        id = session.query(GzszfDataZwgk.id).filter(GzszfDataZwgk.url == url).first()
        session.close()
        return id

    def insert_gzszf_data_xwdt(self, GZSZFData):
        session = self.db_session()
        session.add(
            GzszfDataXwdt(
                id=get_uuid(),
                title=GZSZFData.title,
                publish_time=GZSZFData.publish_time,
                url=GZSZFData.url,
                create_time=get_datetime(),
                update_time=get_datetime()
            )
        )
        print("Success insert ：{}".format(GZSZFData.title))
        session.commit()
        session.close()

    def query_gzszf_data_xwdt_id_by_url(self, url):
        session = self.db_session()
        id = session.query(GzszfDataXwdt.id).filter(GzszfDataXwdt.url == url).first()
        session.close()
        return id
