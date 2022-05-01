import requests


def get(url, params, token):
    return requests.get(url, params=params, cookies={'edu_gate_login_token': token}, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'Refer': 'https://kaiwu.lagou.com/',
        'Origin': 'https://kaiwu.lagou.com',
        'x-l-req-header': '{deviceType:1}'
    })
