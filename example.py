#!/usr/bin/env python3

"""
Image Grid Drawing Tool - Example Script

This script demonstrates how to use the image_grid module to draw various types of grids.
"""

import cv2
import numpy as np
import os
from image_grid import (
    load_image, 
    draw_grid, 
    draw_adaptive_grid, 
    draw_golden_ratio_grid,
    draw_rule_of_thirds,
    create_sample_image
)

def save_example_images():
    """Generate and save example images with different grid types."""
    # Create examples directory if it doesn't exist
    if not os.path.exists('examples'):
        os.makedirs('examples')
    
    # Create a sample image
    image = create_sample_image(800, 600)
    
    # Save the original image
    cv2.imwrite('examples/original.jpg', image)
    
    # Example 1: Fixed-size grid (50x50 pixels)
    fixed_grid = draw_grid(
        image, 
        grid_size_x=50, 
        grid_size_y=50, 
        color=(0, 0, 255),  # Red in BGR
        thickness=1,
        alpha=0.7
    )
    cv2.imwrite('examples/fixed_size_grid.jpg', fixed_grid)
    
    # Example 2: Adaptive grid (10x8 cells)
    adaptive_grid = draw_adaptive_grid(
        image, 
        num_cells_x=10, 
        num_cells_y=8, 
        color=(0, 255, 0),  # Green in BGR
        thickness=1,
        alpha=0.7
    )
    cv2.imwrite('examples/adaptive_grid.jpg', adaptive_grid)
    
    # Example 3: Golden ratio grid
    golden_grid = draw_golden_ratio_grid(
        image, 
        divisions=2, 
        color=(0, 215, 255),  # Gold in BGR
        thickness=1,
        alpha=0.7
    )
    cv2.imwrite('examples/golden_ratio_grid.jpg', golden_grid)
    
    # Example 4: Rule of thirds
    thirds_grid = draw_rule_of_thirds(
        image, 
        color=(255, 255, 255),  # White in BGR
        thickness=1,
        alpha=0.7
    )
    cv2.imwrite('examples/rule_of_thirds.jpg', thirds_grid)
    
    # Example 5: Grid with offset (position)
    # Offset to the right
    offset_right = draw_grid(
        image, 
        grid_size_x=50, 
        grid_size_y=50, 
        color=(0, 0, 255),  # Red in BGR
        thickness=1,
        alpha=0.7,
        offset_x=25,
        offset_y=0
    )
    cv2.imwrite('examples/offset_grid_right.jpg', offset_right)
    
    # Offset down
    offset_down = draw_grid(
        image, 
        grid_size_x=50, 
        grid_size_y=50, 
        color=(0, 0, 255),  # Red in BGR
        thickness=1,
        alpha=0.7,
        offset_x=0,
        offset_y=25
    )
    cv2.imwrite('examples/offset_grid_down.jpg', offset_down)
    
    # Offset diagonally
    offset_diagonal = draw_grid(
        image, 
        grid_size_x=50, 
        grid_size_y=50, 
        color=(0, 0, 255),  # Red in BGR
        thickness=1,
        alpha=0.7,
        offset_x=25,
        offset_y=25
    )
    cv2.imwrite('examples/offset_grid_diagonal.jpg', offset_diagonal)
    
    # Create a composite image showing grid positioning
    # Create a blank canvas
    height, width = image.shape[:2]
    composite = np.zeros((height * 2, width * 2, 3), dtype=np.uint8)
    
    # Place images in a 2x2 grid
    composite[0:height, 0:width] = image  # Original
    composite[0:height, width:width*2] = offset_right  # Right offset
    composite[height:height*2, 0:width] = offset_down  # Down offset
    composite[height:height*2, width:width*2] = offset_diagonal  # Diagonal offset
    
    # Add labels
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(composite, "Original", (10, 30), font, 1, (255, 255, 255), 2)
    cv2.putText(composite, "Offset Right", (width + 10, 30), font, 1, (255, 255, 255), 2)
    cv2.putText(composite, "Offset Down", (10, height + 30), font, 1, (255, 255, 255), 2)
    cv2.putText(composite, "Offset Diagonal", (width + 10, height + 30), font, 1, (255, 255, 255), 2)
    
    cv2.imwrite('examples/grid_positioning.jpg', composite)
    
    print("Example images saved to 'examples' directory.")

if __name__ == "__main__":
    save_example_images() 