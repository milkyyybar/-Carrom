import subprocess
import cv2
import numpy as np

def capture_screen():
    # Pull screenshot directly from Android device via ADB
    subprocess.run(["adb", "shell", "screencap", "-p", "/sdcard/screen.png"], stdout=subprocess.DEVNULL)
    subprocess.run(["adb", "pull", "/sdcard/screen.png", "./screen.png"], stdout=subprocess.DEVNULL)
    
    # Read image with OpenCV
    img = cv2.imread("./screen.png")
    return img