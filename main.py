import time
from capture import capture_screen
from vision import load_templates, detect_objects
from physics import calculate_shot
from controller import swipe

# Approximate board pocket coordinates for a 1080x2400 layout
# (Top-Left, Top-Right, Bottom-Left, Bottom-Right, etc.)
POCKETS = [
    (150, 600),   # Top-Left
    (930, 600),   # Top-Right
    (150, 1800),  # Bottom-Left
    (930, 1800)   # Bottom-Right
]

def main():
    print("Loading assets...")
    templates = load_templates()
    
    print("Starting Carrom Automation Engine...")
    while True:
        start_time = time.time()
        
        # 1. Capture screen
        frame = capture_screen()
        if frame is None:
            print("Failed to capture screen. Retrying...")
            time.sleep(1)
            continue
            
        # 2. Detect game elements
        game_state = detect_objects(frame, templates)
        
        # 3. Calculate optimal trajectory
        shot = calculate_shot(game_state, POCKETS)
        
        # 4. Execute swipe command if valid shot found
        if shot:
            print(f"Executing shot: {shot}")
            swipe(shot['x1'], shot['y1'], shot['x2'], shot['y2'], duration_ms=300)
            # Wait for physics/animation to settle before next frame
            time.sleep(2.5)
        else:
            time.sleep(0.5)

if __name__ == "__main__":
    main()