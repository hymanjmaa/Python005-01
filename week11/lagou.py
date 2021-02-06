#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project Name: Python005-01
@Author: 'Hyman MA'
@Email: 'hymanjma@gmail.com'
@Time: 2021/2/1 17:36
"""
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from lxml import etree
import random
import time
import re
from sqlalchemy.orm import sessionmaker
import pymysql
from sqlalchemy import create_engine, Table, Float, Column, Integer, SmallInteger, DateTime, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import DateTime, func, and_, or_
import threading
from matplotlib import pyplot as plt


Base = declarative_base()
db_url = "mysql+pymysql://root:root@localhost/testdb?charset=utf8mb4"
engine = create_engine(db_url, echo=True, encoding="utf-8")
SessionClass = sessionmaker(bind=engine)
session = SessionClass()


class Job(Base):
    __tablename__ = 'job'

    job_id = Column(Integer, primary_key=True, autoincrement=True)
    region = Column(Integer)
    company_id = Column(Integer)
    company_name = Column(String(128))
    job_name = Column(String(128))
    salary_minimum = Column(Integer)
    salary_maxinum = Column(Integer)
    district = Column(String(128))
    logo = Column(String(256))
    tags = Column(String(128))
    advantage = Column(String(512))
    industry = Column(String(128))
    exp = Column(String(128))
    degree = Column(String(128))

    create_time = Column(DateTime)
    update_time = Column(DateTime)


class LaGou(threading.Thread):
    def __init__(self, city_id, dp):
        super().__init__()
        self.driver_path = dp
        self.use_chrome_browser()
        self.city_id = city_id

    def use_chrome_browser(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(executable_path=self.driver_path, chrome_options=chrome_options)

    def run(self):
        list_url = 'https://www.lagou.com/jobs/list_Python/p-city_{}?px=default#filterBox'.format(self.city_id)
        self.browser.get(list_url)
        element = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'salary'))
        )
        print('salary text：', element.text)
        # 如果出现红包弹层，那关闭它
        time.sleep(0.5)
        if self.is_element_exist(By.CSS_SELECTOR, '.body-container .body-btn'):
            self.browser.find_element_by_css_selector('.body-container .body-btn').click()
            print('关闭红包弹层')

        page_count = 0
        job_count = 0
        while True:
            page_count += 1
            # 处理并记录当前列表信息到数据库
            time.sleep(random.randint(1000, 2000) * 0.001)
            self.parse_list_page(self.browser.page_source)

            # 获取下一页按钮，当可用时，点击跳转下一页
            if not self.is_element_exist(By.CSS_SELECTOR, '.pager_next.pager_next_disabled'):
                self.browser.find_element_by_css_selector('.pager_next').click()
                WebDriverWait(self.browser, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, 'salary'))
                )
                time.sleep(1)
                print('next page')
            else:
                break

        print('顺利完成,共(%s)页(%s)条' % (page_count, job_count))

    def parse_list_page(self, page_source):
        """
        :param page_source: 列表页的html字串
        :return:
        """
        page = etree.HTML(page_source)
        jobs = page.xpath('//li[contains(@class,"con_list_item")]')
        jobs_info = []
        for i in jobs:
            item = {
                'job_id': i.xpath('./@data-positionid')[0],
                'company_id': i.xpath('./@data-companyid')[0],
                'company_name': i.xpath('./@data-company')[0],
                'name': i.xpath('./@data-positionname')[0],
                'salary': i.xpath('./@data-salary')[0],
                # 'company_name': i.xpath('string(.//div[@class="company_name"]//a)'),
                # 'name': i.xpath('string(.//h3)'),
                # 'salary': i.xpath('string(.//span[@class="money"])'),
                'district': i.xpath('string(//span[@class="add"])').strip('[]'),
                'industry': i.xpath('string(.//div[@class="industry"])').strip(),
                'logo': i.xpath('.//div[@class="com_logo"]//img/@src')[0],
                'link': i.xpath('.//a[@class="position_link"]/@href')[0],
                'tags': i.xpath('.//div[@class="list_item_bot"]//span/text()'),
                'advantage': i.xpath('.//div[@class="list_item_bot"]/div[last()]/text()')[0].strip('“”'),
                'post_at': i.xpath('.//span[@class="format-time"]/text()')[0],
            }
            exp, degree = ''.join(i.xpath('.//div[@class="p_bot"]/div/text()')).strip().split(' / ')

            item['exp'] = exp
            item['degree'] = degree

            salary_minimum, salary_maxinum = item['salary'].replace('k', '').replace('K', '').split('-')

            job = session.query(Job).filter(Job.region == self.city_id,
                                            Job.job_name == item['name'],
                                            Job.salary_minimum == int(salary_minimum),
                                            Job.salary_maxinum == int(salary_maxinum)).first()
            if job is None:
                try:
                    job = Job(job_id=item['job_id'], region=self.city_id, company_id=item['company_id'],
                              company_name=item['company_name'], job_name=item['name'],
                              salary_minimum=salary_minimum, salary_maxinum=salary_maxinum,
                              district=item['district'], logo=item['logo'],
                              tags=','.join(item['tags']), advantage=item['advantage'],
                              industry=item['industry'], exp=item['exp'],
                              degree=item['degree'], create_time=datetime.utcnow(),
                              update_time=datetime.utcnow())
                    session.merge(job)
                    session.commit()
                except:
                    print('sql execute error')
                    continue

            print(item)
            # jobs_info.append(item)

        # print('列表页获得数据：', jobs_info)

    def is_element_exist(self, by, value):
        """
        用来判断标签元素是否存在
        :param by: 条件类型
        :param value: 条件内容
        :return:
        """
        try:
            self.browser.find_element(by=by, value=value)

        except NoSuchElementException as e:
            # 发生了NoSuchElementException异常，说明页面中未找到该元素，返回False
            return False
        else:
            return True


def show_rate(city_id):
    job_data = session.query(Job).with_entities(
        session.query(Job).with_entities(func.count(Job.job_id)).filter(Job.salary_minimum >= 0,
                                                                        Job.salary_maxinum <= 8).label('one'),
        session.query(Job).with_entities(func.count(Job.job_id)).filter(Job.salary_minimum >= 8,
                                                                        Job.salary_maxinum <= 15).label('two'),
        session.query(Job).with_entities(func.count(Job.job_id)).filter(Job.salary_minimum >= 15,
                                                                        Job.salary_maxinum <= 30).label('three'),
        session.query(Job).with_entities(func.count(Job.job_id)).filter(Job.salary_minimum >= 30,
                                                                        Job.salary_maxinum <= 60).label('four'),
        session.query(Job).with_entities(func.count(Job.job_id)).filter(Job.salary_minimum >= 60).label('five'),
        func.count(Job.job_id).label('total')
        ).filter(Job.region == city_id).first()

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(7.5, 5), dpi=80)  # 调节画布的大小
    labels = ['0-8k', '8-15k', '15-30k', '30-60k', '60k+']  # 定义各个扇形的面积/标签
    sizes = [round(job_data.one/job_data.total, 2),
             round(job_data.two/job_data.total, 2),
             round(job_data.three/job_data.total, 2),
             round(job_data.four/job_data.total, 2),
             round(job_data.five/job_data.total, 2)]  # 各个值，影响各个扇形的面积
    colors = ['red', 'yellowgreen', 'lightskyblue', 'yellow', 'purple']  # 每块扇形的颜色
    explode = (0.01, 0.01, 0.01, 0.01, 0.01)
    patches, text1, text2 = plt.pie(sizes,
                                    explode=explode,
                                    labels=labels,
                                    colors=colors,
                                    labeldistance=1.2,  # 图例距圆心半径倍距离
                                    autopct='%3.2f%%',  # 数值保留固定小数位
                                    shadow=False,  # 无阴影设置
                                    startangle=90,  # 逆时针起始角度设置
                                    pctdistance=0.6)  # 数值距圆心半径倍数距离
    # patches饼图的返回值，texts1为饼图外label的文本，texts2为饼图内部文本
    plt.axis('equal')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    # Base.metadata.create_all(engine)
    driver_path = '/Users/hyman/py5/Python005-01/week02/chromedriver'

    city_ids = [213, 215, 2, 3]
    thead_list = []
    for cid in city_ids:
        lg = LaGou(cid, driver_path)
        lg.start()
        thead_list.append(lg)

    for t in thead_list:
        t.join()

    # LaGou(2, driver_path).run()
    # LaGou(3, driver_path).run()
    # LaGou(213, driver_path).run()
    # LaGou(215, driver_path).run()

    # show_rate(3)
    # show_rate(2)
    # show_rate(213)
    # show_rate(215)