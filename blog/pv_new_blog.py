import os
from minitools import (
    get_current_path, to_path, make_dir, timekiller, make_file, find_file_by_name,
    valid_list, load_json, save_json
)
from itertools import count
from datetime import datetime
from collections import defaultdict

create_time = lambda file: datetime.fromtimestamp(os.path.getctime(file))
amend_time = lambda file: datetime.fromtimestamp(os.path.getmtime(file))


class Path:

    def __init__(self, path=None):
        self.cur_path = get_current_path(path or __file__)
        self.today = timekiller.split()[:3]
        self.path = to_path(self.cur_path, *self.today, forceStr=True)
        self.blog_path = ''

    def create_dir(self, path=None):
        make_dir(path or self.path)

    def create_file(self, path, content=''):
        make_file(path, content)


class Blog:
    default_content = """
<!--
./static/img/dd.jpg
未定义
default title
default abstract
default blog content, please don't use some markdown grammar in first paragraph.
-->

## default title

> default abstract

default blog content, please don't use some
markdown grammar in first paragraph.

you also don't want to show this in web-html.
    """

    def __init__(self):
        self.prefix = "pv_blog"
        self.suffix = ".md"
        self.blogs = []
        self.blog_name = ''

    def init_blog(self):
        self.blog_name = to_path(self.prefix, '_', len(self.blogs) + 1, self.suffix, sep='', forceStr=True)


class BlogManager:
    def __init__(self, path=None):
        self.pather = Path(path)
        self.bloger = Blog()

    def search_blog(self, path=None):
        self.bloger.blogs = find_file_by_name(self.bloger.prefix, path=(path or self.pather.path), matching='startswith')

    def init_blog(self):
        self.pather.create_dir()
        self.search_blog()
        self.bloger.init_blog()
        self.pather.blog_path = to_path(self.pather.path, self.bloger.blog_name)

    def create(self):
        self.init_blog()
        self.pather.create_file(self.pather.blog_path, self.bloger.default_content.strip())


class GatherManager:
    def __init__(self):
        self.handler = BlogManager()
        self.gather_blog_dir = "blog"
        self.gather_label_dir = "label"
        self.settings = "settings.json"
        self.limit = 6
        self.labels = defaultdict(list)
        self.author = "CzaOrz"
        self.__init()
        self.init_settings()

    def __init(self):
        self.count = count().__next__
        self.blogs = []
        self.blog_total = 0
        self.blog_id = 1

    def init_settings(self):
        self.settings = to_path(self.handler.pather.cur_path, self.settings)
        if not os.path.exists(self.settings):
            self.handler.pather.create_file(
                self.settings,
                '{"blog_url": "./blog/blog1.json", "blog_total": 0, "blog_total_page": 0, "blog_last_url": "", "labels": []}')
        self.handler.pather.create_dir(to_path(self.handler.pather.cur_path, self.gather_blog_dir))
        self.handler.pather.create_dir(to_path(self.handler.pather.cur_path, self.gather_label_dir))

    def search_blog(self):
        self.handler.search_blog('.')
        self.blogs = self.handler.bloger.blogs[:]
        self.blog_total = len(self.blogs)

    def json_file(self, file_id=None, label=None):
        if label:
            return f"./{self.gather_label_dir}/{label}/label{file_id or self.blog_id}.json"
        return f"./{self.gather_blog_dir}/blog{file_id or self.blog_id}.json"

    def gather(self, label=None):
        if len(self.blogs) > self.limit:
            self.blogs, blogs = self.blogs[:-self.limit], self.blogs[-self.limit:]
            self._gather(blogs, self.json_file(self.blog_id + 1), label=label)
            self.gather(label)
        else:
            self._gather(label=label)

    def _gather(self, blogs=None, next_url="", label=None):
        results = []
        result = []
        row = 1
        for blog in (blogs or self.blogs)[::-1]:
            if not label:
                blog_info = valid_list(blog.strip(".").split(os.sep))
                template = {
                    "blog_id": self.count(),
                    "blog_img": "",
                    "blog_title": "",
                    "blog_abstract": "",
                    "blog_author": self.author,
                    "blog_created": timekiller.datetimeStr(create_time(blog)),
                    "blog_amend": timekiller.datetimeStr(amend_time(blog)),
                    "blog_content": "",
                    "blog_url": f"./{to_path(*blog_info, sep='/')}".replace(".md", ""),
                }
                with open(blog, 'r', encoding='utf-8') as f:
                    text = f.readline()
                    if text.startswith("<!--"):
                        template['blog_img'] = f.readline().strip()
                        template['labels'] = f.readline().strip().split('|')
                        template['blog_title'] = f.readline().strip()
                        template['blog_abstract'] = f.readline().strip()
                        template['blog_content'] = f.readline().strip()
                        result.append(template)
                        for _label in template['labels']:
                            self.labels[_label].append(template)
                    else:
                        raise Exception('Invalid blog-content, it should startswith <!--xxx-->')
            else:
                result.append(blog)
            if row % 3 == 0:
                results.append(result)
                result = []
            row += 1
        if result:
            results.append(result)
        save_json(self.json_file(label=label), {
            "blogs": results,
            "next_url": next_url
        })
        self.blog_id += 1

    def save_settings(self):
        settings = load_json(self.settings)
        settings['blog_total'] = self.blog_total
        settings['blog_total_page'] = self.blog_id - 1
        settings['blog_last_url'] = self.json_file()
        settings['labels'] = []
        for name, templates in self.labels.items():
            settings['labels'].append({
                'name': name,
                'url': f'./{self.gather_label_dir}/{name}/label1.json',
                'total': len(templates),
                'total_page': len(templates) // 6 + 1,
            })
            self.handler.pather.create_dir(to_path(self.gather_label_dir, name))
            self.__init()
            self.blogs[:] = templates
            self.gather(name)
        save_json(self.settings, settings)


    def run(self):
        self.search_blog()
        self.gather()
        self.save_settings()


if __name__ == '__main__':
    # BlogManager().create()

    GatherManager().run()
