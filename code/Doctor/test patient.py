import tkinter as tk
from tkinter import font

def calculate_entry_width_in_columns(pixel_width, font_name="Poppins", font_size=16):
    # Create a temporary root to measure font dimensions
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Create a font object
    test_font = font.Font(family=font_name, size=font_size)
    
    # Measure the width of a single character ('0' is often used as a representative character)
    char_width = test_font.measure('0')
    
    # Calculate the required number of columns
    columns = pixel_width // char_width
    
    root.destroy()  # Clean up the temporary root window
    return int(columns)

# Example usage
desired_pixel_width = 396  # Target width in pixels
calculated_columns = calculate_entry_width_in_columns(desired_pixel_width)
print(calculated_columns)
