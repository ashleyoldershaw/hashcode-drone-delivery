import json
import math

from Drone import Drone
from Order import Order
from Warehouse import Warehouse
from utils import distance_from


class Simulation:
    def __init__(self, sim_info, warehouses: [Warehouse], orders: [Order]):
        self._sim_rows = sim_info['sim_rows']
        self._sim_cols = sim_info['sim_cols']
        self._total_drones = sim_info['total_drones']
        self._sim_deadline = sim_info['sim_deadline']
        self._drone_capacity = sim_info['drone_capacity']
        self._product_weights = sim_info['weights']
        self._warehouses = warehouses
        self._orders = {i: orders[i] for i in range(len(orders))}

        self._drones = [Drone(i, self._drone_capacity, self._product_weights, self._warehouses[0].get_location()) for i
                        in range(self._total_drones)]

    @property
    def __str__(self):
        # initialise the map
        sim_map = []
        for i in range(self._sim_rows):
            sim_map.append([])
            for _ in range(self._sim_cols):
                sim_map[i].append(' ')

        # write over the initialised map with orders and then warehouses
        for order in self._orders:
            loc = order._location
            try:
                sim_map[loc[1]][loc[0]] = 'O'
            except IndexError:
                print(loc)

        for warehouse in self._warehouses:
            loc = warehouse._column, warehouse._row
            sim_map[loc[1]][loc[0]] = 'W'

        lines = ["".join(row) for row in sim_map]
        return "\n".join(lines)

    def closest_drone(self, warehouse_id):
        warehouse_location = (self._warehouses[warehouse_id]._column, self._warehouses[warehouse_id]._row)
        if self.find_available_drones():
            return min(self.find_available_drones(), key=lambda x: distance_from(x._location, warehouse_location))
        else:
            return False

    def calculate_total_order_weight(self):
        total = 0
        for order in self._orders:
            for item in self._orders[order]._items:
                total += self._orders[order]._items[item] * self._product_weights[item]
        return total

    def calculate_total_available_drone_weight(self):
        return sum(drone._free_capacity for drone in self.find_available_drones())

    def estimate_completion(self):
        number_of_orders = len(self._orders)
        total_order_weight = self.calculate_total_order_weight()

        return number_of_orders + total_order_weight

    def find_available_drones(self):
        return [d for d in self._drones if d._busy == 0]

    def calculate_average_drone_location(self):
        average_x = sum(float(d._location[0]) for d in self._drones) / len(self._drones)
        average_y = sum(float(d._location[1]) for d in self._drones) / len(self._drones)
        return average_x, average_y

    def calculate_closest_warehouse_satisfying_order(self, order_number, product_id, amount):
        eligible_warehouses = [w for w in self._warehouses if w._inventory._stock.get(product_id, 0) >= amount]

        if not eligible_warehouses:
            raise RuntimeWarning(
                f"No warehouse contains enough of product {product_id} to satisfy order {order_number}")

        return min(
            eligible_warehouses,
            key=lambda w: distance_from(
                (w._column, w._row), self._orders[order_number]._location
            ),
        )

    def deliver_order(self, order_number, product_id, turn, amount=1):
        remaining_order_weight = self._product_weights[product_id] * amount
        pickup_turns = 1
        dropoff_turns = 1

        while remaining_order_weight:
            if remaining_order_weight > self._drone_capacity:
                amount_to_pick = math.floor(self._drone_capacity / self._product_weights[product_id])
                remaining_order_weight -= amount_to_pick * self._product_weights[product_id]
                amount -= amount_to_pick

            else:
                amount_to_pick = amount
                remaining_order_weight = 0

            warehouse = self.calculate_closest_warehouse_satisfying_order(order_number, product_id, amount_to_pick)
            drone = self.closest_drone(warehouse._id)
            if drone:
                # print(f"Drone {drone._id} -> warehouse {warehouse._id} for {amount_to_pick} of product {product_id}")
                pickup_distance = distance_from(drone._location, warehouse.get_location())
                dropoff_location = self._orders[order_number]._location
                dropoff_distance = distance_from(warehouse.get_location(), dropoff_location)
                total = pickup_distance + dropoff_distance
                total_turns = total + pickup_turns + dropoff_turns

                drone.receive_order(total_turns)
                drone._location = self._orders[order_number]._location

                drone.load(product_id, amount_to_pick)
                warehouse._inventory.remove(product_id, amount_to_pick)
                drone.unload(product_id, amount_to_pick)
                self._orders[order_number].remove(product_id, amount_to_pick)

                if self._orders[order_number].is_empty():
                    print(f"Completed order {order_number}! (Turn {turn}, {len(self._orders)} orders to go)")
                    del self._orders[order_number]

                drone_capacity_used = float(amount_to_pick * self._product_weights[product_id]) / self._drone_capacity

                movement_info = {'intial_location': drone._location, 'warehouse_location': warehouse.get_location(),
                                 'dropoff_location': dropoff_location, 'pickup_distance': pickup_distance,
                                 'dropoff_distance': dropoff_distance, 'turns_taken': total_turns,
                                 'drone_capacity_used': drone_capacity_used, 'turn': turn, 'drone_id': drone._id,
                                 'warehouse_id': warehouse._id, 'order_id': order_number, 'product_id': product_id,
                                 'amount': amount_to_pick}

                with open("data.txt", 'a+') as f:
                    f.write(f"{json.dumps(movement_info)}\n")
            else:
                break

    def increment_turn(self):
        for drone in self._drones:
            drone.next_turn()
