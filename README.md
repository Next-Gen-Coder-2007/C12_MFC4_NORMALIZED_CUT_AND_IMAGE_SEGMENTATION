# Image Segmentation Using Classical Algorithms  
*(Based on IEEE Normalized Cut Framework)*

## Project Overview
This project implements and compares multiple **classical image segmentation techniques** inspired by the IEEE reference paper **“Normalized Cuts and Image Segmentation” (Document ID: 868688)**.  
The system provides a **web-based interface** that allows users to upload images, apply different segmentation algorithms, and visualize results.

The project bridges **theoretical concepts from the base paper** with **practical implementation using Python and OpenCV**.

---

## Team Members

| Name | Roll Number |
|----|----|
| Cibikumar B | CB.SC.U4AIE24212 |
| Naveen K | CB.SC.U4AIE24235 | 
| Sai Kushal B| CB.SC.U4AIE24252 |
| Subash B| CB.SC.U4AIE24254 |

---

## Base / Reference Paper

**Title:** Normalized Cuts and Image Segmentation  
**Authors:** Jianbo Shi, Jitendra Malik  
**Source:** IEEE Transactions on Pattern Analysis and Machine Intelligence  
**Document ID:** 868688  
**Link:** https://ieeexplore.ieee.org/document/868688  

### Key Idea from the Paper
The paper models image segmentation as a **graph partitioning problem**, where:
- Each pixel (or region) is a node
- Edge weights represent similarity
- Segmentation is achieved by minimizing the **Normalized Cut (Ncut)** value

---

## What We Implemented From the Paper

| Concept from Paper | Implementation in Project |
|------------------|---------------------------|
| Graph-based segmentation | Region adjacency graph using superpixels |
| Normalized Cut criterion | Eigenvalue-based spectral clustering |
| Similarity computation | Color and spatial distance |
| Recursive partitioning | Clustering of eigenvectors |

Instead of operating on **individual pixels** (which is computationally expensive), our implementation:
- Uses **SLIC superpixels** to reduce complexity
- Applies **spectral clustering** on region-level graph

---

## Implemented Segmentation Methods

### 1. Normalized Cut Segmentation (Core Contribution)
- Implemented using:
  - SLIC superpixels
  - Sparse affinity matrix
  - Graph Laplacian
  - Eigen decomposition
- Closely follows the methodology described in the IEEE paper
- Produces high-quality region-based segmentation

 Code: `segmentation_methods.py`

---

### 2. K-Means Clustering
- Unsupervised clustering based on pixel color features
- Faster but less accurate than Normalized Cut
- Used for comparison

---

### 3. Edge Detection
- Uses classical edge detection techniques
- Highlights object boundaries
- Does not produce region-based segmentation

---

### 4. Thresholding
- Segments image based on pixel intensity
- Works well only for high-contrast images

---

### 5. Region Growing
- Expands regions from seed points
- Sensitive to noise and parameter selection

---

## System Architecture

User → Web Interface → Flask Backend
→ Image Upload
→ Segmentation Method Selection
→ Processing (OpenCV / Scikit-image)
→ Output Visualization


---

## Technologies Used

- **Programming Language:** Python
- **Framework:** Flask
- **Libraries:**
  - OpenCV
  - NumPy
  - SciPy
  - scikit-image
  - scikit-learn
- **Frontend:** HTML, CSS (Jinja templates)

---

## Project Structure

- final
  - app.py
  - segmentation_methods.py
  - static
    - uploads
    - results
  - templates
    - index.html
    - history.html
    - methods


---

## Current Project Status (Updates)

- ✔ Studied and analyzed base IEEE paper
- ✔ Implemented Normalized Cut algorithm
- ✔ Integrated multiple segmentation techniques
- ✔ Developed web-based UI
- ✔ Generated and stored segmentation results

---

## Challenges / Issues Faced

- Understanding spectral graph theory concepts
- High computational cost of Normalized Cut
- Eigenvalue convergence issues
- Parameter tuning for segmentation quality
- Managing performance for large images

---

## Future Plans

- Optimize Normalized Cut using GPU acceleration
- Add quantitative evaluation metrics
- Implement deep-learning-based segmentation for comparison
- Improve UI and result visualization
- Extend support to video segmentation

---

## Conclusion
This project successfully demonstrates how a **theoretical IEEE research paper** can be transformed into a **functional real-world application**.  
Normalized Cut segmentation provided the best balance between accuracy and theoretical soundness when compared with other classical methods.

---



# Project Update

## Changes Implemented

The following updates were made to improve the project quality, clarity, and experimental results.

### 1. Improved Figures
- Added clearer and higher quality figures to properly show the results.
- Figures are now easier to understand and interpret.

### 2. More Experimental Results
- Added additional results to better evaluate the model.
- This helps identify where the method performs well and where it does not.

### 3. Proper Examples
- Included detailed examples to explain the methodology and outputs.
- Examples help in understanding how the system works step by step.

### 4. Graph Representation
- Added graphs to represent experimental results visually.
- Graphs are included as images for better readability.

### 5. Original Images
- Included original sample images used in experiments.
- This improves transparency and reproducibility of the results.

### 6. Standard Dataset
- Used a standard dataset for testing and evaluation.
- This allows fair comparison with other approaches.

### 7. Superpixel Explanation
- Added a clear explanation of the **Superpixel** concept used in the project.
- Explained how superpixels help in image segmentation and analysis.

### 8. Simple Image Demonstrations
- Added simple images to demonstrate how the algorithm processes data.
- Helps readers easily understand the workflow.

---

## Summary
These updates improve the clarity, experimental validation, and explanation of the project, making the work easier to understand and reproduce.

## References

1. J. Shi and J. Malik, *“Normalized Cuts and Image Segmentation,”* IEEE TPAMI, 2000.
2. OpenCV Documentation
3. scikit-image Documentation
