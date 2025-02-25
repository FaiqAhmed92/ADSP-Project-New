import json
import os
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from acoustics import RoomAcoustics 

# ===================== RT60 CALCULATION =====================
def compute_room_volume(room_dims):
    """Calculate room volume (length × width × height)."""
    length, width, height = room_dims
    return length * width * height

def compute_surface_areas(room_dims):
    """Calculate surface areas of the 6 sides of a rectangular room."""
    length, width, height = room_dims
    return [length * width, length * width,  # Floor & Ceiling
            length * height, length * height,  # Front & Back Walls
            width * height, width * height]  # Left & Right Walls

def calculate_rt60(room_dims, abs_coeff):
    """
    Compute RT60 for each frequency band using Sabine’s formula.
    abs_coeff should be a dictionary with absorption coefficients for 'low', 'mid', and 'high' frequencies.
    """
    volume = compute_room_volume(room_dims)
    surface_areas = compute_surface_areas(room_dims)

    rt60_results = {}
    for band, coeffs in abs_coeff.items():
        total_absorption = sum(area * alpha for area, alpha in zip(surface_areas, coeffs))
        rt60_results[band] = 0.161 * (volume / total_absorption) if total_absorption > 0 else 0
    return rt60_results

# ===================== ROOM & ACOUSTICS SIMULATION =====================
def load_room_specs(file_path):
    """Load room specifications from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def simulate_acoustics(acoustics_simulator):
    """Simulate impulse responses for different frequency bands."""
    return acoustics_simulator.image_source_method(enhanced=True)

def plot_responses_and_rt60(responses, rt60_values, title):
    """Plot impulse responses (2D), RT60 values, and Decay Curves."""
    
    # ✅ IMPULSE RESPONSE PLOT
    fig, ax1 = plt.subplots(figsize=(10, 5))
    for freq_band, response in responses.items():
        ax1.plot(response[0], label=f'{freq_band.capitalize()} Frequency')

    ax1.set_xlabel("Time (samples)")
    ax1.set_ylabel("Amplitude")
    ax1.set_title(f"Impulse Response - {title}")
    ax1.legend()
    ax1.grid(True)
    plt.show()

    # ✅ RT60 VALUES PLOT (with consistent labeling)
    fig, ax2 = plt.subplots(figsize=(6, 4))
    bands = ['Low', 'Mid', 'High']  # Clear labels
    values = [rt60_values['low'], rt60_values['mid'], rt60_values['high']]
    ax2.bar(bands, values, color=['red', 'green', 'blue'])
    ax2.set_title(f"RT60 (Reverberation Time) - {title}")
    ax2.set_ylabel("RT60 (seconds)")
    plt.show()

    # ✅ ENERGY DECAY PLOT (time samples clearly visible)
    fig, ax3 = plt.subplots(figsize=(10, 5))
    for freq_band, response in responses.items():
        energy = np.cumsum(response[0]**2)[::-1]  # Reverse cumulative sum for decay
        energy_db = 10 * np.log10(energy / np.max(energy))
        ax3.plot(energy_db, label=f'{freq_band.capitalize()} Frequency')

    ax3.set_xlabel("Time (samples)")
    ax3.set_ylabel("Energy Decay (dB)")
    ax3.set_title(f"Energy Decay Curve - {title}")
    ax3.legend()
    ax3.grid(True)

    # ✅ Ensure x-axis labels (time samples) are clear
    ax3.set_xticks(np.linspace(0, len(energy_db), num=10, dtype=int))  # Ensures clear labels
    plt.show()

# ===================== MAIN FUNCTION =====================
def main():
    # Get the directory where the current script resides.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, 'data')  # Path to the JSON data files
    
    # ✅ ONLY USING SELECTED 4 ROOMS
    room_configs = [
        "furnished_room.json",
        "empty_room.json",
        "treated_big_room.json",
        "untreated_big_room.json"
    ]

    for config_file in room_configs:
        full_path = os.path.join(config_path, config_file)
        room_specs = load_room_specs(full_path)

        # Initialize RoomAcoustics
        acoustics_simulator = RoomAcoustics(
            room_dims=room_specs['room_dims'],
            source_positions=room_specs['source_positions'],
            receiver_positions=room_specs['receiver_positions'],
            abs_coeff=room_specs['abs_coeff'],
            max_order=room_specs['max_order']
        )

        # Compute RT60 values
        rt60_values = calculate_rt60(
            room_dims=room_specs['room_dims'],
            abs_coeff=room_specs['abs_coeff']
        )

        # Print RT60 results
        print(f"\n=== {config_file} ===")
        for band, rt60 in rt60_values.items():
            print(f"RT60 ({band}): {rt60:.3f} seconds")

        # Simulate and plot impulse responses, RT60, and Decay Curves
        responses = simulate_acoustics(acoustics_simulator)
        plot_responses_and_rt60(responses, rt60_values, Path(config_file).stem)

if __name__ == "__main__":
    main()
