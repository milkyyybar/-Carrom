import math

def calculate_shot(game_state, pockets):
    """
    Calculates the required swipe vector to hit a target coin into a pocket.
    
    pockets: List of (x, y) coordinates for the board holes.
    game_state: Dictionary containing lists of detected coordinates for striker, coins, etc.
    """
    strikers = game_state.get('striker', [])
    white_coins = game_state.get('white_coin', [])
    
    if not strikers or not white_coins:
        return None

    striker_pos = (strikers[0]['x'], strikers[0]['y'])
    
    # Pick the first available white coin as the target (for prototype logic)
    target_coin = (white_coins[0]['x'], white_coins[0]['y'])
    
    # Pick a sample pocket (e.g., top-left pocket coordinates)
    target_pocket = pockets[0] 

    # 1. Vector from Target Coin to Pocket
    pocket_vector = (target_pocket[0] - target_coin[0], target_pocket[1] - target_coin[1])
    pocket_distance = math.hypot(pocket_vector[0], pocket_vector[1])
    
    if pocket_distance == 0:
        return None
        
    # Normalize pocket vector
    p_unit = (pocket_vector[0] / pocket_distance, pocket_vector[1] / pocket_distance)

    # 2. Account for coin radius offset (Ghost ball position)
    # The striker must hit the coin along the line opposite to the pocket vector
    coin_radius = 20  # Approximate pixel radius; adjust based on resolution
    ghost_x = target_coin[0] - (p_unit[0] * (coin_radius * 2))
    ghost_y = target_coin[1] - (p_unit[1] * (coin_radius * 2))

    # 3. Vector from Striker to Ghost Position
    strike_vector = (ghost_x - striker_pos[0], ghost_y - striker_pos[1])
    strike_distance = math.hypot(strike_vector[0], strike_vector[1])

    if strike_distance == 0:
        return None

    # 4. Generate swipe coordinates: Drag backward from striker to pull back power
    # Power scaling factor based on distance
    power_scale = min(strike_distance * 1.5, 500) 
    
    s_unit = (strike_vector[0] / strike_distance, strike_vector[1] / strike_distance)
    
    # Start touch at striker, pull back in the exact opposite direction of the shot vector
    start_x = striker_pos[0]
    start_y = striker_pos[1]
    
    end_x = striker_pos[0] - (s_unit[0] * power_scale)
    end_y = striker_pos[1] - (s_unit[1] * power_scale)

    return {
        'x1': int(start_x),
        'y1': int(start_y),
        'x2': int(end_x),
        'y2': int(end_y)
    }