**For more info:** [Understanding Pac-Man Ghost Behavior](https://gameinternals.com/understanding-pac-man-ghost-behavior)

## GHOST BEHAVIOR

### Blinky (Red Ghost)
- Tends to chase directly behind Pac-Man
- Speed increases as fewer dots remain on the board
- Becomes more aggressive than the others when the number of dots left to eat decreases

### Pinky (Pink Ghost)
- Attempts to position itself in front of Pac-Man by using a 4 tiles offset in front of Pac-Man's current direction
- The ambush tactic is less effective in the corners

### Inky (Cyan Ghost)
- Movement is influenced by the position of both Pac-Man and Blinky, acting unpredictably
- His target tile is calculated with a combination of Pac-Man’s position and Blinky’s, making him the most unpredictable of the ghosts

### Clyde (Orange Ghost)
- Exhibits behavior that combines targeting Pac-Man like Blinky and escaping to the bottom left corner of the maze
- When Clyde is far from Pac-Man, he acts more like Blinky; when close, he tends to wander away towards his home corner

## GHOST MODES

### Chase Mode
- In 'Chase' mode, each ghost uses its unique algorithm to pursue Pac-Man
  - Blinky tries to directly chase down Pac-Man, aiming for his current tile
  - Pinky targets a point that is four tiles ahead of Pac-Man in the direction he is facing, aiming to cut him off
  - Inky uses a more complex method that involves the positions of both Blinky and Pac-Man, targeting a position by drawing a vector from Blinky to two tiles in front of Pac-Man and doubling that vector
  - Clyde toggles between chasing Pac-Man like Blinky and retreating to his home corner depending on his proximity to Pac-Man

### Scatter Mode
- In 'Scatter' mode, each ghost retreats to its respective home corner; this provides a timed break from the aggressive pursuit
  - Blinky heads to the top-right corner
  - Pinky goes to the top-left corner
  - Inky moves to the bottom-right corner
  - Clyde goes to the bottom-left corner

### Frightened Mode
- When Pac-Man eats a power pellet, all ghosts enter the 'Frightened' mode
  - In this mode, the ghosts turn blue and wander around the maze randomly. This is the only time they do not follow their unique or scatter behaviors
  - The ghosts move slower than usual, and their direction is chosen randomly at each intersection
  - Pac-Man can eat the ghosts for extra points during this mode. After being eaten, a ghost's eyes return to the ghost pen (the starting area), where it regenerates and resumes its normal behavior

## GHOST PROGRESSION

### Level Progression
- As levels progress, the duration of Frightened mode decreases, and the ghosts generally move faster (except when Frightened)

### Ghost Behavior and Timing
- Ghosts have specific timing patterns for switching between Scatter and Chase modes, and these become shorter as the game progresses

### Tunnels
- The side tunnels (or "warp tunnels") that connect the left and right sides of the screen cause Pac-Man and the ghosts slow down while passing through these tunnels

### Cornering
- When maneuvering around corners, Pac-Man can "cut corners" by turning just before he actually reaches the turn

### Ghost Release from the Pen
- Ghosts are initially confined in the central pen and begin to leave one by one

## PROJECT INFO

**Professor will ask:**
- What representation scheme we used
- What search scheme we used
    - Will ask what lines of code do the searching
