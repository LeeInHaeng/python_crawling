from itertools import count
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import ssl
import datetime
import pandas as pd
from selenium import webdriver
import time

from collection import crawler


def crawling_pelicana():
    results = []

    for page in count(111):
        url = 'https://pelicana.co.kr/store/stroe_search.html?branch_name=&gu=&si=&page=%d' % page
        html = crawler.crawling(url)

        bs = BeautifulSoup(html, 'html.parser')
        tag_table = bs.find('table', attrs={'class': 'table mt20'})
        tag_tbody = tag_table.find('tbody')
        tags_tr = tag_tbody.findAll('tr')

        # 끝 검출
        if len(tags_tr) == 0:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[3]
            sidogu = address.split(' ')[:2]
            results.append((name, address) + tuple(sidogu))

    for result in results:
        print(result)

    # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugun'])
    # print(table)
    table.to_csv('__results__/pelicana.csv', encoding='utf-8', mode='w', index=True)

def crawling_nene():
    results = []

    for page in count(45):
        url = 'https://nenechicken.com/17_new/sub_shop01.asp?ex_select=1&ex_select2=&IndexSword=&GUBUN=A&page=%d' % page
        html = crawler.crawling(url)

        bs = BeautifulSoup(html, 'html.parser')
        shopInfos = bs.findAll('div', attrs={'class': 'shopInfo'})

        # 끝 검출
        pagination = bs.find('div', attrs={'class': 'pagination'})
        if page > int(pagination.findAll('a')[-2].text):
            break

        for shopInfo in shopInfos:
            strings = list(shopInfo.strings)

            if strings[4] != '\n':
                name = strings[4]
                address = strings[6]
            else:
                name = strings[6]
                address = strings[8]

            sidogu = address.split(' ')
            results.append((name, address) + tuple([''.join(sidogu[:2]), ''.join(sidogu[2:])]))

    for result in results:
        print(result)

    # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugun'])
    # print(table)
    table.to_csv('__results__/nene.csv', encoding='utf-8', mode='w', index=True)


def crawling_kyochon():
    results = []

    for sido1 in range(1, 2):
        for sido2 in count(1):
            url = 'http://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d&txtsearch=' % (sido1, sido2)
            html = crawler.crawling(url)

            # 끝 검출
            if html is None:
                break

            bs = BeautifulSoup(html, 'html.parser')
            tag_ul = bs.find('ul', attrs={'class': 'list'})
            tags_span = tag_ul.findAll('span', attrs={'class': 'store_item'})

            for tag_span in tags_span:
                strings = list(tag_span.strings)

                name = strings[1]
                address = strings[3].replace('\r\n\t', '').strip()
                sidogu = address.split(' ')[:2]

                results.append((name, address) + tuple(sidogu))

    for result in results:
        print(result)

    # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugun'])
    # print(table)
    table.to_csv('__results__/kyochon.csv', encoding='utf-8', mode='w', index=True)


def crawling_goobne():
    results = []

    url = 'http://www.goobne.co.kr/store/search_store.jsp'

    wd = webdriver.Chrome('E:\\cafe24\\bin\\chromedriver.exe')
    wd.get(url)
    time.sleep(5)

    for page in count(102):
        # javascript 실행
        script = 'store.getList(%d)' % page
        wd.execute_script(script)
        print(f'{datetime.datetime.now()} : success for request [{script}]')
        time.sleep(3)

        # 동적으로 렌더링된 실행 결과 가져오기
        html = wd.page_source

        bs = BeautifulSoup(html, 'html.parser')
        tag_tbody = bs.find('tbody', attrs={'id': 'store_list'})
        tags_tr = tag_tbody.findAll('tr')

        # 끝 검출
        if tags_tr[0].get('class') is None:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[6]
            sidogu = address.split(' ')[:2]

            results.append((name, address) + tuple(sidogu))

    wd.quit()
    for result in results:
        print(result)

    # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugun'])
    # print(table)
    table.to_csv('__results__/goobne.csv', encoding='utf-8', mode='w', index=True)


if __name__ == '__main__':
    # crawling_pelicana()
    crawling_nene()
    # crawling_kyochon()
    # crawling_goobne()