import pytest

from Drone import Drone
from Order import Order
from Simulation import Simulation
from Warehouse import Warehouse
from utils import distance_from


def test_warehouse():
    inv = Warehouse.Inventory([0, 1, 2])
    # assert we can remove one
    assert inv.remove(1)
    # assert we can't keep going
    with pytest.raises(RuntimeError) as e:
        inv.remove(1)
    # assert order_products are deleted
    assert 1 not in inv._stock


def test_drones():
    drone = Drone(0, 10, [3, 5], (0, 0))
    # check loading
    assert drone.load(0, 3)
    assert drone._inventory[0] == 3
    assert drone._free_capacity == 1

    # check unloading
    assert drone.unload(0, 2)

    assert drone._free_capacity == 7
    assert drone._inventory[0] == 1

    # check can't empty too much
    with pytest.raises(RuntimeError) as e:
        drone.unload(0, 2)

    assert drone._free_capacity == 7
    assert drone._inventory[0] == 1

    # check emptying
    assert drone.unload(0, 1)
    assert drone._free_capacity == 10
    assert 0 not in drone._inventory
    assert drone._inventory == {}


def test_drone_distance_checking():
    drone = Drone(0, 0, [], (0, 0))

    # check the distance function works as intended (i.e. however many turns it goes)
    assert distance_from(drone._location, (3, 4)) == 5
    assert distance_from(drone._location, (1, 1)) == 2

    warehouse = Warehouse(0, 3, 4, [])
    assert drone.distance_from_warehouse(warehouse) == 5

    warehouse = Warehouse(0, 1, 1, [])
    assert drone.distance_from_warehouse(warehouse) == 2


def test_weight_calculator():
    weights = [2, 7, 11]

    info = {
        'sim_rows': 0,
        'sim_cols': 0,
        'total_drones': 0,
        'sim_deadline': 0,
        'drone_capacity': 0,
        'weights': tuple(weights)
    }

    o1 = Order(0, (0, 0), [0, 1])
    o2 = Order(1, (0, 0), [0, 0])
    o3 = Order(2, (0, 0), [1, 2])
    o4 = Order(3, (0, 0), [])

    sim = Simulation(info, [], [o1])
    assert sim.calculate_total_order_weight() == 9

    sim = Simulation(info, [], [o2])
    assert sim.calculate_total_order_weight() == 4

    sim = Simulation(info, [], [o3])
    assert sim.calculate_total_order_weight() == 18

    sim = Simulation(info, [], [o4])
    assert sim.calculate_total_order_weight() == 0

    sim = Simulation(info, [], [o1, o2, o3, o4])
    assert sim.calculate_total_order_weight() == 31


def test_drone_availability():
    info = {
        'sim_rows': 0,
        'sim_cols': 0,
        'total_drones': 5,
        'sim_deadline': 0,
        'drone_capacity': 3,
        'weights': (2, 3)
    }

    sim = Simulation(info, [Warehouse(0, 0, 0, [])], [])
    assert sim.calculate_total_available_drone_weight() == 15

    busy_drone = sim.find_available_drones()[0]
    busy_drone.receive_order(1)
    assert sim.calculate_total_available_drone_weight() == 12

    sim.find_available_drones()[0].load(0)
    assert sim.calculate_total_available_drone_weight() == 10

    busy_drone.next_turn()
    assert sim.calculate_total_available_drone_weight() == 13


def test_average_drone_calculation():
    info = {
        'sim_rows': 0,
        'sim_cols': 0,
        'total_drones': 1,
        'sim_deadline': 0,
        'drone_capacity': 3,
        'weights': (2, 3)
    }

    sim = Simulation(info, [Warehouse(0, 2, 3, [])], [])

    assert sim.calculate_average_drone_location() == (2., 3.)

    sim._drones.append(Drone(0, 0, (), (4, 4)))
    assert sim.calculate_average_drone_location() == (3., 3.5)

    sim._drones.append(Drone(0, 0, (), (4, 4)))
    assert sim.calculate_average_drone_location() == (10 / 3, 11 / 3)


def test_order_logic():
    order = Order(0, (0, 0), [0, 1, 0, 0])

    assert order.remove(1)
    assert order.remove(0, 2)
    with pytest.raises(RuntimeError) as e:
        order.remove(0, 2)

    assert order.remove(0, 1)

    assert 0 not in order._items
