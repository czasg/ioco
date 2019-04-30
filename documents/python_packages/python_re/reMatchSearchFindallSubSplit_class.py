"""
正则的5种基本使用
match
search
findall
sub
split
"""

class Re:
    def __init__(self, reRule, content=None, flag=0):
        import re
        self.compile = re.compile(reRule, flags=flag)
        self.content = content

    def match(self, content=None):
        con = content if content else self.content
        return self.compile.match(con)

    def search(self, content=None):
        con = content if content else self.content
        return self.compile.search(con)

    def findall(self, content=None):
        con = content if content else self.content
        return self.compile.findall(con)

    def sub(self, repl, content=None):
        con = content if content else self.content
        return self.compile.sub(repl, con)

    def split(self, content=None):
        con = content if content else self.content
        return self.compile.split(con)

test_string = "this; is. a, test? string"

if __name__ == "__main__":
    """match，匹配开头一次"""
    print(Re('(.*?)\s', test_string).match().group(1))
    """search， 匹配符合的str一次"""
    print(Re('(\S{4})', test_string).search().group(1))
    """findall，匹配所有符合的规则，但是每次匹配不管你是否需要，匹配完后都会‘去除’，不要二次使用"""
    print(Re('(\S{4})', test_string).findall())
    """sub，替换所有符合规则的str"""
    print(Re('(\S{4})', test_string).sub('TEST'))
    """split，切割所有符合规则的符号"""
    print(Re('(;|\.|,)', test_string).split())
