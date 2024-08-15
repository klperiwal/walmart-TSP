import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
import seaborn as sns

from itertools import permutations

# Categories and Grid Initialization
categories = [
    'Grocery', 'Electronics', 'Home & Kitchen', 'Clothing', 
    'Health & Beauty', 'Toys & Games', 'Sports & Outdoors', 'Auto & Hardware'
]

np.random.seed(42)
grid_size = 10
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

def animate_path(path, coords, selected_items):
    ax.clear()
    
    # Draw all points with default color
    for category, coord in coords.items():
        ax.scatter(coord[0], coord[1], c='gray', s=100)
    
    # Highlight selected items and start point
    for category in selected_items + ['Start']:
        ax.scatter(coords[category][0], coords[category][1], c='blue', s=100)
        ax.text(coords[category][0] + 0.2, coords[category][1] + 0.2, category, fontsize=12, color='red')
    
    # Draw the route between selected items
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
    best_path, _ = tsp_brute_force(category_coords, selected_items)
    animate_path(best_path, category_coords, selected_items)

# Plot initialization
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.3)

# Checkbuttons widget
check = CheckButtons(plt.axes([0.05, 0.4, 0.15, 0.5]), categories, [False] * len(categories))
check.on_clicked(update)

# Show the plot
plt.show()
