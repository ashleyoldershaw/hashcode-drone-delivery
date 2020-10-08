import csv

from Order import Order
from Simulation import Simulation
from Warehouse import Warehouse


def get_sim_info(info):
    return {
        'sim_rows': int(info[0][0]),
        'sim_cols': int(info[0][1]),
        'total_drones': int(info[0][2]),
        'sim_deadline': int(info[0][3]),
        'drone_capacity': int(info[0][4]),
        'num_products': int(info[1][0]),
        'num_warehouses': int(info[3][0]),
        'weights': tuple(int(info[2][i]) for i in range(len(info[2])))
    }


def get_warehouse_order_info(file_info, sim_info):
    warehouses = []

    row_count = 4
    for warehouse_id in range(sim_info['num_warehouses']):
        warehouses.append(
            Warehouse(warehouse_id, file_info[row_count][1], file_info[row_count][0], file_info[row_count + 1]))
        row_count += 2

    num_orders = int(file_info[row_count][0])
    row_count += 1

    orders = []

    for order_id in range(num_orders):
        orders.append(Order(order_id, file_info[row_count], file_info[row_count + 2]))
        row_count += 3

    return warehouses, orders


def init_sim():
    with open('busy_day.in') as f:
        reader = csv.reader(f, delimiter=" ")
        file_info = [row for row in reader]

    info = get_sim_info(file_info)

    w, o = get_warehouse_order_info(file_info, info)

    return Simulation(info, w, o)
