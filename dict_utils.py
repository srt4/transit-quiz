__author__ = 'Kun Xi'

import collections


class LRUCache:
    """
    Implementation taken from http://www.kunxi.org/blog/2014/05/lru-cache-in-python/
    """

    def __init__(self, capacity):
        self.__capacity = capacity
        self.__cache = collections.OrderedDict()

    def get(self, key):
        value = self.__cache.pop(key)
        self.__cache[key] = value
        return value

    def set(self, key, value):
        try:
            self.__cache.pop(key)
        except KeyError:
            if len(self.__cache) >= self.__capacity:
                self.__cache.popitem(last=False)
        self.__cache[key] = value

    def contains_key(self, key):
        return self.__cache.has_key(key)