import os
import random
import time

# 1. ENVIRONMENT SETUP
# 0 = Empty space, -1 = Trap (Game Over), 10 = Treasure (Win)
GRID = [
    [0, 0, 0, -1],
    [0, -1, 0, 0],
    [0, 0, 0, -1],
    [0, -1, 0, 10]
]
ROWS, COLS = len(GRID), len(GRID[0])
ACTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT']

# Q-Table: Stores the AI's "memory" of how good each action is at each (row, col)
q_table = {(r, c): {a: 0.0 for a in ACTIONS} for r in range(ROWS) for c in range(COLS)}

# 2. AI HYPERPARAMETERS (Students: Tweak these!)
LEARNING_RATE = 0.1     # How fast the AI overwrites old knowledge (0.0 to 1.0)
DISCOUNT_FACTOR = 0.9   # How much the AI cares about future rewards vs. immediate ones
EPSILON = 1.0           # Exploration rate: 0.5 means 50% random moves, 50% smart moves
EPISODES = 200          # Number of practice games

def get_next_position(r, c, action):
    if action == 'UP':    r = max(0, r - 1)
    elif action == 'DOWN':  r = min(ROWS - 1, r + 1)
    elif action == 'LEFT':  c = max(0, c - 1)
    elif action == 'RIGHT': c = min(COLS - 1, c + 1)
    return r, c

def print_board(agent_r, agent_c, step_num=0, last_action="START"):
    # Clears the terminal screen (works on Windows 'nt' and Mac/Linux 'posix')
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"Step: {step_num} | Last Move: {last_action}\n")
    for r in range(ROWS):
        row_display = []
        for c in range(COLS):
            if r == agent_r and c == agent_c:
                # Show explosion or celebration if agent landed on trap/treasure
                if GRID[r][c] == -1:
                    row_display.append("💥")
                elif GRID[r][c] == 10:
                    row_display.append("🥳")
                else:
                    row_display.append("🤖")
            elif GRID[r][c] == -1:
                row_display.append("💣")
            elif GRID[r][c] == 10:
                row_display.append("💎")
            else:
                row_display.append("⬜")
        print(" ".join(row_display))
    print()

# 3. TRAINING LOOP
print("Training AI...")
for episode in range(EPISODES):
    r, c = 0, 0  # Always start at top-left
    steps = 0
    
    while steps < 50:  # Prevent infinite loops
        # Decide: Explore (random) or Exploit (use Q-table)?
        if random.uniform(0, 1) < EPSILON:
            action = random.choice(ACTIONS)
        else:
            action = max(q_table[(r, c)], key=q_table[(r, c)].get)
            
        next_r, next_c = get_next_position(r, c, action)
        reward = GRID[next_r][next_c]
        
        # Q-Learning Formula (Updating the AI's brain)
        old_value = q_table[(r, c)][action]
        next_max = max(q_table[(next_r, next_c)].values())
        
        new_value = old_value + LEARNING_RATE * (reward + DISCOUNT_FACTOR * next_max - old_value)
        q_table[(r, c)][action] = new_value
        
        r, c = next_r, next_c
        steps += 1
        
        if reward == 10 or reward == -1:  # Hit treasure or trap
            break

# 4. WATCH THE TRAINED AI PLAY
r, c = 0, 0
print_board(r, c, step_num=0, last_action="READY")
time.sleep(1.0)

for step in range(1, 16):
    action = max(q_table[(r, c)], key=q_table[(r, c)].get)
    r, c = get_next_position(r, c, action)
    
    print_board(r, c, step_num=step, last_action=action)
    time.sleep(0.5)
    
    if GRID[r][c] == 10:
        print("🏆 AI found the treasure!")
        break
    elif GRID[r][c] == -1:
        print("💀 AI fell into a trap!")
        break
else:
    print("⏳ AI ran out of moves (got stuck in a loop)!")