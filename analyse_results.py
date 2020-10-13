import json
import statistics


def get_data():
    with open('data.json', 'r') as f:
        return json.loads(f.read())


def generate_output_file(input_data):
    lines = [f"{c['drone_id']} L {c['warehouse_id']} {c['product_id']} {c['amount']}\n" \
             f"{c['drone_id']} D {c['order_id']} {c['product_id']} {c['amount']}" for c in input_data]

    with open('submission.csv', 'w') as f:
        f.write('\n'.join(lines))


def print_initial(input_data):
    average_utilisation = statistics.mean(d['drone_capacity_used'] for d in input_data)
    print(average_utilisation)
    average_turns_taken = statistics.mean(d['turns_taken'] for d in input_data)
    average_pickup_distance = statistics.mean(d['pickup_distance'] for d in input_data)
    average_dropoff_distance = statistics.mean(d['dropoff_distance'] for d in input_data)

    print(f"Average utilisation: {average_utilisation}")
    print(f"Average duration: {average_turns_taken}")
    print(f"Average pickup distance: {average_pickup_distance}")
    print(f"Average dropoff distance: {average_dropoff_distance}")


def generate_tableau_input(input_data):
    tableau = []
    for movement in data:
        new_movement = movement
        new_movement['drone_x'] = movement['intial_location'][0]
        new_movement['drone_y'] = movement['intial_location'][1]
        new_movement['warehouse_x'] = movement['warehouse_location'][0]
        new_movement['warehouse_y'] = movement['warehouse_location'][1]
        new_movement['dropoff_x'] = movement['dropoff_location'][0]
        new_movement['dropoff_y'] = movement['dropoff_location'][1]

        del new_movement['intial_location']
        del new_movement['warehouse_location']
        del new_movement['dropoff_location']

        tableau.append(new_movement)

    print(tableau)
    with open('tableau.json', 'w') as f:
        f.write(json.dumps(tableau))
    return


if __name__ == '__main__':
    data = get_data()

    # generate_output_file(data)
    # print_initial(data)

    generate_tableau_input(data)
