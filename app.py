import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
import seaborn as sns
from itertools import permutations

categories = [
    'Grocery', 'Electronics', 'Home & Kitchen', 'Clothing', 
    'Health & Beauty', 'Toys & Games', 'Sports & Outdoors', 'Auto & Hardware'
]

np.random.seed(42)
grid_size = 100
category_coords = {category: (np.random.randint(0, grid_size), np.random.randint(0, grid_size)) for category in categories}
category_coords['Start'] = (0, 0)

def calculate_total_distance(path, coords):
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += np.linalg.norm(np.array(coords[path[i]]) - np.array(coords[path[i+1]]))
    return total_distance

def tsp_brute_force(coords, items):
    best_path = None
    min_distance = float('inf')
    for perm in permutations(items):
        current_path = ['Start'] + list(perm) + ['Start']
        current_distance = calculate_total_distance(current_path, coords)
        if current_distance < min_distance:
            min_distance = current_distance
            best_path = current_path
    return best_path, min_distance

def calculate_expected_time(total_distance, num_selections):
    # Time for traveling
    travel_time = (total_distance / 10) * 1  # 1 minute for every 10 distance units
    # Time for selections
    selection_time = num_selections * 0.5  # 0.5 minutes (30 seconds) per selection
    return travel_time + selection_time

def animate_path(path, coords, selected_items):
    ax.clear()
    
    for category, coord in coords.items():
        ax.scatter(coord[0], coord[1], c='gray', s=100)
    
    for category in selected_items + ['Start']:
        ax.scatter(coords[category][0], coords[category][1], c='blue', s=100)
        ax.text(coords[category][0] + 0.5, coords[category][1] + 0.5, category, fontsize=12, color='red')
    
    for i in range(len(path) - 1):
        ax.plot([coords[path[i]][0], coords[path[i + 1]][0]], [coords[path[i]][1], coords[path[i + 1]][1]], 'g--', linewidth=2)
    
    ax.set_xlim(-1, grid_size)
    ax.set_ylim(-1, grid_size)
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.set_title("Shortest Path in the Mall")
    ax.grid(True)
    plt.draw()

def update(val):
    selected_items = [label for label, active in zip(categories, check.get_status()) if active]
    best_path, total_distance = tsp_brute_force(category_coords, selected_items)
    expected_time = calculate_expected_time(total_distance, len(selected_items))
    print(f"Expected Time: {expected_time:.2f} minutes")
    
    animate_path(best_path, category_coords, selected_items)

# Plot initialization
fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(left=0.3)

check = CheckButtons(plt.axes([0.05, 0.4, 0.15, 0.5]), categories, [False] * len(categories))
check.on_clicked(update)

plt.show()
