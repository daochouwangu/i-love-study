import json
from random import randrange

import requests


def post(url, data, gcess, gcid):
    r = requests.post(url, data=json.dumps(data),
                      cookies={'GCESS': gcess, 'GCID': gcid},
                      headers={
                          'Content-Type': 'application/json',
                          'Origin': 'https://time.geekbang.org',
                          'Referer': 'https://time.geekbang.org/column/intro/100109201',
                          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
                      })
    if r.status_code == 451:
        randrange(1, 5)
        print('451 retry')
        r = post(url, data, gcess, gcid)
    return r
