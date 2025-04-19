import numpy as np
import matplotlib.pyplot as plt
import re

# Load and parse data
def parse_data(filepath):
    real_parts = []
    imaginary_parts = []
    x_vals = []
    y_vals = []

    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:
                x = float(parts[0])
                y = float(parts[1])
                complex_str = parts[2].replace("i", "j")

                try:
                    c = complex(complex_str)
                    x_vals.append(x)
                    y_vals.append(y)
                    real_parts.append(c.real)
                    imaginary_parts.append(c.imag)
                except ValueError:
                    print(f"Skipping line due to error: {line}")

    return np.array(x_vals), np.array(y_vals), np.array(real_parts), np.array(imaginary_parts)

# Visualisation
def plot_data(x_vals, y_vals, real_vals, imag_vals):
    fig = plt.figure(figsize=(12, 6))

    # Real part
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.scatter(x_vals, y_vals, real_vals, c=real_vals, cmap='coolwarm')
    ax1.set_title('Real Part')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Real')

    # Imaginary part
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.scatter(x_vals, y_vals, imag_vals, c=imag_vals, cmap='viridis')
    ax2.set_title('Imaginary Part')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Imaginary')

    plt.tight_layout()
    plt.show()

# Print extrema
def print_extremes(real_vals, imag_vals):
    print(f"Max Real Part: {np.max(real_vals)}")
    print(f"Min Real Part: {np.min(real_vals)}")
    print(f"Max Imaginary Part: {np.max(imag_vals)}")
    print(f"Min Imaginary Part: {np.min(imag_vals)}")

# Main
file_path = 'untitled.txt'
x_vals, y_vals, real_vals, imag_vals = parse_data(file_path)
plot_data(x_vals, y_vals, real_vals, imag_vals)
print_extremes(real_vals, imag_vals)
