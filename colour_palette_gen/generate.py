import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import MiniBatchKMeans
from pathlib import Path
import os



def plot_color_palette(palette, hist,output_dir,input_file):
    height = 200
    width = 600
    img = np.zeros((height + 30, width, 3), dtype=np.uint8)  # Increased height by 30 pixels

    total_pixels = np.sum(hist)
    start_x = 0

    for i, color in enumerate(palette):
        end_x = start_x + int((hist[i] / total_pixels) * width)
        img[:height, start_x:end_x] = color  # Fill color bar
        start_x = end_x

    # Add white strip at the bottom
    img[height:, :] = 255
    img = img[:,:end_x] 

    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    print("---output dir created at: ",output_dir)
    parent= os.path.splitext(os.path.basename(input_file))[0]  
    cv2.imwrite(os.path.join(output_dir , parent+'_colour_palette.jpg'), img)



def process_video(input_dir, batch_size=100, num_colors=5,output_dir="."):
    files=[]
    for dirname, _, filenames in os.walk(input_dir):
        for filename in filenames:
            if filename.endswith('.mp4') or filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
                files.append(os.path.join(dirname, filename))
    print("---files found: ",files)
    for i in files:
        print("---processing file: ",i)
        cap = cv2.VideoCapture(i)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        kmeans = MiniBatchKMeans(n_clusters=num_colors)
        
        for batch_start in range(0, frame_count, batch_size):
            frames = []
            cap.set(cv2.CAP_PROP_POS_FRAMES, batch_start)
            for _ in range(min(batch_size, frame_count - batch_start)):
                ret, frame = cap.read()
                if not ret:
                    break
                frame_resized = cv2.resize(frame, (width // 2, height // 2))
                frames.append(frame_resized.reshape(-1, 3))
            frames = np.concatenate(frames, axis=0)
            #print(frames)
            kmeans.partial_fit(frames)
            
        cap.release()
        
        hist, _ = np.histogram(kmeans.labels_, bins=np.arange(0, len(kmeans.cluster_centers_) + 1))
        sorted_indices = np.argsort(hist)[::-1]  # Sort indices based on frequency
        
        # Generate color palette
        palette = kmeans.cluster_centers_[sorted_indices].astype(int)
        hist = hist[sorted_indices]
        plot_color_palette(palette, hist,output_dir,i)
    




#sample
#process_video(input_dir="./examples", batch_size=100, num_colors=5,output_dir="./output_palettes")
