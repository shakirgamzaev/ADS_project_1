# from minHeap import MinHeap
# import random
# heap = MinHeap()

# flights = [random.randint(0,10_000) for i in range(1000)]
# for i in flights:
#     heap.insert_node(MinHeap.Node(i))

# sorted_flights: list[MinHeap.Node] = []

# for i in flights:
#     sorted_flights.append(heap.remove_min())

# from maxPairingHeap import MaxPairingHeap
# import random

# pairing_heap = MaxPairingHeap()
# nodes = []

# for i in range(6, 0, -1):
#     #key = random.randint(0, 100_000)
#     new_node = MaxPairingHeap.Node(key=i, payload=None)
#     pairing_heap.push(new_node.key, payload=None)
#     nodes.append(new_node)

# pairing_heap.increase_key(nodes[2], 30)

# print("end")
# keys = []   
# while pairing_heap.node_count > 0:
#     keys.append(pairing_heap.pop().key)
    
# for i in range(0, len(keys) - 1):
#     if keys[i] < keys[i+1]:
#         print(f"key not in correct descneding order")
#         break
# print("end of program")


from maxPairingHeap import MaxPairingHeap

print("=== Testing MaxPairingHeap ===\n")

# print("Test 1: Basic push and pop")

# heap = MaxPairingHeap()

# nodes = []

# #insert values into pairing heap
# for i in range(1,11):
#     node = heap.push(key=i, payload=f"flight_{i}")
#     nodes.append(node)
#     print(f"Pushed {i}, root is now {heap.root.key}")


# print("\n Popping all elements")
# popped_values = []

# while heap.root is not None:
#     popped_node = heap.pop()
#     popped_values.append(popped_node.key)
    
# print("--- After popping all --------")
# print(f"expected: [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]")
# print(f"     got: {popped_values}")

# print("\n\nTest 2: Increase key")
# heap2 = MaxPairingHeap()
# node1 = heap2.push(key=5, payload="A")
# node2 = heap2.push(key=10, payload="B")
# node3 = heap2.push(key=3, payload="C")
# print(f"root before increase_key: {heap2.root.key}")
# heap2.increase_key(node1, 15)
# print(f"Root after increase_key(5 -> 15): {heap2.root.key}")
# print(f"✓ Pass" if heap2.root.key == 15 else "✗ Fail")

# print("-------------Test erase-----------------")
# print("\n\nTest 3: Erase")
# heap = MaxPairingHeap()
# n1 = heap.push(key=10, payload="A")
# n2 = heap.push(key=20, payload="B")
# n3 = heap.push(key=15, payload="C")
# n4 = heap.push(key=5, payload="D")

# heap.erase(n3)

# print("-------- Test 4: Large scale ---------")
# heap = MaxPairingHeap()
# import random
# values = list(range(1,100_001))
# random.shuffle(values)

# for v in values:
#     heap.push(key=v, payload=None)
# print(f"Root is: {heap.root.key}, (should be 10_000)")

# all_correct = True
# for expected in range(100_000, 0, -1):
#     node = heap.pop()
#     if node.key != expected:
#         all_correct = False
#         print(f"Error: expected {expected}, got {node.key}")
#         break

# print(f"✓ All 100,000 elements popped in correct order" if all_correct else "✗ Failed")


# flight_scheduler.submit_flight(flight_id = 401, airline_id = 10, submit_time = 0, priority = 7, duration = 4)
#     flight_scheduler.submit_flight(flight_id = 404, airline_id = 11, submit_time = 0, priority = 5, duration = 2)
#     flight_scheduler.submit_flight(flight_id = 402, airline_id = 11, submit_time = 0, priority=6, duration=3)
#     flight_scheduler.submit_flight(flight_id = 403, airline_id = 11, submit_time = 0, priority=5, duration=5)
#     flight_scheduler.reprioritize_flight(403, new_current_time=0, new_priority=10)


# flight_scheduler.initialize(count_runways = 2)
    
#     flight_scheduler.submit_flight(flight_id = 401, airline_id=11, submit_time=0, priority=8, duration=4)
    
#     flight_scheduler.submit_flight(flight_id = 402, airline_id=12, submit_time=0, priority=7, duration=5)
    
#     flight_scheduler.submit_flight(flight_id = 403, airline_id=13, submit_time=0, priority=6, duration=3)
    
#     flight_scheduler.submit_flight(flight_id = 404, airline_id=14, submit_time=0, priority=5, duration=4)
    
    
#     flight_scheduler.print_schedule(3, 9)
#     flight_scheduler.reprioritize_flight(404, 1, 10)
    
    
#     flight_scheduler.add_runways(1, 1)
    
#     flight_scheduler.submit_flight(405, 15, 2, 6, 2)
    
#     flight_scheduler.submit_flight(406, 16, 3, 7, 5)

#     flight_scheduler.ground_hold(16, 16, 3)
    
#     flight_scheduler.cancel_flight(405, 3)
    
#     flight_scheduler.tick(4)
    
#     flight_scheduler.submit_flight(407, 17, 4, 6, 3)
    
#     flight_scheduler.reprioritize_flight(407, 4, 9)
    
#     flight_scheduler.submit_flight(408, 18, 4, 8, 2)
    
#     flight_scheduler.add_runways(1, 5)
    
#     flight_scheduler.print_active()
    
    
#     flight_scheduler.tick(8)
    
#     flight_scheduler.print_schedule(6, 12)