#!/usr/bin/env python3

"""
Image Grid Drawing Tool - Demo Script

This script demonstrates how to use the image grid drawing functionality programmatically.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image

# Import functions from our module
from image_grid import load_image, draw_grid, draw_adaptive_grid, create_sample_image, display_image

def main():
    print("Image Grid Drawing Tool - Demo")
    print("==============================\n")
    
    # Create a sample image
    print("Creating sample image...")
    sample_image = create_sample_image(width=800, height=600)
    
    # Display the sample image
    display_image(sample_image, "Sample Image")
    
    # Example 1: Basic grid
    print("\nExample 1: Drawing a basic grid (50x50 pixels, red lines)")
    basic_grid = draw_grid(sample_image, grid_size_x=50, grid_size_y=50, color=(255, 0, 0))
    display_image(basic_grid, "Basic Grid (50x50 pixels)")
    
    # Example 2: Adaptive grid
    print("\nExample 2: Drawing an adaptive grid (8x6 cells, green lines)")
    adaptive_grid = draw_adaptive_grid(
        sample_image, 
        num_cells_x=8, 
        num_cells_y=6, 
        color=(0, 255, 0), 
        thickness=2
    )
    display_image(adaptive_grid, "Adaptive Grid (8x6 cells)")
    
    # Example 3: Dashed grid
    print("\nExample 3: Drawing a dashed grid (100x100 pixels, blue lines)")
    dashed_grid = draw_grid(
        sample_image, 
        grid_size_x=100, 
        grid_size_y=100, 
        color=(0, 0, 255), 
        dashed=True, 
        dash_length=15
    )
    display_image(dashed_grid, "Dashed Grid (100x100 pixels)")
    
    # Example 4: Offset grid
    print("\nExample 4: Drawing an offset grid (75x75 pixels, magenta lines, offset 25,25)")
    offset_grid = draw_grid(
        sample_image, 
        grid_size_x=75, 
        grid_size_y=75, 
        color=(255, 0, 255), 
        offset_x=25, 
        offset_y=25
    )
    display_image(offset_grid, "Offset Grid (75x75 pixels, offset 25,25)")
    
    # Example 5: Using your own image
    print("\nExample 5: Using your own image")
    print("To use your own image, uncomment and modify the code below:")
    print("""
    # Replace with your image path
    image_path = 'path/to/your/image.jpg'
    
    try:
        # Load the image
        your_image = load_image(image_path)
        display_image(your_image, "Your Original Image")
        
        # Apply a grid
        your_grid = draw_grid(your_image, grid_size_x=50, grid_size_y=50)
        display_image(your_grid, "Your Image with Grid")
        
        # Save the result
        cv2.imwrite('your_image_with_grid.jpg', cv2.cvtColor(your_grid, cv2.COLOR_RGB2BGR))
        print(f"Saved result to 'your_image_with_grid.jpg'")
    except Exception as e:
        print(f"Error: {e}")
    """)
    
    print("\nFor more options and interactive usage, run the Streamlit app:")
    print("streamlit run streamlit_app.py")

if __name__ == "__main__":
    main() 