import sys
import subprocess

# פקודה להתקנה ישירות לתוך ה-Interpreter הנוכחי
subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python"])

import cv2
print("הצלחה! גרסת OpenCV היא:", cv2.__version__)