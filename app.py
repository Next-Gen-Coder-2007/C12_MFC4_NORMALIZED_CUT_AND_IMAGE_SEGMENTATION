from flask import Flask, render_template, request, jsonify
import cv2
import os
import time
import numpy as np
import json
from datetime import datetime
from segmentation_methods import (
    normalized_cut_segmentation,
    kmeans_segmentation,
    thresholding_segmentation,
    edge_detection_segmentation,
    region_growing_segmentation
)

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
RESULTS_FOLDER = "static/results"
HISTORY_FILE = "static/history.json"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)


def save_image(img, path):
    """Save image with proper normalization"""
    if len(img.shape) == 2:  # Grayscale
        img = img.astype(np.float32)
        img = img - img.min()
        img = img / (img.max() + 1e-8)
        img = (img * 255).astype(np.uint8)
    cv2.imwrite(path, img)


def load_history():
    """Load processing history from JSON file"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []


def save_history(entry):
    """Save a new entry to processing history"""
    history = load_history()
    history.insert(0, entry)  # Add to beginning
    # Keep only last 50 entries
    history = history[:50]
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/method/<method_name>", methods=["GET"])
def method_page(method_name):
    """Render the page for a specific segmentation method"""
    valid_methods = ['normalized-cut', 'kmeans', 'thresholding', 'edge-detection', 'region-growing']
    if method_name not in valid_methods:
        return "Method not found", 404
    return render_template(f"methods/{method_name}.html")


@app.route("/process", methods=["POST"])
def process_image():
    """Process image with selected segmentation method"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    method = request.form.get('method', 'normalized-cut')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Generate timestamp-based filenames
    timestamp = str(int(time.time()))
    input_filename = f"input_{timestamp}.jpg"
    result_filename = f"result_{method}_{timestamp}.png"
    
    input_path = os.path.join(UPLOAD_FOLDER, input_filename)
    result_path = os.path.join(RESULTS_FOLDER, result_filename)
    
    # Save uploaded image
    file.save(input_path)
    
    # Read and preprocess image
    image = cv2.imread(input_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Resize for processing (maintain aspect ratio)
    h, w = image.shape[:2]
    max_dim = 500
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        new_w, new_h = int(w * scale), int(h * scale)
        image = cv2.resize(image, (new_w, new_h))
    
    # Apply selected segmentation method
    try:
        if method == 'normalized-cut':
            result = normalized_cut_segmentation(image)
        elif method == 'kmeans':
            k = int(request.form.get('k', 3))
            result = kmeans_segmentation(image, k=k)
        elif method == 'thresholding':
            threshold = int(request.form.get('threshold', 128))
            result = thresholding_segmentation(image, threshold=threshold)
        elif method == 'edge-detection':
            low_threshold = int(request.form.get('low_threshold', 50))
            high_threshold = int(request.form.get('high_threshold', 150))
            result = edge_detection_segmentation(image, low_threshold, high_threshold)
        elif method == 'region-growing':
            result = region_growing_segmentation(image)
        else:
            return jsonify({'error': 'Invalid method'}), 400
        
        # Save result
        save_image(result, result_path)
        
        # Create history entry
        history_entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'method': method,
            'input_image': f"/{input_path}",
            'result_image': f"/{result_path}",
            'parameters': request.form.to_dict()
        }
        save_history(history_entry)
        
        return jsonify({
            'success': True,
            'input_image': f"/{input_path}",
            'result_image': f"/{result_path}"
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/history", methods=["GET"])
def history():
    """Display processing history"""
    history_data = load_history()
    return render_template("history.html", history=history_data)


@app.route("/clear-history", methods=["POST"])
def clear_history():
    """Clear all processing history"""
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    return jsonify({'success': True})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)