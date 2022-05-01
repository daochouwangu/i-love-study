import os
from concurrent.futures import ThreadPoolExecutor
from time import sleep

import markdownify
import requests

from lagou.course import get_course_info, get_course_lesson_info, get_course_meta_info
from utils import mkdir, write_file, write_bytes, to_markdown, to_epub, to_pdf


class Lago:
    def __init__(self, courses, token=os.getenv('LAGO_TOKEN'), base_dir='.', epub=True, pdf=True, worker=5):
        self.courses = courses
        self.token = token
        self.base_dir = base_dir
        self.epub = epub
        self.pdf = pdf
        self.worker = worker
        
        # 初始化目录
        mkdir(base_dir)

    def run(self):
        print(f'start {len(self.courses)} courses!')
        for course in self.courses:
            self._handle_course(course)
            sleep(2)
        print('all complete')

    def trans(self):
        print(f'start {len(self.courses)} courses!')
        pool = ThreadPoolExecutor(max_workers=self.worker)
        _ = [pool.submit(self._trans_course, course).result() for course in self.courses]
        print('all complete')

    def _trans_course(self, course_id):
        info = get_course_info(course_id, self.token)['content']
        course_name = info['courseName']
        print(f'{course_name} start')
        course_dir = os.path.join(self.base_dir, course_name)
        self._handle_course_meta(course_id, course_dir)
        to_markdown(course_dir)
        if self.epub:
            to_epub(course_dir)
        if self.pdf:
            to_pdf(course_dir)
        print(f'finish course {course_name} - id {course_id}')

    def _handle_course(self, course_id):
        info = get_course_info(course_id, self.token)['content']
        course_name = info['courseName']
        print(f'{course_name} start')
        course_dir = os.path.join(self.base_dir, course_name)
        mkdir(course_dir)
        print(f'mkdir {course_dir}')
        course_sections = info['courseSectionList']
        self._handle_sections(course_sections, course_dir)

    def _handle_course_meta(self, course_id, course_dir):
        meta = get_course_meta_info(course_id, self.token)['content']
        cover = meta['coverImage']
        author = meta['teacherName']
        title = meta['courseName']
        response = requests.get(cover)
        write_bytes(os.path.join(course_dir, 'cover.png'), response.content)
        write_file(os.path.join(course_dir, 'meta.yaml'), f"""\
title: {title}
author: {author}
cover-image: {course_dir}/cover.png
css: ./style.css
""")
        print(f'{title} course meta added')

    def _handle_sections(self, sections, course_dir):
        for idx, section in enumerate(sections):
            section_name = section['sectionName']
            section_dir = os.path.join(course_dir, f'{idx}.{section_name.replace("/", "")}')
            mkdir(section_dir)
            print(f'mkdir {section_name}')
            self._handle_lessons(section['courseLessons'], section_dir)

    def _handle_lessons(self, lessons, section_dir):
        for idx, lesson in enumerate(lessons):
            lesson_id = lesson['id']
            lesson_name = lesson['theme']
            lesson_info = get_course_lesson_info(lesson_id, self.token)['content']
            content = lesson_info['textContent']
            filename = os.path.join(section_dir, f'{idx}.{lesson_name.replace("/", "")}')
            write_file(f'{filename}.html', content)
            markdown_file = markdownify.markdownify(html=f'<h2>{lesson_name}</h2>{content}', heading_style='ATX')
            write_file(f'{filename}.md', markdown_file)
            print(f'save lesson finish: {lesson_name}')
