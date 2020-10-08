import json
from copy import deepcopy

from setup_functions import init_sim

if __name__ == '__main__':
    turn = 0
    sim = init_sim()

    with open('data.txt', 'w') as f:
        pass

    while len(sim._orders) > 0:
        if sim.find_available_drones():
            orders = deepcopy(sim._orders)
            for order in orders:
                # if order < 209:
                #     continue
                order_products = deepcopy(sim._orders[order]._items)
                for product_id in order_products:
                    sim.deliver_order(order, product_id, turn, sim._orders[order]._items[product_id])
        turn += 1
        sim.increment_turn()
    while len(sim.find_available_drones()) != len(sim._drones):
        turn += 1
        sim.increment_turn()
    print(f"Completed simulation after {turn} turns! (deadline is {sim._sim_deadline})")

    with open('data.txt', 'r') as f:
        data = [json.loads(line) for line in f.readlines()]

    with open('data.json', 'w') as f:
        f.write(json.dumps(data))
