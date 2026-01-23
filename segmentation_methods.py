import numpy as np
import cv2
from skimage.segmentation import slic
from skimage.color import rgb2lab
from scipy.sparse import lil_matrix, diags
from scipy.sparse.linalg import eigsh
from sklearn.cluster import KMeans

def normalized_cut_segmentation(image, n_segments=250, sigma_I=20, sigma_X=40):
    sp = slic(image, n_segments=n_segments, compactness=10, start_label=0)
    lab = rgb2lab(image)
    regions = sp.max() + 1

    feats = []
    centers = []

    for r in range(regions):
        mask = sp == r
        pixels = lab[mask]
        feats.append(pixels.mean(axis=0))

        coords = np.column_stack(np.where(mask))
        centers.append(coords.mean(axis=0))

    feats = np.array(feats)
    centers = np.array(centers)

    adj = set()
    h, w = sp.shape

    for i in range(h - 1):
        for j in range(w - 1):
            a = sp[i, j]
            b = sp[i + 1, j]
            c = sp[i, j + 1]

            if a != b:
                adj.add((a, b))
                adj.add((b, a))

            if a != c:
                adj.add((a, c))
                adj.add((c, a))

    W = lil_matrix((regions, regions))

    for i, j in adj:
        dI = np.linalg.norm(feats[i] - feats[j]) ** 2
        dX = np.linalg.norm(centers[i] - centers[j]) ** 2

        w = np.exp(-dI / sigma_I**2) * np.exp(-dX / sigma_X**2)

        if w > 1e-6:
            W[i, j] = w
            W[j, i] = w

    D = np.array(W.sum(axis=1)).flatten()
    D[D == 0] = 1e-6

    Dm = diags(D)
    L = Dm - W

    _, vecs = eigsh(L, k=2, M=Dm, which="SM")
    fiedler = vecs[:, 1]

    partition = fiedler > 0

    seg = np.zeros_like(sp)

    for r in range(regions): 
        seg[sp == r] = int(partition[r])

    output = np.zeros_like(image)
    output[seg == 0] = [255, 100, 100]
    output[seg == 1] = [100, 100, 255]

    return output

def kmeans_segmentation(image, k=3):
    h, w, c = image.shape
    pixels = image.reshape(-1, 3).astype(np.float32)
    
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(pixels)
    
    centers = kmeans.cluster_centers_.astype(np.uint8)
    
    segmented = centers[labels]
    
    output = segmented.reshape(h, w, c)
    
    return output


def thresholding_segmentation(image, threshold=128):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    
    _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    output = np.zeros_like(image)
    output[binary > 0] = [255, 255, 255]  # White
    output[binary == 0] = [0, 0, 0]  # Black
    
    edges = cv2.Canny(binary, 50, 150)
    output[edges > 0] = [0, 255, 0]
    
    return output


def edge_detection_segmentation(image, low_threshold=50, high_threshold=150):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    blurred = cv2.GaussianBlur(gray, (5, 5), 1.4)
    
    edges = cv2.Canny(blurred, low_threshold, high_threshold)
    
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    output = image.copy()
    
    output[edges > 0] = [255, 0, 0]
    
    cv2.drawContours(output, contours, -1, (0, 255, 0), 2)
    
    return output


def region_growing_segmentation(image, num_seeds=10, threshold=20):

    h, w, c = image.shape
    
    lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB).astype(np.float32)
    
    segmented = np.zeros((h, w), dtype=np.int32)
    
    # Generate random seed points
    np.random.seed(42)
    seeds = []
    for i in range(num_seeds):
        y = np.random.randint(h)
        x = np.random.randint(w)
        seeds.append((y, x))
    
    # Grow regions from seeds
    for region_id, (seed_y, seed_x) in enumerate(seeds, start=1):
        queue = [(seed_y, seed_x)]
        seed_color = lab[seed_y, seed_x]
        visited = set()
        
        while queue and len(visited) < 5000:  # Limit region size
            y, x = queue.pop(0)
            
            if (y, x) in visited:
                continue
            
            if y < 0 or y >= h or x < 0 or x >= w:
                continue
            
            if segmented[y, x] != 0:
                continue
            
            # Check color similarity
            color_diff = np.linalg.norm(lab[y, x] - seed_color)
            
            if color_diff < threshold:
                segmented[y, x] = region_id
                visited.add((y, x))
                
                # Add neighbors to queue
                queue.extend([(y-1, x), (y+1, x), (y, x-1), (y, x+1)])
    
    # Create colored output
    output = np.zeros_like(image)
    colors = np.random.randint(0, 256, (num_seeds + 1, 3), dtype=np.uint8)
    colors[0] = [128, 128, 128]  # Gray for unsegmented regions
    
    for i in range(h):
        for j in range(w):
            output[i, j] = colors[segmented[i, j]]
    
    return output