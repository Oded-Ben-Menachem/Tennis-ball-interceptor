import cv2
import numpy as np
import os
from dotenv import load_dotenv

# 1. Initialize System
load_dotenv()
camera_ip = os.getenv("SERVER_IP")
cap = cv2.VideoCapture(camera_ip)
avg_bg = None 
alpha = 0.05 # Learning rate for the LPF background model

print("System Initialized. Press 'q' to stop.")
counter = 0
file_number = 1
while True:
    counter +=1
    if counter > 2000: break
    # 2. Capture Frame
    ret, frame = cap.read()
    if not ret: break

    # 3. Pre-processing (Signal Conditioning)
    # Gray scale and Blur to reduce high-frequency noise
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

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
    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    
    

    # 7. Spatial Analysis (Finding the Ball)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #print(contours)
    if contours:
        np.save(f'other_sample{file_number}', thresh)
        print(f'{file_number} saved')
        file_number +=1
        # Get the largest moving object to filter out noise
        largest_cnt = max(contours, key=cv2.contourArea)
        
        # Filter by physical size (SNR improvement)
        if cv2.contourArea(largest_cnt) > 1:
            # 8. Data Extraction (Centroid calculation)
            M = cv2.moments(largest_cnt)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                
                # FINAL OUTPUT: Send these to ESP32
                print(f"TRACKING: X={cX}, Y={cY}")

                # Visual feedback
                cv2.circle(frame, (cX, cY), 7, (0, 0, 255), -1)
                x, y, w, h = cv2.boundingRect(largest_cnt)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # 9. Visualization
    cv2.imshow("Main Feed", frame)
    cv2.imshow("Motion Mask (Binary)", thresh)

    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()