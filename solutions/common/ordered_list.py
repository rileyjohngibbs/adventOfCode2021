from typing import Callable, Generic, Iterable, TypeVar

import pytest


T = TypeVar("T")


class OrderedList(Generic[T]):
    def __init__(self, items: Iterable[T], key: Callable[[T], int]) -> None:
        self.key = key
        self._list = sorted(list(items), key=self.key)

    def __getitem__(self, index: int) -> T:
        return self._list.__getitem__(index)

    def __iter__(self) -> Iterable[T]:
        return self._list.__iter__()

    def __len__(self) -> int:
        return self._list.__len__()

    def insert(self, item: T) -> None:
        index = self.find_index(item)
        self._list.insert(index, item)

    def find_index(self, item: T) -> int:
        left, right = 0, len(self._list)
        item_value = self.key(item)
        while right > left:
            test = (right + left) // 2
            if self.key(self._list[test]) > item_value:
                right = test
            elif self.key(self._list[test]) < item_value:
                left = test + 1
            else:
                left, right = test, test
        return left

    def pop(self, index: int) -> T:
        return self._list.pop(index)


@pytest.mark.parametrize(
    "item, index",
    [(0, 0), (2, 1), (4, 2), (6, 3), (8, 4)],
)
def test_find_index(item, index):
    ol = OrderedList([1, 3, 5, 7], lambda x: x)
    assert ol.find_index(item) == index


@pytest.mark.parametrize(
    "item",
    [0, 2, 4, 6, 8],
)
def test_insertion(item):
    ol = OrderedList([1, 3, 5, 7], lambda x: x)
    ol.insert(item)
    assert len(ol) == 5
    assert all(a < b for a, b in zip(ol[:-1], ol[1:]))
