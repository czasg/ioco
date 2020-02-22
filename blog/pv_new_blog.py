import os
from minitools import (
    get_current_path, to_path, make_dir, timekiller, make_file, find_file_by_name,
    valid_list, load_json, save_json
)
from itertools import count


class Path:

    def __init__(self):
        self.cur_path = get_current_path(__file__)
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
    def __init__(self):
        self.pather = Path()
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
        self.gather_dir = "blog"
        self.settings = "settings.json"
        self.__init()
        self.init_settings()

    def __init(self):
        self.count = count().__next__
        self.limit = 6
        self.blogs = []
        self.blog_id = 1
        self.author = "CzaOrz"

    def init_settings(self):
        self.settings = to_path(self.handler.pather.cur_path, self.settings)
        if not os.path.exists(self.settings):
            self.handler.pather.create_file(self.settings, '{"blog_url": "", "blog_total": 0}')
        self.handler.pather.create_dir(to_path(self.handler.pather.cur_path, self.gather_dir))

    def search_blog(self):
        self.handler.search_blog('.')
        self.blogs = self.handler.bloger.blogs[:]
        settings = load_json(self.settings)
        settings['blog_total'] = len(self.blogs)
        save_json(self.settings, settings)

    def json_file(self, file_id=None):
        return f"./{self.gather_dir}/blog{file_id or self.blog_id}.json"

    def gather(self):
        if len(self.blogs) > self.limit:
            self.blogs, blogs = self.blogs[:-self.limit], self.blogs[-self.limit:]
            self._gather(blogs, self.json_file(self.blog_id + 1))
            self.gather()
        else:
            self._gather()

    def _gather(self, blogs=None, next_url=""):
        results = []
        result = []
        row = 1
        for blog in (blogs or self.blogs)[::-1]:
            blog_info = valid_list(blog.strip(".").split(os.sep))
            template = {
                "blog_id": self.count(),
                "blog_img": "",
                "blog_title": "",
                "blog_abstract": "",
                "blog_author": self.author,
                "blog_created": to_path(*blog_info[:3], sep="-"),
                "blog_content": "",
                "blog_url": f"./{to_path(*blog_info, sep='/')}".replace(".md", ""),
            }
            with open(blog, 'r', encoding='utf-8') as f:
                text = f.readline()
                if text.startswith("<!--"):
                    template['blog_img'] = f.readline().strip()
                    template['blog_title'] = f.readline().strip()
                    template['blog_abstract'] = f.readline().strip()
                    template['blog_content'] = f.readline().strip()
                    result.append(template)
                else:
                    raise Exception('Invalid blog-content, it should startswith <!--xxx-->')
            if row % 3 == 0:
                results.append(result)
                result = []
            row += 1
        if result:
            results.append(result)
        save_json(self.json_file(), {
            "blogs": results,
            "next_url": next_url
        })
        self.blog_id += 1

    def run(self):
        self.search_blog()
        self.gather()


if __name__ == '__main__':
    # BlogManager().create()

    GatherManager().run()
