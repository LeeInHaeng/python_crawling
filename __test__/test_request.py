from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

from collection import crawler


def ex01():
    request = Request('http://movie.naver.com/movie/sdb/rank/rmovie.nhn')
    response = urlopen(request)
    html = response.read().decode('cp949')

    bs = BeautifulSoup(html, 'html.parser')
    divs = bs.findAll('div', attrs={'class': 'tit3'})
    # print(divs)
    for index, div in enumerate(divs):
        print(index+1, div.a.text, div.a['href'], sep=':')
    print('================================')


def proc_naver_movie_rank(html):
    bs = BeautifulSoup(html, 'html.parser')
    divs = bs.findAll('div', attrs={'class': 'tit3'})

    return divs


# def store_naver_movie_rank(data):
#     for index, div in enumerate(data):
#         print(index+1, div.a.text, div.a['href'], sep=':')
#
#     return data


def ex02():
    crawler.crawling(
        url='http://movie.naver.com/movie/sdb/rank/rmovie.nhn',
        encoding='cp949',
        proc1=proc_naver_movie_rank,
        proc2=lambda data: list(map(lambda div: print(div[0]+1, div[1].a.text, div[1].a['href'], sep=':'), enumerate(data)))
    )


__name__ == '__main__' and not ex01() and not ex02()
