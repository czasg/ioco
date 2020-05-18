from minitools.github.blog import BlogManager, GatherManager

if __name__ == '__main__':
    BlogManager(__file__).create()
    GatherManager(__file__).gather()
