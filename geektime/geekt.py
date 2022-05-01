import os
import re
from concurrent.futures import ThreadPoolExecutor
from random import randrange
from time import sleep

import markdownify
import requests

from geektime.course import get_course_info, get_chapters, get_articles, get_article
from utils import write_bytes, write_file, mkdir, to_markdown, to_epub, to_pdf


def fix_content_heading(content):
    h2_start, h2_end = re.compile('<h2.*?>'), re.compile('</h2>')
    h3_start, h3_end = re.compile('<h3.*?>'), re.compile('</h3>')
    h4_start, h4_end = re.compile('<h4.*?>'), re.compile('</h4>')
    h5_start, h5_end = re.compile('<h5.*?>'), re.compile('</h5>')
    content = re.sub(h5_start, '<h6>', content)
    content = re.sub(h5_end, '</h6>', content)
    content = re.sub(h4_start, '<h5>', content)
    content = re.sub(h4_end, '</h5>', content)
    content = re.sub(h3_start, '<h4>', content)
    content = re.sub(h3_end, '</h4>', content)
    content = re.sub(h2_start, '<h3>', content)
    content = re.sub(h2_end, '</h3>', content)
    return content


class GeekT:
    def __init__(self, courses, token=os.getenv('GEEKT_TOKEN'), gcid=os.getenv('GEEKT_GCID'), base_dir='.', epub=True,
                 pdf=True, audio=False, worker=5, force=False):
        self.courses = courses
        self.token = token
        self.gcid = gcid
        self.base_dir = base_dir
        self.epub = epub
        self.pdf = pdf
        self.audio = audio
        self.worker = worker
        self.force = force
        # 初始化目录
        mkdir(base_dir)

    # 单线程爬取内容
    def run(self):
        print(f'start {len(self.courses)} courses!')
        for course in self.courses:
            self._handle_course(course)
        print('all complete')

    def trans(self):
        print(f'start {len(self.courses)} courses!')
        pool = ThreadPoolExecutor(max_workers=self.worker)
        _ = [pool.submit(self._trans_course, course) for course in self.courses]
        pool.shutdown(wait=True)
        print('all complete')

    def _handle_course_meta(self, course_id):
        meta = get_course_info(course_id, self.token, self.gcid)['data']
        cover = meta['cover']['rectangle'] or meta['cover']['square']
        author = meta['author']['name']
        title = meta['title']
        cid = meta['extra']['cid']
        course_dir = os.path.join(self.base_dir, title)
        mkdir(course_dir)
        write_bytes(os.path.join(course_dir, 'cover.png'), requests.get(cover).content)
        write_file(os.path.join(course_dir, 'meta.yaml'), f"""\
title: {title}
author: {author}
cover-image: {course_dir}/cover.png
css: ./style.css
""")
        print(f'{title} course meta added')
        return {'title': title, 'course_dir': course_dir, 'cid': cid, 'is_video': meta['is_video']}

    def _trans_course(self, course_id):
        meta = self._handle_course_meta(course_id)
        course_dir = meta['course_dir']
        title = meta['title']
        if meta['is_video']:
            print(f'id {course_id} - {title} is video lesson, skip')
            return
        to_markdown(course_dir, self.force)
        if self.epub:
            to_epub(course_dir, self.force)
        if self.pdf:
            to_pdf(course_dir, self.force)
        print(f'finish course {title} - id {course_id}')

    def _handle_course(self, course_id):
        meta = self._handle_course_meta(course_id)
        course_dir = meta['course_dir']
        cid = meta['cid']
        title = meta['title']
        if meta['is_video']:
            print(f'id {course_id} - {title} is video lesson, skip')
            return
        chapters = self._handle_chapters(cid, course_dir)
        chapters = self._handle_articles(cid, chapters)
        for chapter in chapters.values():
            for idx, article_id in enumerate(chapter['articles']):
                self._handle_article(idx, str(article_id), chapter['chapter_dir'])
        print(f'finish course {title} - id {course_id}')

    def _handle_chapters(self, course_cid, course_dir):
        chapters = get_chapters(course_cid, self.token, self.gcid)['data']
        res = dict()
        for idx, chapter in enumerate(chapters):
            chapter_name = chapter['title']
            chapter_dir = os.path.join(course_dir, f'{idx}.{chapter_name.replace("/", "")}')
            mkdir(chapter_dir)
            print(f'mkdir {chapter_dir}')
            # 3.6+ 是有序集合
            res[chapter['id']] = {
                'chapter_name': chapter_name,
                'id': chapter['id'],
                'idx': idx,
                'chapter_dir': chapter_dir,
                'articles': []
            }
        return res

    def _handle_articles(self, cid, chapters):
        articles = get_articles(cid, self.token, self.gcid)['data']['list']
        for article in articles:
            chapters[article['chapter_id']]['articles'].append(article['id'])
        return chapters

    def _handle_article(self, idx, aid, chapter_dir):
        article = get_article(str(aid), self.token, self.gcid)['data']
        content = article['article_content']
        audio = article['audio_download_url']
        title = article['article_title']
        filename = os.path.join(chapter_dir, f'{idx}.{title.replace("/", "")}')
        if self.audio:
            write_bytes(f'{filename}.mp3', requests.get(audio).content)
        write_file(f'{filename}.html', content)
        markdown_file = markdownify.markdownify(html=f'<h2>{title}</h2>{fix_content_heading(content)}',
                                                heading_style='ATX')
        write_file(f'{filename}.md', markdown_file)
        sleep(randrange(1, 5))
        print(f'save lesson finish: {title}')
