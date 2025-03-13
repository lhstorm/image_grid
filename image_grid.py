#!/usr/bin/env python3

"""
Image Grid Drawing Tool - Core Module

This module provides functions for loading images and drawing various types of grids.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io

def load_image(image_path):
    """
    Load an image from a file path.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        numpy.ndarray: The loaded image in BGR format (OpenCV format)
    """
    # Read the image
    image = cv2.imread(image_path)
    
    # Check if image was loaded successfully
    if image is None:
        raise ValueError(f"Could not load image from {image_path}")
    
    return image

def draw_grid(image, grid_size_x=50, grid_size_y=50, color=(255, 0, 0), 
              thickness=1, alpha=0.7, dashed=False, dash_length=10, dash_gap=10,
              offset_x=0, offset_y=0):
    """
    Draw a grid with fixed cell size on an image.
    
    Args:
        image (numpy.ndarray): Input image
        grid_size_x (int): Width of each grid cell in pixels
        grid_size_y (int): Height of each grid cell in pixels
        color (tuple): Grid color in BGR format (B, G, R)
        thickness (int): Line thickness
        alpha (float): Grid opacity (0.0 to 1.0)
        dashed (bool): Whether to use dashed lines
        dash_length (int): Length of each dash in pixels
        dash_gap (int): Gap between dashes in pixels
        offset_x (int): Horizontal offset for the grid in pixels
        offset_y (int): Vertical offset for the grid in pixels
        
    Returns:
        numpy.ndarray: Image with grid overlay
    """
    img_with_grid = image.copy()
    height, width = image.shape[:2]
    
    overlay = image.copy()
    
    # Draw vertical lines with offset
    for x in range(offset_x, width, grid_size_x):
        if not dashed:
            cv2.line(overlay, (x, 0), (x, height), color, thickness)
        else:
            # Draw dashed vertical lines
            for y in range(0, height, dash_length + dash_gap):
                y2 = min(y + dash_length, height)
                cv2.line(overlay, (x, y), (x, y2), color, thickness)
    
    # Draw horizontal lines with offset
    for y in range(offset_y, height, grid_size_y):
        if not dashed:
            cv2.line(overlay, (0, y), (width, y), color, thickness)
        else:
            # Draw dashed horizontal lines
            for x in range(0, width, dash_length + dash_gap):
                x2 = min(x + dash_length, width)
                cv2.line(overlay, (x, y), (x2, y), color, thickness)
    
    # Blend the overlay with the original image
    img_with_grid = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)
    
    return img_with_grid

def draw_adaptive_grid(image, num_cells_x=10, num_cells_y=10, color=(255, 0, 0), 
                      thickness=1, alpha=0.7, dashed=False, dash_length=10, dash_gap=10,
                      offset_x=0, offset_y=0):
    """
    Draw a grid with a fixed number of cells on an image.
    
    Args:
        image (numpy.ndarray): Input image
        num_cells_x (int): Number of horizontal cells
        num_cells_y (int): Number of vertical cells
        color (tuple): Grid color in BGR format (B, G, R)
        thickness (int): Line thickness
        alpha (float): Grid opacity (0.0 to 1.0)
        dashed (bool): Whether to use dashed lines
        dash_length (int): Length of each dash in pixels
        dash_gap (int): Gap between dashes in pixels
        offset_x (int): Horizontal offset for the grid in pixels
        offset_y (int): Vertical offset for the grid in pixels
        
    Returns:
        numpy.ndarray: Image with grid overlay
    """
    height, width = image.shape[:2]
    
    # Calculate cell sizes
    cell_width = width // num_cells_x
    cell_height = height // num_cells_y
    
    # Draw the grid using the calculated cell sizes
    return draw_grid(
        image, 
        grid_size_x=cell_width, 
        grid_size_y=cell_height, 
        color=color, 
        thickness=thickness, 
        alpha=alpha, 
        dashed=dashed, 
        dash_length=dash_length, 
        dash_gap=dash_gap,
        offset_x=offset_x,
        offset_y=offset_y
    )

def draw_golden_ratio_grid(image, divisions=2, color=(255, 215, 0), 
                          thickness=1, alpha=0.7, offset_x=0, offset_y=0):
    """
    Draw a golden ratio grid on an image.
    
    Args:
        image (numpy.ndarray): Input image
        divisions (int): Number of golden ratio divisions
        color (tuple): Grid color in BGR format (B, G, R)
        thickness (int): Line thickness
        alpha (float): Grid opacity (0.0 to 1.0)
        offset_x (int): Horizontal offset for the grid in pixels
        offset_y (int): Vertical offset for the grid in pixels
        
    Returns:
        numpy.ndarray: Image with golden ratio grid overlay
    """
    height, width = image.shape[:2]
    overlay = image.copy()
    
    # Golden ratio constant
    phi = 1.618033988749895
    
    # Calculate positions for golden ratio divisions
    positions_h = []
    positions_v = []
    
    # Calculate horizontal positions
    pos = offset_x
    for i in range(divisions):
        pos += width / (phi ** (i+1))
        positions_h.append(int(pos))
    
    # Calculate vertical positions
    pos = offset_y
    for i in range(divisions):
        pos += height / (phi ** (i+1))
        positions_v.append(int(pos))
    
    # Draw vertical lines
    for x in positions_h:
        cv2.line(overlay, (x, 0), (x, height), color, thickness)
    
    # Draw horizontal lines
    for y in positions_v:
        cv2.line(overlay, (0, y), (width, y), color, thickness)
    
    # Blend the overlay with the original image
    return cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

def draw_rule_of_thirds(image, color=(255, 255, 255), thickness=1, alpha=0.7):
    """
    Draw rule of thirds grid on image.
    
    Args:
        image (numpy.ndarray): Input image
        color (tuple): Grid color in BGR format (B, G, R)
        thickness (int): Line thickness
        alpha (float): Grid opacity (0.0 to 1.0)
        
    Returns:
        numpy.ndarray: Image with rule of thirds grid overlay
    """
    height, width = image.shape[:2]
    overlay = image.copy()
    
    # Calculate positions for rule of thirds
    h1 = height // 3
    h2 = 2 * height // 3
    w1 = width // 3
    w2 = 2 * width // 3
    
    # Draw vertical lines
    cv2.line(overlay, (w1, 0), (w1, height), color, thickness)
    cv2.line(overlay, (w2, 0), (w2, height), color, thickness)
    
    # Draw horizontal lines
    cv2.line(overlay, (0, h1), (width, h1), color, thickness)
    cv2.line(overlay, (0, h2), (width, h2), color, thickness)
    
    # Blend the overlay with the original image
    return cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

def draw_center_lines(image, color=(255, 255, 255), thickness=1, alpha=0.7):
    """
    Draw center lines on image.
    
    Args:
        image (numpy.ndarray): Input image
        color (tuple): Line color in BGR format (B, G, R)
        thickness (int): Line thickness
        alpha (float): Line opacity (0.0 to 1.0)
        
    Returns:
        numpy.ndarray: Image with center lines overlay
    """
    height, width = image.shape[:2]
    overlay = image.copy()
    
    # Calculate center positions
    center_h = height // 2
    center_w = width // 2
    
    # Draw vertical center line
    cv2.line(overlay, (center_w, 0), (center_w, height), color, thickness)
    
    # Draw horizontal center line
    cv2.line(overlay, (0, center_h), (width, center_h), color, thickness)
    
    # Blend the overlay with the original image
    return cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

def draw_guide_lines(image, h_pos_percent, v_pos_percent, color=(255, 0, 0), thickness=1):
    """
    Draw horizontal and vertical guide lines at specified positions.
    
    Args:
        image (numpy.ndarray): Input image
        h_pos_percent (int): Horizontal position as percentage of image height
        v_pos_percent (int): Vertical position as percentage of image width
        color (tuple): Line color in BGR format (B, G, R)
        thickness (int): Line thickness
        
    Returns:
        numpy.ndarray: Image with guide lines
    """
    height, width = image.shape[:2]
    result = image.copy()
    
    # Calculate pixel positions from percentages
    h_pixel = int(height * h_pos_percent / 100)
    v_pixel = int(width * v_pos_percent / 100)
    
    # Draw horizontal guide line
    cv2.line(result, (0, h_pixel), (width, h_pixel), color, thickness)
    
    # Draw vertical guide line
    cv2.line(result, (v_pixel, 0), (v_pixel, height), color, thickness)
    
    return result

def create_sample_image(width=800, height=600):
    """
    Create a sample image for testing.
    
    Args:
        width (int): Width of the sample image
        height (int): Height of the sample image
        
    Returns:
        numpy.ndarray: Sample image
    """
    # Create a gradient background
    x = np.linspace(0, 1, width)
    y = np.linspace(0, 1, height)
    
    # Create meshgrid
    X, Y = np.meshgrid(x, y)
    
    # Create RGB channels
    r = np.sin(X * 3 * np.pi) * 127 + 128
    g = np.sin(Y * 3 * np.pi) * 127 + 128
    b = np.sin((X + Y) * 3 * np.pi) * 127 + 128
    
    # Stack channels
    image = np.stack([b, g, r], axis=2).astype(np.uint8)
    
    # Add some shapes
    cv2.circle(image, (width // 4, height // 4), 50, (255, 0, 0), -1)
    cv2.rectangle(image, (width // 2, height // 2), (width // 2 + 100, height // 2 + 100), (0, 255, 0), -1)
    cv2.line(image, (0, height), (width, 0), (0, 0, 255), 5)
    
    return image

def cv2_to_pil(cv2_img):
    """
    Convert OpenCV image to PIL Image.
    
    Args:
        cv2_img (numpy.ndarray): OpenCV image in BGR format
        
    Returns:
        PIL.Image: PIL Image in RGB format
    """
    cv2_img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(cv2_img_rgb)

def pil_to_cv2(pil_img):
    """
    Convert PIL Image to OpenCV image.
    
    Args:
        pil_img (PIL.Image): PIL Image
        
    Returns:
        numpy.ndarray: OpenCV image in BGR format
    """
    numpy_img = np.array(pil_img)
    # Convert RGB to BGR if the image has 3 channels
    if len(numpy_img.shape) == 3 and numpy_img.shape[2] == 3:
        return cv2.cvtColor(numpy_img, cv2.COLOR_RGB2BGR)
    return numpy_img

if __name__ == "__main__":
    # Example usage
    print("This module provides functions for the Image Grid Drawing Tool.")
    print("Import it in your own scripts or run the Streamlit app with:")
    print("  streamlit run streamlit_app.py") 