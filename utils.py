import os
import re

import pandoc
import yaml


def mkdir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    return


def write_bytes(filename, content):
    f = open(filename, 'bw')
    f.write(content)
    f.close()
    return


def write_file(filename, content):
    f = open(filename, 'w', encoding='utf8')
    f.write(content)
    f.close()
    return


def read_file(filename):
    f = open(filename, 'r', encoding='utf8')
    content = f.read()
    f.close()
    return content


def read_bytes(filename):
    f = open(filename, 'r')
    content = f.read()
    f.close()
    return content


def sort(dirs):
    return sorted(dirs, key=lambda x: int(x.split('.')[0] if x.split('.')[0].isdigit() else 0))


def to_markdown(root_dir, force=False):
    if not force and os.path.exists(os.path.join(root_dir, f'{os.path.basename(root_dir)}.md')):
        print(f'{root_dir} to markdown existed, skip')
        return
    else:
        print(f'{root_dir} start to create markdown')
    sections = os.listdir(root_dir)
    md = ''
    print('sections:')
    for section in sort(sections):
        section_path = os.path.join(root_dir, section)
        if not os.path.isdir(section_path):
            continue
        print(section)
        section_name = re.sub(r'^\d+\.', '', section)
        r = re.compile('.+\.md$')
        lessons = sort(os.listdir(section_path))
        lessons = [lesson for lesson in lessons if r.match(lesson)]
        md += f'# {section_name}\n'
        for lesson in lessons:
            md += read_file(os.path.join(root_dir, section, lesson))
    write_file(os.path.join(root_dir, f'{os.path.basename(root_dir)}.md'), md)
    print(f'{root_dir} to markdown finish')
    return md


def get_meta(root_dir):
    ym = read_file(os.path.join(root_dir, 'meta.yaml'))
    data = yaml.load(ym, Loader=yaml.Loader)
    return data['title'], data['author'], data['cover-image'], data['css']


def to_epub(root_dir, force=False):
    course_name = os.path.basename(root_dir)
    if not force and os.path.exists(os.path.join(root_dir, f'{course_name}.epub')):
        print(f'{root_dir} to epub existed, skip')
        return
    else:
        print(f'{root_dir} start to create epub')
    content = read_file(os.path.join(root_dir, f'{course_name}.md'))
    title, author, cover_image, css = get_meta(root_dir)

    doc = pandoc.write(pandoc.read(content, format='commonmark'), format='epub',
                       options=[f'--css={css}', f'--epub-cover-image={cover_image}',
                                '--metadata', f'author={author}', '--metadata', f'title={title}'])
    print(f'{root_dir} to epub finish')
    write_bytes(os.path.join(root_dir, f'{course_name}.epub'), doc)


def to_pdf(root_dir, force=False):
    course_name = os.path.basename(root_dir)
    if not force and os.path.exists(os.path.join(root_dir, f'{course_name}.pdf')):
        print(f'{root_dir} to pdf existed, skip')
        return
    else:
        print(f'{root_dir} start to create pdf')
    content = read_file(os.path.join(root_dir, f'{course_name}.md'))
    title, author, cover_image, css = get_meta(root_dir)

    doc = pandoc.write(pandoc.read(content, format='commonmark'), format='pdf',
                       options=['--pdf-engine=wkhtmltopdf', '--metadata', f'title={title}', f'--css={css}',
                                '--metadata', f'author={author}'])
    print(f'{root_dir} to pdf finish')
    write_bytes(os.path.join(root_dir, f'{course_name}.pdf'), doc)
