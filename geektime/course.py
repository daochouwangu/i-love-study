from geektime.request import post


# cid: int 从基本信息中拿到的 cid，如 411
# 获取分节信息
def get_chapters(cid, token, gcid):
    r = post('https://time.geekbang.org/serv/v1/chapters', {'cid': cid}, token, gcid)
    return r.json()


# aid: str
# 获取文章正文
def get_article(aid, token, gcid):
    r = post('https://time.geekbang.org/serv/v1/article', {'id': aid, 'include_neighbors': True, 'is_freelyread': True},
             token, gcid)
    print(r.status_code)
    return r.json()


# cid: str 从基本信息中拿到的 cid，如 411
# 获取文章列表；需要对应上分节
def get_articles(cid, token, gcid):
    r = post('https://time.geekbang.org/serv/v1/column/articles',
             {'cid': cid, 'size': 500, 'prev': 0, 'order': "earliest", 'sample': False}, token, gcid)
    return r.json()


# pid: int url 上的地址，比如：100078401
# 获取课程基本信息
def get_course_info(pid, token, gcid):
    r = post('https://time.geekbang.org/serv/v3/column/info', {'product_id': pid, 'with_recommend_article': True},
             token, gcid)
    return r.json()
