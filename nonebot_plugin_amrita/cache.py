"""
缓存模块
Ref: https://github.com/AmritaBot/Amrita/blob/main/amrita/cache.py
"""

from __future__ import annotations

from collections import OrderedDict
from collections.abc import Hashable, Iterator
from typing import Generic, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")
T = TypeVar("T")


class LRUCache(Generic[K, V]):
    """LRU缓存实现，基于OrderedDict实现

    该缓存具有固定容量，当添加新条目导致缓存满时，
    会自动删除最久未使用的条目（Least Recently Used）。
    """

    __marker = object()

    def __init__(self, capacity: int):
        """初始化LRU缓存

        Args:
            capacity: 缓存的最大容量
        """
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer")
        self._capacity = capacity
        self._cache: OrderedDict[K, V] = OrderedDict()

    def get(self, key: K) -> V | None:
        """获取缓存中的值，如果存在则将其标记为最近使用

        Args:
            key: 要获取的键

        Returns:
            键对应的值，如果键不存在则返回None
        """
        if key not in self._cache:
            return None

        # 将访问的键移到末尾（标记为最近使用）
        value = self._cache.pop(key)
        self._cache[key] = value
        return value

    def put(self, key: K, value: V) -> None:
        """向缓存中添加或更新键值对

        如果键已存在，则更新其值并标记为最近使用。
        如果键不存在且缓存已满，则删除最久未使用的条目后再添加。

        Args:
            key: 要添加的键
            value: 要添加的值
        """
        if key in self._cache:
            # 如果键已存在，先删除它以便移到末尾
            self._cache.pop(key)
        elif len(self._cache) >= self._capacity:
            # 如果缓存已满，删除最久未使用的项（第一个）
            oldest_key = next(iter(self._cache))
            self._cache.pop(oldest_key)

        # 添加新的键值对到末尾（标记为最近使用）
        self._cache[key] = value

    def __getitem__(self, key: K) -> V:
        """支持字典风格的取值操作

        Args:
            key: 要获取的键

        Returns:
            键对应的值

        Raises:
            KeyError: 当键不存在时抛出
        """
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __setitem__(self, key: K, value: V) -> None:
        """支持字典风格的赋值操作

        Args:
            key: 要设置的键
            value: 要设置的值
        """
        self.put(key, value)

    def __delitem__(self, key: K) -> None:
        """支持删除操作

        Args:
            key: 要删除的键

        Raises:
            KeyError: 当键不存在时抛出
        """
        if key not in self._cache:
            raise KeyError(key)
        del self._cache[key]

    def __contains__(self, key: K) -> bool:
        """支持in操作符

        Args:
            key: 要检查的键

        Returns:
            如果键存在于缓存中则返回True，否则返回False
        """
        return key in self._cache

    def __len__(self) -> int:
        """返回缓存中的条目数量

        Returns:
            缓存中键值对的数量
        """
        return len(self._cache)

    def __iter__(self) -> Iterator[K]:
        """支持迭代操作，返回键的迭代器

        Returns:
            键的迭代器，按使用顺序排列（最近使用的在后）
        """
        return iter(self._cache)

    def keys(self):
        """返回键的迭代器

        Returns:
            键的迭代器
        """
        return self._cache.keys()

    def values(self):
        """返回值的迭代器

        Returns:
            值的迭代器，按使用顺序排列（最近使用的在后）
        """
        return self._cache.values()

    def items(self):
        """返回键值对的迭代器

        Returns:
            键值对的迭代器，按使用顺序排列（最近使用的在后）
        """
        return self._cache.items()

    def clear(self) -> None:
        """清空缓存"""
        self._cache.clear()

    def capacity(self) -> int:
        """获取缓存容量

        Returns:
            缓存的最大容量
        """
        return self._capacity

    def size(self) -> int:
        """获取当前缓存大小

        Returns:
            当前缓存中的条目数量
        """
        return len(self._cache)

    def is_full(self) -> bool:
        """检查缓存是否已满

        Returns:
            如果缓存已满则返回True，否则返回False
        """
        return len(self._cache) >= self._capacity

    def pop(self, key: K, default: T = __marker) -> V | T:
        """从缓存中删除指定键的条目并返回其值
        如果指定键不存在，则抛出异常

        """
        if default is self.__marker:
            return self._cache.pop(key)
        else:
            return self._cache.pop(key, default)

    def resize(self, new_size: int):
        """调整缓存大小"""
        self._capacity = new_size

    def __repr__(self) -> str:
        """返回缓存的字符串表示

        Returns:
            缓存内容的字符串表示
        """
        items = [f"{k!r}: {v!r}" for k, v in self._cache.items()]
        return f"{self.__class__.__name__}(capacity={self._capacity}, items={{{', '.join(items)}}})"
