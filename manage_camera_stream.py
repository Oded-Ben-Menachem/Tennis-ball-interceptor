

import cv2
import threading
import time

class CameraStream:
    def __init__(self,source = 0):
        self.capture = cv2.VideoCapture(source)
        self.ret, frame = self.capture.read()
        self.frame = frame.copy() if self.ret else None
        self.running = True
        # 1. Create a new thread object. 
        # 'target' points to the function you want to run in the background.
        # 'args' is empty because our function doesn't need extra inputs.
        self.thread = threading.Thread(target=self.update)

        # 2. Set the thread as a 'daemon'. 
        # This means the thread will automatically close when your main script stops. 
        # Without this, the program might "hang" and stay open in the background.
        self.thread.daemon = True

        # 3. This actually starts the thread execution. 
        # The 'update' function will now begin running in parallel with your main code.
        self.thread.start()
        
    
    def update(self):
        # 4. This loop runs in its own separate "lane" (thread).
        # It continuously updates self.frame while the main loop does the math.
        #frame_counter = 0
        while self.running:
            #frame_counter += 1
            #print(f'frame number: {frame_counter}')
            ret, frame = self.capture.read()
            if ret:
                self.frame = frame.copy()
            time.sleep(0.01)
            

    def read(self):
        return self.frame
      
       
    
    def stop(self):
        self.running = False
        self.capture.release()
'''

import cv2
import threading
import time

class CameraStream:
    def __init__(self, src=0):
        self.src = src
        print(f"[DEBUG] Connecting to: {src}")
        self.cap = cv2.VideoCapture(self.src)
        
        if not self.cap.isOpened():
            print("[ERROR] Could not open video source!")
            
        self.ret, frame = self.cap.read()
        self.frame = frame.copy() if self.ret else None
        self.count = 0
        self.running = True
        
        
        self.thread = threading.Thread(target=self.update)
        self.thread.daemon = True
        print("[DEBUG] Starting Thread...")
        self.thread.start()

    def update(self):
        print("[DEBUG] Inside Update Thread - Loop Started")
        try:
            while self.running:
                ret, frame = self.cap.read()
                if ret:
                    self.frame = frame.copy()
                    self.count += 1
                else:
                    print("[WARNING] Thread failed to grab frame.")
                    # אם זו מצלמת IP, אולי היא התנתקה?
                    time.sleep(1) 
                
                # השהייה קטנה כדי לראות אם זה עוזר
                time.sleep(0.01)
        except Exception as e:
            print(f"[CRITICAL ERROR] Thread crashed: {e}")

    def read(self):
        return self.frame, self.count

    def stop(self):
        self.running = False
        self.cap.release()
'''
'''
cap = CameraStream("http://192.168.1.157:8080/video")
frame_id = 0
while True:
    frame = cap.read()
    print(f"Main loop sees Frame ID: {frame_id}")

    if frame is not None:
        cv2.imshow("Test", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
'''