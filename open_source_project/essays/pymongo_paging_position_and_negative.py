from pymongo import MongoClient


class PagerManager:
    def __init__(self, item_count, page_index=1, page_size=6):
        self.item_count = item_count
        self.page_size = page_size
        self.page_count = item_count // page_size + (1 if item_count % page_size > 0 else 0)
        self.page_index = page_index
        if (item_count == 0) or (page_index > self.page_count):
            self.is_last = self.is_first = True
            self.is_pre_half = True
            self.offset = self.residue = 0
        else:
            self.is_last = (self.page_index == self.page_count)
            self.is_first = (self.page_index == 1)
            self.is_pre_half = (self.page_index <= (self.page_count // 2))
            self.offset = self.page_size * (page_index - 1)
            self.residue = (self.item_count - self.offset - (0 if self.is_last else self.page_size))


class Mongodb:
    def __init__(self):
        self.collection = MongoClient()['db_name']['collection_name']

    def count(self):
        return self.collection.count()

    def find_page(self, pager, query=None):
        if pager.is_pre_half:
            result = list(self.collection.find(query).skip(pager.offset).limit(pager.page_size))
        else:
            result = list(self.collection.find(query) \
                          .sort([('_id', -1)]).skip(0 if pager.is_last else pager.residue) \
                          .limit(min(pager.page_size, pager.residue if pager.is_last else pager.page_size)))[::-1]
        return result


if __name__ == '__main__':
    page_query = 1
    page_size = 10

    mongodb_handler = Mongodb()
    all_count = mongodb_handler.count()
    pager = PagerManager(all_count, page_query, page_size)

    result = mongodb_handler.find_page(pager)
