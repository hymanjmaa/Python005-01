#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project Name: Python005-01
@Author: 'Hyman MA'
@Email: 'hymanjma@gmail.com'
@Time: 2020/12/6 12:07
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import random
from pathlib import Path
from lxml import etree
import json

p = Path(__file__)
base_path = p.resolve().parent


def selenium_get_zhihu_page(question_page):
    """
    use selenium get page html
    :param question_page: zhihu question page url
    :return:
    """

    # 加载xpath插件
    chrome_options = webdriver.ChromeOptions()
    extension_path = base_path.joinpath('chrome_Xpath_v2.0.2.crx')
    chrome_options.add_extension(extension_path)

    # chrome_options.add_argument('--headless')  # 设置chrome无头 会导致xpath插件加载失败
    browser = webdriver.Chrome(executable_path=base_path.joinpath('chromedriver'), chrome_options=chrome_options)
    browser.maximize_window()
    wait = WebDriverWait(browser, 25)
    waitPopWindow = WebDriverWait(browser, 25)

    browser.get(question_page)

    print('wait qrcode load...')
    time.sleep(random.randint(10, 15))

    try:
        qrcode_window = browser.find_element_by_xpath('//button[@class="Button Modal-closeButton Button--plain"]')
        qrcode_window.click()
        print('catch qrcode window and close success')
    except Exception as e:
        print(f"catch qrcode window fail, e = {e}")

    scroll_js = "var q=document.documentElement.scrollTop={}"
    browser.execute_script(scroll_js.format(100000))
    print('滑动到底部...')

    time.sleep(random.randint(1, 3))
    browser.execute_script(scroll_js.format(500))
    print('向上滑...')  # 否则下边内容不加载
    time.sleep(random.randint(1, 3))

    scroll_top = 100000
    for x in range(10):  # 可将页面高度不再变化作为终止条件以获取所有回答
        browser.execute_script(scroll_js.format(scroll_top))

        print("拖动滚动条....")
        scroll_top += 100000
        time.sleep(random.randint(5, 10))

    html = browser.find_element_by_xpath("//*").get_attribute("outerHTML")
    browser.quit()
    save_answer_data(html, question_page.split('/')[-1])
    print('{} 已保存'.format(question_page))


def save_answer_data(html_data, question_id):
    """
    use xpath get useful data and save to file
    :param html_data: str, html content
    :param question_id: str
    :return:
    """

    html = etree.HTML(html_data)

    user_name = html.xpath('//div[@class="List-item"]/div/div[@class="ContentItem-meta"]/div/meta[@itemprop="name"]/@content')
    user_img = html.xpath('//div[@class="List-item"]/div/div[@class="ContentItem-meta"]/div/meta[@itemprop="image"]/@content')
    user_url = html.xpath('//div[@class="List-item"]/div/div[@class="ContentItem-meta"]/div/meta[@itemprop="url"]/@content')
    user_follow_count = html.xpath('//div[@class="List-item"]/div/div[@class="ContentItem-meta"]/div/meta[@itemprop="zhihu:followerCount"]/@content')

    upvote_count = html.xpath('//div[@class="List-item"]/div/meta[@itemprop="upvoteCount"]/@content')
    ans_url = html.xpath('//div[@class="List-item"]/div/meta[@itemprop="url"]/@content')
    create_time = html.xpath('//div[@class="List-item"]/div/meta[@itemprop="dateCreated"]/@content')
    last_update = html.xpath('//div[@class="List-item"]/div/meta[@itemprop="dateModified"]/@content')
    comment_count = html.xpath('//div[@class="List-item"]/div/meta[@itemprop="commentCount"]/@content')
    rich_content = html.xpath('//div[@class="List-item"]/div/div[@class="RichContent RichContent--unescapable"]/div[@class="RichContent-inner"]/span')

    answer_l = []
    for idx, name in enumerate(user_name):
        answer_d = dict(user_name=name,
                        user_img=user_img[idx],
                        user_url=user_url[idx],
                        user_follow_count=user_follow_count[idx],
                        upvote_count=upvote_count[idx],
                        ans_url=ans_url[idx],
                        create_time=create_time[idx],
                        last_update=last_update[idx],
                        comment_count=comment_count[idx],
                        rich_content=rich_content[idx].xpath('string(.)').strip())
        answer_l.append(answer_d)

    with open(base_path.joinpath(f'{question_id}.json'), 'w') as ff:
        ff.write(json.dumps(answer_l))


if __name__ == '__main__':
    selenium_get_zhihu_page("https://www.zhihu.com/question/27343167")
