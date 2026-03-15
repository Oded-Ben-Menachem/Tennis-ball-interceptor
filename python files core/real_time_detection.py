import cv2
import numpy as np
from data_process import real_time_process
import joblib
import time
from manage_camera_stream import CameraStream
import os
from dotenv import load_dotenv




# Get the absolute path of the directory where this script is located
base_dir = os.path.dirname(os.path.abspath(__file__))
#model_path = os.path.join(base_dir, 'tennis_ball_recognize.pkl')

# Build the full path to the model file located inside the 'samples' folder
model_path = os.path.join(os.path.dirname(__file__), 'samples', 'tennis_ball_recognize.pkl')
#print(model_path)

# Check if the model file actually exists at the specified location
if os.path.exists(model_path):
    # Load the pre-trained model using joblib
    model = joblib.load(model_path)
    #print(f"Model loaded successfully from: {model_path}")
else:
    # Stop the program and show an error if the file is missing
    raise FileNotFoundError(f"Could not find the model at: {model_path}. Make sure the .pkl file is in the same folder as this script.")


# 1. Initialize System
load_dotenv()
camera_ip = os.getenv("SERVER_IP")
cap = CameraStream(camera_ip)
avg_bg = None 
alpha = 0.05 # Learning rate for the LPF background model

print("System Initialized. Press 'q' to stop.")

while True:
    in_start = time.perf_counter()
    # 2. Capture Frame
    in_c1 = time.perf_counter()
    frame = cap.read()
    in_c2 = time.perf_counter()
    if frame is None: break

    # 3. Pre-processing (Signal Conditioning)
    # Gray scale and Blur to reduce high-frequency noise
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # 4. Background Model Update (The Memory)
    if avg_bg is None:
        avg_bg = gray.copy().astype("float")
        continue
    
    # Update: B = (1-a)B + aF
    cv2.accumulateWeighted(gray, avg_bg, alpha)
    
    # 5. Innovation Extraction (The Subtraction)
    # Difference between current frame and the 'slow' background
    diff = cv2.absdiff(gray, cv2.convertScaleAbs(avg_bg))

    # 6. Digitization (Thresholding)
    # Convert differences to binary mask (0 or 255)
    _, thresh = cv2.threshold(diff, 15, 255, cv2.THRESH_BINARY)
    in1 = time.perf_counter()
    # 7. Spatial Analysis (Finding the Ball)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    in2 = time.perf_counter()
    if contours:
            # 8. Data Extraction (Centroid calculation)
        for obj in contours:
            obj_length = len(obj)
            if obj_length < 35 or obj_length > 500:
                continue
            in3 = time.perf_counter()
            
            real_time_feature = real_time_process(obj)
            
            #prediction = model.predict(real_time_feature)

            probs = model.predict_proba(real_time_feature) 
            ball_probability = probs[0][1]
            #print(f'ball probability: {ball_probability}')

            in4 = time.perf_counter()
            #prediction = 'T'
            #print(f'contours: {in2-in1}, prediction: {in4-in3}')
            #if prediction == 'T':
            
            if ball_probability > 0.9:
                print(f'ball probability: {ball_probability}')
                M = cv2.moments(obj)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])

                    print(f"TRACKING: X={cX}, Y={cY}")

                    # Visual feedback
                    cv2.circle(frame, (cX, cY), 7, (0, 0, 255), -1)
                    x, y, w, h = cv2.boundingRect(obj)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # 9. Visualization
    cv2.imshow("Main Feed", frame)
    #cv2.imshow("Motion Mask (Binary)", thresh)

    if cv2.waitKey(1) & 0xFF == ord('q'): break
    in_end = time.perf_counter()
    #print(f'all process: {in_end-in_start}')
    #print(f'check now: {in_c2-in_c1}')
cap.release()
cv2.destroyAllWindows()