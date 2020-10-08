from Warehouse import Warehouse
from utils import distance_from


class Drone:
    def __init__(self, drone_id, capacity, weights, starting_location):
        self._capacity = capacity
        self._free_capacity = self._capacity
        self._id = drone_id
        self._weights = weights
        self._inventory = {}
        self._location = starting_location
        self._busy = 0

    def receive_order(self, turns):
        self._busy = turns

    def next_turn(self):
        if self._busy:
            self._busy -= 1

    def load(self, product_id, amount=1):
        # only add if we have capacity
        if self._free_capacity >= amount * self._weights[product_id]:
            self._inventory[product_id] = self._inventory.get(product_id, 0) + amount
            self._free_capacity -= amount * self._weights[product_id]
            return True
        else:
            raise RuntimeError(f"Overloaded drone: Capacity: {self._capacity}, "
                               f"free: {self._free_capacity}, items: {self._inventory}, "
                               f"product id: {product_id}, amount: {amount}, "
                               f"total weight: {amount * self._weights[product_id]}")

    def unload(self, product_id, amount=1):
        # only take away if we have that amount in our inventory to begin with
        if self._inventory.get(product_id, 0) > amount:
            self._inventory[product_id] -= amount
            self._free_capacity += amount * self._weights[product_id]
            return True
        elif self._inventory.get(product_id, 0) == amount:
            del self._inventory[product_id]
            self._free_capacity += amount * self._weights[product_id]
            return True
        else:
            raise RuntimeError("Tried to empty more than we have!")

    def distance_from_warehouse(self, warehouse: Warehouse):
        return distance_from(self._location, warehouse.get_location())

    def __str__(self):
        return f"{self._id}, {self._location}"
