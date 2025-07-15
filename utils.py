# Utility Functions for use in nba_re-scoring.ipynb
import polars as pl
import pyarrow as pa
import pyarrow.parquet as pq
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Draw Basketball Court
def draw_court(ax=None, color='black', lw=1):
    if ax is None:
        ax = plt.gca()
        ax.set_aspect('equal')

    # Hoop (inner diameter 18in)
    hoop_center_y = 5.25
    hoop = patches.Circle((0, hoop_center_y), radius=9/12, linewidth=lw, color=color, fill=False)

    # Three-point line (22ft away, 14up, then 23.75 radius around hoop)
    corner_three_a = patches.Rectangle((-22, 0), 0, 14, linewidth=lw, color=color)
    corner_three_b = patches.Rectangle((22, 0), 0, 14, linewidth=lw, color=color)
    three_arc = patches.Arc((0, hoop_center_y), 47.5, 47.5, theta1=22, theta2=158, linewidth=lw, color=color)

    # Center court (Circles 94/2 ft up, 6ft and 2ft radius)
    center_outer = patches.Circle((0, 94/2), radius=6, linewidth=lw, color=color, fill=False)
    center_inner = patches.Circle((0, 94/2), radius=2, linewidth=lw, color=color, fill=False)
    halfcourt = patches.Rectangle((-25, 94/2), 50, 0, linewidth=lw, color=color, fill=False)
    
    # Opposite 3pt line
    opp_corner_three_a = patches.Rectangle((-22, 0), 0, 14, linewidth=lw, color=color, angle=180, rotation_point=(0,94/2))
    opp_corner_three_b = patches.Rectangle((22, 0), 0, 14, linewidth=lw, color=color, angle=180, rotation_point=(0,94/2))
    opp_three_arc = patches.Arc((0, 94-hoop_center_y), 47.5, 47.5, theta2=360-22, theta1=360-158, linewidth=lw, color=color)

    # Boundary (94ft by 50ft)
    boundary = patches.Rectangle((-25, 0), 50, 94, linewidth=lw, color=color, fill=False)

    court_elements = [hoop, corner_three_a, corner_three_b, three_arc, halfcourt, boundary, opp_corner_three_a, opp_corner_three_b, opp_three_arc]
    for element in court_elements:
        ax.add_patch(element)

    return ax

# Plots made and missed shots density
def made_missed_shots_density(df):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 8))
    ax1.set_aspect('equal')
    made_df = df.filter(df["SHOT_MADE"] == True)
    hb1 = ax1.hexbin(
        made_df["LOC_X"].to_numpy(), made_df["LOC_Y"].to_numpy(),
        gridsize=50, cmap='Greens', bins='log'
    )
    draw_court(ax1)
    ax1.set_xlim(-27, 27)
    ax1.set_ylim(-2, 96)
    ax1.set_title("Shots Made")
    ax1.axis('off')
    ax2.set_aspect('equal')
    miss_df = df.filter(df["SHOT_MADE"] == False)
    hb2 = ax2.hexbin(
        miss_df["LOC_X"].to_numpy(), miss_df["LOC_Y"].to_numpy(),
        gridsize=50, cmap='Reds', bins='log'
    )
    draw_court(ax2)
    ax2.set_xlim(-27, 27)
    ax2.set_ylim(-2, 96)
    ax2.set_title("Shots Missed")
    ax2.axis('off')
    plt.tight_layout()
    plt.show()
    
# Function to calculate number of shots based on inclusive distance range from df
def calculate_num_shots(df, d1, d2):
    filtered_shots = df.filter((df["SHOT_DISTANCE"] >= d1) & (df["SHOT_DISTANCE"] <= d2))
    total_shots = len(filtered_shots)
    return total_shots
    
# Function to calculate shot probability based on inclusive distance range from df
def calculate_shot_probability(df, d1, d2):
    filtered_shots = df.filter((df["SHOT_DISTANCE"] >= d1) & (df["SHOT_DISTANCE"] <= d2))
    total_shots = len(filtered_shots)
    made_shots = len(filtered_shots.filter(filtered_shots["SHOT_MADE"] == True))
    if total_shots == 0:
        return 0.0
    return made_shots / total_shots

# Histogram of number of shots by distance
def plot_shots_by_distance(df):
    shot_distances = df["SHOT_DISTANCE"].to_numpy()
    plt.figure(figsize=(10, 6))
    plt.hist(shot_distances, bins=94, color='blue', range=(0, 94), log=True)
    plt.axvline(x=22, color='red', linestyle='--', linewidth=2, label='3PT Corner (22 ft)')
    plt.axvline(x=23.75, color='orange', linestyle='--', linewidth=2, label='3PT Arc (23.75 ft)')
    plt.title("Shots by Distance")
    plt.xlabel("Shot Distance (ft)")
    plt.ylabel("Number of Shots")
    plt.xlim(0,94)
    plt.grid(axis='y', alpha=0.75)
    plt.legend()
    plt.show()

# Histogram of shot probability by distance
def plot_shot_prob_by_distance(df):
    shot_distances = df["SHOT_DISTANCE"].to_numpy()
    unique_distances = np.unique(shot_distances)
    probabilities = [calculate_shot_probability(df, d, d) for d in unique_distances]
    plt.figure(figsize=(10, 6))
    plt.bar(unique_distances, probabilities, width=1, color='blue')
    plt.axvline(x=22, color='red', linestyle='--', linewidth=2, label='3PT Corner (22 ft)')
    plt.axvline(x=23.75, color='orange', linestyle='--', linewidth=2, label='3PT Arc (23.75 ft)')
    plt.title("Shot Probability by Distance")
    plt.xlabel("Shot Distance (ft)")
    plt.ylabel("Shot Probability")
    plt.xlim(0,94)
    plt.grid(axis='y', alpha=0.75)
    plt.legend()
    plt.show()

# Plot Shot Expected Value by Distance
def plot_shot_EV_by_distance(df):
    shot_distances = df["SHOT_DISTANCE"].to_numpy()
    unique_distances = np.unique(shot_distances)
    probabilities = [calculate_shot_probability(df, d, d) for d in unique_distances]
    EVs = [p * (3 if d >= 23 else 2) for d, p in zip(unique_distances, probabilities)]
    plt.figure(figsize=(10, 6))
    plt.bar(unique_distances, EVs, width=1, color='blue')
    plt.axvline(x=22, color='red', linestyle='--', linewidth=2, label='3PT Corner (22 ft)')
    plt.axvline(x=23.75, color='orange', linestyle='--', linewidth=2, label='3PT Arc (23.75 ft)')
    plt.title("Shot Expected Value by Distance")
    plt.xlabel("Shot Distance (ft)")
    plt.ylabel("Shot EV")
    plt.xlim(0,94)
    plt.grid(axis='y', alpha=0.75)
    plt.legend()
    plt.show()

# Returns deserved points for given shot length given a target EV
def get_deserved_points(df, d1, d2, target_EV, print_bool=False):
    num_shots = calculate_num_shots(df, d1, d2)
    if print_bool: print(f"Number of shots from {d1} to {d2}ft: {num_shots}")
    shot_prob = calculate_shot_probability(df, d1, d2)
    if print_bool: print(f"Probability from {d1} to {d2}ft: {shot_prob*100:.4f}%")
    if shot_prob > 0:
        deserved_points = target_EV / shot_prob
        print(f"Deserved points for Target EV of {target_EV}: {deserved_points}")
        return deserved_points
    else:
        print("Divide by 0 Error, Worth Infinite Points, Returning -1")
        return -1