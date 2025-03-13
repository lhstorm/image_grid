#!/usr/bin/env python3

"""
Image Grid Drawing Tool - Streamlit App

This app provides a user-friendly interface for reading images and drawing
customizable grids over them.
"""

import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
import io
from image_grid import load_image, draw_grid, draw_adaptive_grid, create_sample_image

# Set page configuration
st.set_page_config(
    page_title="Image Grid Drawing Tool",
    page_icon="🔲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    .stButton button {
        width: 100%;
    }
    .highlight {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .grid-info {
        background-color: #e6f3ff;
        padding: 0.5rem;
        border-radius: 0.3rem;
        margin-top: 0.5rem;
    }
    .position-controls {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 1rem;
    }
    .position-row {
        display: flex;
        justify-content: center;
        width: 100%;
        margin: 0.2rem 0;
    }
    .position-button {
        margin: 0 0.2rem;
    }
    /* Increase sidebar width */
    [data-testid="stSidebar"] {
        min-width: 350px;
        max-width: 450px;
    }
    /* Adjust main content area to accommodate wider sidebar */
    .main .block-container {
        max-width: calc(100% - 450px);
    }
    /* Improve tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e6f3ff;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.markdown("<h1 class='main-header'>Image Grid Drawing Tool</h1>", unsafe_allow_html=True)
st.markdown("""
This app allows you to upload an image and draw customizable grids over it.
You can adjust grid size, color, thickness, and transparency to suit your needs.
Perfect for photography composition, image analysis, and design reference.
""")

# Add a quick help section
with st.expander("📋 Quick Guide"):
    st.markdown("""
    ### How to use this tool:
    1. **Select an image source** in the sidebar (upload, camera, or sample)
    2. **Choose a grid type** and customize its appearance
    3. **Position the grid** using sliders or arrow buttons
    4. **Enable additional features** like rule of thirds or guide lines
    5. **Download** the final image with your custom grid
    
    Use the tabs in the sidebar to navigate between different settings.
    """)

# Sidebar for controls
st.sidebar.markdown("<h2 class='sub-header'>Image Grid Tool</h2>", unsafe_allow_html=True)

# Create tabs for better organization
tab1, tab2, tab3 = st.sidebar.tabs(["Image Source", "Grid Settings", "Advanced"])

# Tab 1: Image Source
with tab1:
    # Image source selection
    image_source = st.radio(
        "Image Source",
        ["Upload Image", "Use Sample Image", "Use Camera"]
    )
    
    if image_source == "Upload Image":
        uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png", "bmp"])
    elif image_source == "Use Camera":
        camera_image = st.camera_input("Take a picture")

# Tab 2: Grid Settings
with tab2:
    # Grid type selection with better layout
    st.markdown("<h4>Grid Type</h4>", unsafe_allow_html=True)
    grid_type = st.radio(
        "",  # Empty label since we're using the markdown header
        ["Fixed Size Grid", "Fixed Number of Cells", "Golden Ratio Grid"],
        horizontal=True  # Display options horizontally
    )
    
    # Grid parameters based on type
    if grid_type == "Fixed Size Grid":
        col1, col2 = st.columns(2)
        with col1:
            grid_size_x = st.slider("Horizontal Size (px)", 10, 200, 50, 5)
        with col2:
            grid_size_y = st.slider("Vertical Size (px)", 10, 200, 50, 5)
    elif grid_type == "Fixed Number of Cells":
        col1, col2 = st.columns(2)
        with col1:
            num_cells_x = st.slider("Horizontal Cells", 2, 50, 10)
        with col2:
            num_cells_y = st.slider("Vertical Cells", 2, 50, 10)
    else:  # Golden Ratio Grid
        num_divisions = st.slider("Number of Divisions", 1, 5, 2)
    
    st.markdown("---")
    st.markdown("<h4>Grid Appearance</h4>", unsafe_allow_html=True)
    
    # Color selection with custom color option
    col1, col2 = st.columns([3, 2])
    with col1:
        color_options = {
            "Red": (255, 0, 0),
            "Green": (0, 255, 0),
            "Blue": (0, 0, 255),
            "Yellow": (255, 255, 0),
            "Cyan": (0, 255, 255),
            "Magenta": (255, 0, 255),
            "White": (255, 255, 255),
            "Black": (0, 0, 0),
            "Custom": "custom"
        }
        color_choice = st.selectbox("Grid Color", list(color_options.keys()))
    
    with col2:
        if color_choice == "Custom":
            custom_color = st.color_picker("Pick a color", "#FF0000")
            # Convert hex to RGB
            hex_color = custom_color.lstrip('#')
            color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        else:
            color = color_options[color_choice]
            # Display a color preview
            st.markdown(f"""
            <div style="background-color: rgb{color}; width: 30px; height: 30px; border-radius: 5px; margin-top: 25px;"></div>
            """, unsafe_allow_html=True)
    
    # Line style
    st.markdown("<h5>Line Style</h5>", unsafe_allow_html=True)
    line_style = st.radio("", ["Solid", "Dashed"], horizontal=True)
    if line_style == "Dashed":
        col1, col2 = st.columns(2)
        with col1:
            dash_length = st.slider("Dash Length", 5, 30, 10)
        with col2:
            dash_gap = st.slider("Dash Gap", 5, 30, 10)
    
    col1, col2 = st.columns(2)
    with col1:
        thickness = st.slider("Line Thickness", 1, 5, 1)
    with col2:
        alpha = st.slider("Grid Opacity", 0.1, 1.0, 0.7, 0.1)
    
    st.markdown("---")
    st.markdown("<h4>Grid Position</h4>", unsafe_allow_html=True)
    
    # Initialize position state if not exists
    if 'offset_x' not in st.session_state:
        st.session_state.offset_x = 0
    if 'offset_y' not in st.session_state:
        st.session_state.offset_y = 0
    
    # Functions to move grid
    def move_left():
        st.session_state.offset_x = max(0, st.session_state.offset_x - 5)
        
    def move_right():
        st.session_state.offset_x = min(100, st.session_state.offset_x + 5)
        
    def move_up():
        st.session_state.offset_y = max(0, st.session_state.offset_y - 5)
        
    def move_down():
        st.session_state.offset_y = min(100, st.session_state.offset_y + 5)
    
    def reset_position():
        st.session_state.offset_x = 0
        st.session_state.offset_y = 0
    
    # Slider controls for precise positioning
    col1, col2 = st.columns(2)
    with col1:
        offset_x = st.slider("Horizontal", 0, 100, st.session_state.offset_x, 1, 
                           key="offset_x_slider", help="Move grid horizontally")
    with col2:
        offset_y = st.slider("Vertical", 0, 100, st.session_state.offset_y, 1,
                           key="offset_y_slider", help="Move grid vertically")
    
    # Update session state from sliders
    st.session_state.offset_x = offset_x
    st.session_state.offset_y = offset_y
    
    # Button controls for incremental movement
    st.markdown("<div class='position-controls'>", unsafe_allow_html=True)
    
    # Up button row
    st.markdown("<div class='position-row'>", unsafe_allow_html=True)
    st.button("⬆️", on_click=move_up, help="Move grid up", key="up_button")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Left, Reset, Right button row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("⬅️", on_click=move_left, help="Move grid left", key="left_button")
    with col2:
        st.button("⟲", on_click=reset_position, help="Reset grid position", key="reset_button")
    with col3:
        st.button("➡️", on_click=move_right, help="Move grid right", key="right_button")
    
    # Down button row
    st.markdown("<div class='position-row'>", unsafe_allow_html=True)
    st.button("⬇️", on_click=move_down, help="Move grid down", key="down_button")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Tab 3: Advanced Options
with tab3:
    # Organize checkboxes in columns
    col1, col2 = st.columns(2)
    with col1:
        show_grid = st.checkbox("Show Grid", True, help="Toggle grid visibility")
        show_rule_of_thirds = st.checkbox("Rule of Thirds", False)
    with col2:
        show_grid_info = st.checkbox("Show Grid Info", True)
        show_center_lines = st.checkbox("Center Lines", False)
    
    show_position_info = st.checkbox("Show Position Information", True)
    
    # Guide lines options
    st.markdown("<h4>Guide Lines</h4>", unsafe_allow_html=True)
    use_guide_lines = st.checkbox("Enable Guide Lines", False, 
                                help="Show adjustable guide lines for precise measurements")
    
    if use_guide_lines:
        col1, col2 = st.columns([3, 2])
        with col1:
            guide_line_color = st.color_picker("Guide Line Color", "#FF0000")
        with col2:
            guide_line_thickness = st.slider("Thickness", 1, 5, 1)
        
        guide_line_opacity = st.slider("Opacity", 0.1, 1.0, 0.7, 0.1)
        
        # Convert hex to RGB
        hex_color = guide_line_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        guide_color = (r, g, b)

# Main content area with two columns
col1, col2 = st.columns([1, 1])

# Function to draw grid with offset
def draw_offset_grid(image, grid_size_x=50, grid_size_y=50, offset_x=0, offset_y=0, color=(255, 0, 0), 
                    thickness=1, alpha=0.7, dashed=False, dash_length=10, dash_gap=10):
    """Draw a grid with custom offset."""
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

# Function to draw rule of thirds
def draw_rule_of_thirds(image, color=(255, 255, 255), thickness=1, alpha=0.7):
    """Draw rule of thirds grid on image."""
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

# Function to draw center lines
def draw_center_lines(image, color=(255, 255, 255), thickness=1, alpha=0.7):
    """Draw center lines on image."""
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

# Function to draw golden ratio grid
def draw_golden_ratio_grid(image, divisions=2, color=(255, 215, 0), thickness=1, alpha=0.7, offset_x=0, offset_y=0):
    """Draw golden ratio grid on image."""
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

# Function to draw guide lines
def draw_guide_lines(image, h_pos_percent, v_pos_percent, color=(255, 0, 0), thickness=1):
    """Draw horizontal and vertical guide lines at specified positions."""
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

# Function to convert OpenCV image to PIL Image
def cv2_to_pil(cv2_img):
    """Convert OpenCV image to PIL Image."""
    cv2_img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(cv2_img_rgb)

# Function to convert PIL Image to OpenCV image
def pil_to_cv2(pil_img):
    """Convert PIL Image to OpenCV image."""
    return np.array(pil_img)

# Load image based on selection
if image_source == "Upload Image":
    if 'uploaded_file' in locals() and uploaded_file is not None:
        # Read the image
        pil_image = Image.open(uploaded_file)
        image = np.array(pil_image)
        # Convert to RGB if it's RGBA
        if len(image.shape) == 3 and image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        # Convert grayscale to RGB if needed
        elif len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        aspect_ratio = image.shape[1] / image.shape[0]
    else:
        # If no image is uploaded, use a placeholder
        st.info("Please upload an image or select 'Use Sample Image'")
        image = None
        aspect_ratio = None
elif image_source == "Use Camera":
    if 'camera_image' in locals() and camera_image is not None:
        # Read the image
        pil_image = Image.open(camera_image)
        image = np.array(pil_image)
        # Convert to RGB if it's RGBA
        if len(image.shape) == 3 and image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    else:
        st.info("Please take a picture or select another image source")
        image = None
else:
    # Use the sample image
    image = create_sample_image()

# Process and display images if an image is loaded
if image is not None:
    # Display original image
    with col1:
        st.markdown("<h3>Original Image</h3>", unsafe_allow_html=True)
        st.image(image, caption="Original Image", use_container_width=True)
        
        # Show image information
        with st.expander("Image Information"):
            height, width = image.shape[:2]
            aspect_ratio = width / height
            st.markdown(f"""
            - **Dimensions**: {width} × {height} pixels
            - **Aspect ratio**: {aspect_ratio:.2f}
            - **In-memory size**: {image.nbytes / (1024*1024):.2f} MB (uncompressed)
            """)
    
    # Apply grid based on selected parameters
    with col2:
        st.markdown("<h3>Image with Grid</h3>", unsafe_allow_html=True)
        
        # Start with the original image
        processed_image = image.copy()
        
        # Apply the main grid based on type if grid is enabled
        if show_grid and grid_type == "Fixed Size Grid":
            is_dashed = line_style == "Dashed"
            dash_params = {}
            if is_dashed:
                dash_params = {"dash_length": dash_length, "dash_gap": dash_gap}
            
            processed_image = draw_offset_grid(
                processed_image, 
                grid_size_x=grid_size_x, 
                grid_size_y=grid_size_y, 
                offset_x=st.session_state.offset_x, 
                offset_y=st.session_state.offset_y, 
                color=color, 
                thickness=thickness, 
                alpha=alpha,
                dashed=is_dashed,
                **dash_params
            )
            
            # Display grid information
            if show_grid_info:
                grid_caption = f"Grid with {grid_size_x}x{grid_size_y} pixel cells"
                height, width = image.shape[:2]
                h_cells = width // grid_size_x
                v_cells = height // grid_size_y
                grid_info = f"Approx. {h_cells}x{v_cells} cells in the grid"
            else:
                grid_caption = "Image with Grid"
                grid_info = ""
                
        elif show_grid and grid_type == "Fixed Number of Cells":
            is_dashed = line_style == "Dashed"
            
            # Calculate cell sizes
            height, width = image.shape[:2]
            grid_size_x = width // num_cells_x
            grid_size_y = height // num_cells_y
            
            # Draw the grid
            if is_dashed:
                processed_image = draw_offset_grid(
                    processed_image,
                    grid_size_x=grid_size_x,
                    grid_size_y=grid_size_y,
                    offset_x=st.session_state.offset_x,
                    offset_y=st.session_state.offset_y,
                    color=color,
                    thickness=thickness,
                    alpha=alpha,
                    dashed=True,
                    dash_length=dash_length,
                    dash_gap=dash_gap
                )
            else:
                processed_image = draw_offset_grid(
                    processed_image, 
                    grid_size_x=grid_size_x, 
                    grid_size_y=grid_size_y,
                    offset_x=st.session_state.offset_x,
                    offset_y=st.session_state.offset_y,
                    color=color, 
                    thickness=thickness, 
                    alpha=alpha
                )
            
            # Display grid information
            if show_grid_info:
                grid_caption = f"Grid with {num_cells_x}x{num_cells_y} cells"
                grid_info = f"Cell size: approx. {grid_size_x}x{grid_size_y} pixels"
            else:
                grid_caption = "Image with Grid"
                grid_info = ""
        elif show_grid and grid_type == "Golden Ratio Grid":  # Golden Ratio Grid
            processed_image = draw_golden_ratio_grid(
                processed_image,
                divisions=num_divisions,
                color=color,
                thickness=thickness,
                alpha=alpha,
                offset_x=st.session_state.offset_x,
                offset_y=st.session_state.offset_y
            )
            
            # Display grid information
            if show_grid_info:
                grid_caption = f"Golden Ratio Grid ({num_divisions} divisions)"
                grid_info = "Based on the golden ratio (φ ≈ 1.618)"
            else:
                grid_caption = "Image with Golden Ratio Grid"
                grid_info = ""
        else:
            # No grid applied
            grid_caption = "Image without Grid" if not show_grid else "Image with Grid"
            grid_info = ""
        
        # Add rule of thirds if selected
        if show_grid and show_rule_of_thirds:
            # Use a different color for rule of thirds
            thirds_color = (255, 255, 255) if color != (255, 255, 255) else (0, 0, 255)
            processed_image = draw_rule_of_thirds(
                processed_image,
                color=thirds_color,
                thickness=thickness,
                alpha=alpha
            )
            if grid_info:
                grid_info += " + Rule of Thirds"
        
        # Add center lines if selected
        if show_grid and show_center_lines:
            # Use a different color for center lines
            center_color = (255, 255, 255) if color != (255, 255, 255) else (0, 0, 255)
            processed_image = draw_center_lines(
                processed_image,
                color=center_color,
                thickness=thickness,
                alpha=alpha
            )
            if grid_info:
                grid_info += " + Center Lines"
        
        # Display position information if selected
        if show_grid and show_position_info and (st.session_state.offset_x > 0 or st.session_state.offset_y > 0):
            if grid_info:
                grid_info += f" | Position: ({st.session_state.offset_x}, {st.session_state.offset_y})"
            else:
                grid_info = f"Position: ({st.session_state.offset_x}, {st.session_state.offset_y})"
        
        # Display the grid image
        if use_guide_lines:
            # Create a container for the image and guide line controls
            guide_container = st.container()
            
            # Create columns for the sliders with better layout
            guide_cols = st.columns([1, 1])
            
            with guide_cols[0]:
                # Horizontal guide line position slider
                h_pos = st.slider("Horizontal Guide", 0, 100, 50, 1, 
                                 key="h_guide_slider", 
                                 help="Position of horizontal guide line (percentage of image height)")
            
            with guide_cols[1]:
                # Vertical guide line position slider
                v_pos = st.slider("Vertical Guide", 0, 100, 50, 1,
                                 key="v_guide_slider", 
                                 help="Position of vertical guide line (percentage of image width)")
            
            # Use the dedicated guide lines function
            guide_image = draw_guide_lines(processed_image, h_pos, v_pos, guide_color, guide_line_thickness)
            
            # Display the image with guide lines
            with guide_container:
                st.image(guide_image, caption=grid_caption, use_container_width=True)
                
                # Show guide line information with more details
                guide_info = f"Guide positions: Horizontal {h_pos}%, Vertical {v_pos}%"
                if grid_info:
                    guide_info += f" | {grid_info}"
                st.markdown(f"<div class='grid-info'>{guide_info}</div>", unsafe_allow_html=True)
        else:
            # Display the regular grid image without guide lines
            st.image(processed_image, caption=grid_caption, use_container_width=True)
            if grid_info:
                st.markdown(f"<div class='grid-info'>{grid_info}</div>", unsafe_allow_html=True)
        
        # Download section with better layout
        st.markdown("---")
        download_col1, download_col2 = st.columns([3, 1])
        
        with download_col1:
            # Prepare the image for download
            if use_guide_lines:
                download_image = guide_image
            else:
                download_image = processed_image
                
            pil_grid_image = cv2_to_pil(download_image)
            buf = io.BytesIO()
            pil_grid_image.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            # Custom filename with grid type
            if grid_type == "Fixed Size Grid":
                filename = f"grid_{grid_size_x}x{grid_size_y}px.png"
            elif grid_type == "Fixed Number of Cells":
                filename = f"grid_{num_cells_x}x{num_cells_y}cells.png"
            else:
                filename = f"golden_ratio_grid.png"
            
            st.download_button(
                label="Download Image with Grid",
                data=byte_im,
                file_name=filename,
                mime="image/png",
                help="Save the processed image with grid to your device"
            )
        
        with download_col2:
            # Display image dimensions
            st.markdown(f"<div style='margin-top: 10px;'>{width}×{height}px</div>", unsafe_allow_html=True)
else:
    # Display a more helpful message when no image is loaded
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background-color: #f8f9fa; border-radius: 0.5rem; margin: 1rem 0;">
        <h3>No Image Loaded</h3>
        <p>Please select an image source from the sidebar to get started.</p>
        <p>You can upload your own image, take a picture with your camera, or use the sample image.</p>
    </div>
    """, unsafe_allow_html=True)

# Add information about the app
st.markdown("---")
st.markdown("""
<div class="highlight">
<h3>About this App</h3>

<p>This app uses OpenCV and Streamlit to draw customizable grids over images. 
It's useful for image analysis, segmentation tasks, or adding visual references to images.</p>

<h4>Features:</h4>
<ul>
<li>Upload your own images, use a sample image, or take a picture with your camera</li>
<li>Choose between fixed-size grids, fixed number of cells, or golden ratio grid</li>
<li>Add rule of thirds and center lines for composition guidance</li>
<li>Customize grid color, thickness, opacity, and line style (solid or dashed)</li>
<li>Move grid position with interactive controls</li>
<li>Toggle grid visibility on and off</li>
<li>Add adjustable horizontal and vertical guide lines</li>
<li>Download the resulting image with the grid</li>
</ul>

<h4>Use Cases:</h4>
<ul>
<li>Photography composition guides</li>
<li>Image analysis and segmentation</li>
<li>Design and layout reference</li>
<li>Educational purposes</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit and OpenCV") 