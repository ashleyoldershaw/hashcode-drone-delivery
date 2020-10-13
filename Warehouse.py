class Warehouse:
    class Inventory:
        def __init__(self, stock):
            self._stock = {i: int(stock[i]) for i in range(len(stock)) if int(stock[i])}

        def __str__(self):
            return str(self._stock)

        def add(self, item_id, amount=1):
            self._stock[item_id] = self._stock.get(item_id, 0) + amount
            return True

        def remove(self, item_id, amount=1):
            if item_id not in self._stock or self._stock[item_id] < amount:
                 raise RuntimeError("Trying to take more than we have from a warehouse!")

            self._stock[item_id] = self._stock[item_id] - amount
            if self._stock[item_id] == 0:
                del self._stock[item_id]
            return True

    def __init__(self, warehouse_id, location_x, location_y, stock):
        self._inventory = self.Inventory(stock)
        self._column = int(location_x)
        self._row = int(location_y)
        self._id = int(warehouse_id)

    def __str__(self):
        return f"{self._id}, {self.get_location()}, {self._inventory}"

    def get_location(self):
        return self._column, self._row
