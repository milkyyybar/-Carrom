import subprocess

def swipe(x1, y1, x2, y2, duration_ms=200):
    cmd = ["adb", "shell", "input", "touchscreen", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration_ms)]
    subprocess.run(cmd, stdout=subprocess.DEVNULL)