import cv2
import time
from capture import capture_screen
from vision import load_templates, detect_objects
from physics import calculate_shot

# Sample pocket coordinates (adjust based on your resolution)
POCKETS = [
    (150, 600),   # Top-Left
    (930, 600),   # Top-Right
    (150, 1800),  # Bottom-Left
    (930, 1800)   # Bottom-Right
]

def main():
    templates = load_templates()
    print("Starting Debug Visualizer. Press 'q' to exit.")
    
    while True:
        frame = capture_screen()
        if frame is None:
            time.sleep(1)
            continue
            
        # Detect objects
        game_state = detect_objects(frame, templates, threshold=0.75)
        
        # Draw detected objects on the frame
        for name, objs in game_state.items():
            color = (0, 255, 0) if name == 'white_coin' else (0, 0, 255)
            if name == 'striker':
                color = (255, 0, 0)
            
            for obj in objs:
                cv2.circle(frame, (obj['x'], obj['y']), 15, color, 2)
                cv2.putText(frame, name, (obj['x'] - 20, obj['y'] - 20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        # Draw pockets
        for p in POCKETS:
            cv2.circle(frame, p, 20, (255, 255, 0), 2)

        # Calculate shot if possible
        shot = calculate_shot(game_state, POCKETS)
        if shot:
            # Draw swipe vector: start point (striker) to pull-back point
            cv2.arrowedLine(frame, (shot['x1'], shot['y1']), (shot['x2'], shot['y2']), (0, 255, 255), 3)

        # Resize for easy viewing on desktop monitor
        display_frame = cv2.resize(frame, (540, 1200))
        cv2.imshow("Carrom Bot Debug", display_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()