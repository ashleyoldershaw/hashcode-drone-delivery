import json
import statistics

if __name__ == '__main__':
    with open('data.json', 'r') as f:
        data = json.loads(f.read())

    lines = [f"{c['drone_id']} L {c['warehouse_id']} {c['product_id']} {c['amount']}\n" \
             f"{c['drone_id']} D {c['order_id']} {c['product_id']} {c['amount']}" for c in data]

    with open('submission.csv', 'w') as f:
        f.write('\n'.join(lines))

    average_utilisation = statistics.mean(d['drone_capacity_used'] for d in data)
    print(average_utilisation)
    average_turns_taken = statistics.mean(d['turns_taken'] for d in data)
    average_pickup_distance = statistics.mean(d['pickup_distance'] for d in data)
    average_dropoff_distance = statistics.mean(d['dropoff_distance'] for d in data)

    print(f"Average utilisation: {average_utilisation}")
    print(f"Average duration: {average_turns_taken}")
    print(f"Average pickup distance: {average_pickup_distance}")
    print(f"Average dropoff distance: {average_dropoff_distance}")
