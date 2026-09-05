import cv2
import numpy as np

def load_templates():
    # Load template images for matching
    templates = {
        'white_coin': cv2.imread('./assets/white_coin.png', cv2.IMREAD_GRAYSCALE),
        'black_coin': cv2.imread('./assets/black_coin.png', cv2.IMREAD_GRAYSCALE),
        'queen': cv2.imread('./assets/queen.png', cv2.IMREAD_GRAYSCALE),
        'striker': cv2.imread('./assets/striker.png', cv2.IMREAD_GRAYSCALE)
    }
    return templates

def detect_objects(frame, templates, threshold=0.8):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detected_objects = {}

    for name, template in templates.items():
        if template is None:
            continue
            
        h, w = template.shape[:2]
        res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        
        objects = []
        # Non-max suppression or basic point collection
        for pt in zip(*loc[::-1]):
            objects.append({'x': pt[0] + w // 2, 'y': pt[1] + h // 2})
            
        detected_objects[name] = objects

    return detected_objects