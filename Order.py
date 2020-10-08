from collections import Counter


class Order:
    def __init__(self, order_id, location, items):
        self._id = int(order_id)
        self._location = (int(location[1]), int(location[0]))
        self._items = dict(Counter(int(i) for i in items))

    def __str__(self):
        return f"{self._id}, {self._location}, {self._items}"

    def remove(self,product_id, amount = 1):
        if amount > self._items[product_id]:
            raise RuntimeError("Trying to deliver too much!")

        self._items[product_id] -= amount

        if self._items[product_id] == 0:
            del self._items[product_id]

        return True

    def is_empty(self):
        return len(self._items) == 0
