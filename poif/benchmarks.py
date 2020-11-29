import time
import random
from pathlib import Path

current_file = Path(__file__)

runs = 500

item_list = list(range(100000))
random.shuffle(item_list)
item_set = set(item_list)

items_to_search = list(range(10))

start_time_list = time.time()
for _ in range(runs):
    for item in items_to_search:
        if item in item_list:
            pass
stop_time_list = time.time()

start_time_set = time.time()
for _ in range(runs):
    for item in items_to_search:
        if item in item_set:
            pass
stop_time_set = time.time()

start_time_disk = time.time()
for _ in range(runs):
    if current_file.exists():
        pass
stop_time_disk = time.time()

list_time = stop_time_list - start_time_list
set_time = stop_time_set - start_time_set
disk_time = stop_time_disk - start_time_disk
print(f'Time for list: {list_time}s')
print(f'Time for set: {set_time}s')
print(f'Time for disk: {disk_time}s')
print(set_time / disk_time)