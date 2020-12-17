#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project Name: Python005-01
@Author: 'Hyman MA'
@Email: 'hymanjma@gmail.com'
@Time: 2020/12/17 22:54
"""
import requests
from lxml import etree
from pathlib import Path
import json


p = Path(__file__)
base_path = p.resolve().parent
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}


def get_douban_comments(url, page):
    comments = []
    for x in range(page):
        resp = requests.get(url + '&start={}'.format(x*20), headers=headers)

        html = etree.HTML(resp.text)

        comment_content = html.xpath('//div[@class="comment-item "]/div[@class="comment"]/p/span/text()')
        pub_time = html.xpath('//div[@class="comment-item "]/div[@class="comment"]/h3/span[@class="comment-info"]/span[@class="comment-time "]/@title')
        star = html.xpath('//div[@class="comment-item "]/div[@class="comment"]/h3/span[@class="comment-info"]/span[contains(@class, "rating")]/@class')

        for idx, content in enumerate(comment_content):
            comment_d = dict(content=content,
                             pub_time=pub_time[idx],
                             star=star[idx].replace('allstar', '').replace('rating', '').strip() if len(star) > idx else 0)
            comments.append(comment_d)

    with open(base_path.joinpath('comments.json'), 'w') as ff:
        ff.write(json.dumps(comments))


if __name__ == '__main__':
    get_douban_comments('https://movie.douban.com/subject/34894753/comments?limit=20&status=P&sort=new_score', 10)
