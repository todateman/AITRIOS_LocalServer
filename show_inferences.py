import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import argparse
import matplotlib.image as mpimg

def plot_inferences(file_path, image_path=None):
    # Load the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Extract the inference data
    inferences = data['Inferences'][0]  # Assuming only one set of inferences

    # Create the plot
    fig, ax = plt.subplots(figsize=(6, 6))

    # If an image path is provided, load and display it as the background
    if image_path:
        img = mpimg.imread(image_path)
        ax.imshow(img, extent=[0, 320, 0, 320])  # Set image size to match the coordinates of the plot

    # Iterate through each detected object and add rectangles and text
    for key, inference in inferences.items():
        if key == 'T':
            continue  # Skip the timestamp

        class_label = inference['C']
        confidence = inference['P']
        x, y, width, height = inference['X'], inference['Y'], inference['x'] - inference['X'], inference['y'] - inference['Y']
        
        # Add rectangle for the bounding box
        rect = patches.Rectangle((x, y), width, height, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        
        # Add class and confidence as text inside the box
        ax.text(x + width / 2, y + height / 2, f"Class: {class_label}\nConf: {confidence:.2f}", 
                color='white', ha='center', va='center', fontsize=8, fontweight='bold', bbox=dict(facecolor='red', alpha=0.5))

    # Set axis limits and labels
    ax.set_xlim(0, 320)
    ax.set_ylim(0, 320)  # Y-axis goes from top (0) to bottom (320)
    ax.set_title("Object Detection Bounding Boxes with Class and Confidence")

    # Display the plot
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

if __name__ == "__main__":
    # Command line argument parsing
    parser = argparse.ArgumentParser(description='Display object detection results from a JSON file with optional background image.')
    parser.add_argument('-j', '--json', type=str, required=True, help='Path to the JSON file with inference results.')
    parser.add_argument('-g', '--image', type=str, help='Path to the background image file (JPEG format).')
    args = parser.parse_args()

    # Call the function with the provided file path and optional image path
    plot_inferences(args.json, args.image)
