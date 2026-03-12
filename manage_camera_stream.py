import cv2
import threading

class CameraStream:
    def __init__(self,source = 0):
        self.caprure = cv2.VideoCapture(source)
        self.ret, self.frame = self.caprure.read()
        self.running = True
        # 1. Create a new thread object. 
        # 'target' points to the function you want to run in the background.
        # 'args' is empty because our function doesn't need extra inputs.
        self.thread = threading.Thread(target=self.update, args=())

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
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.frame = frame

    def read(self):
        return self.frame
    
    def stop(self):
        self.running = False
        self.caprure.release()
