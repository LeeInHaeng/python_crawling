import ssl
from urllib.request import Request, urlopen
import datetime


def crawling(
        url='',
        encoding='utf-8',
        err=lambda e: print('%s : %s' % (e, datetime.datetime.now())),
        proc1=lambda data: data,
        proc2=lambda data: data
    ):

    try:
        request = Request(url)

        context = ssl._create_unverified_context()
        response = urlopen(request, context=context)
        print(f'{datetime.datetime.now()} : success for request [{url}]')

        receive = response.read()

        result = proc2(proc1(receive.decode(encoding, errors='replace')))

        return result
    except Exception as e:
        err(e)