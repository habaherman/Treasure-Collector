# HERMAN IDD BASAJJABALABA 
# STUDENT # 201766954
# STUDENT PROPOSED PROJECT : ECO GAME


import sys 
from pygame.locals import *  # Import all constants and functions from pygame.locals
from os import listdir  # Import listdir to list files in a directory
from os.path import isfile, join  # Import isfile and join for file path operations
import pygame  # Import the Pygame library

pygame.init()  # Initialize all Pygame modules
pygame.mixer.pre_init(44100, -16, 2, 512)  # Pre-initialize the mixer for sound

# Game variables
WIDTH, HEIGHT = 1000, 650  # Set window dimensions
FPS = 60  # Frames per second for the game loop
player_speed = 5  # Player movement speed
main_menu = 0  # Variable for main menu state
score = 0  # Initialize score
player_health = 300  # Player's starting health
block_size = 98  # Size of blocks in the game

# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Eco Game')  # Set the title of the window

# Define font styles
font = pygame.font.SysFont('Bauhaus 93', 70)  # Main font for larger text
font_score = pygame.font.SysFont('Bauhaus 93', 30)  # Font for score display

# Load images
exit_img = pygame.image.load('assets/objects/exit.png')  # Load exit image
coin = pygame.image.load('assets/objects/coin.png')  # Load coin image

# Load sounds
pygame.mixer.music.load('assets/sound/music.wav')  # Load background music
pygame.mixer.music.play(-1, 0.0, 5000)  # Play background music in a loop
coin_fx = pygame.mixer.Sound('assets/sound/img_coin.wav')  # Load coin collection sound
coin_fx.set_volume(0.5)  # Set volume for coin sound effect
jump_fx = pygame.mixer.Sound('assets/sound/img_jump.wav')  # Load jump sound
jump_fx.set_volume(0.5)  # Set volume for jump sound effect
game_over_fx = pygame.mixer.Sound('assets/sound/img_game_over.wav')  # Load game over sound
game_over_fx.set_volume(0.5)  # Set volume for game over sound effect
exit_game_fx = pygame.mixer.Sound('assets/sound/exit_game.wav')  # Load exit game sound
exit_game_fx.set_volume(0.5)  # Set volume for exit game sound effect

# Define colors
red = (255, 0, 0)  # Define the color red
green = (0, 135, 81)  # Define a green color

def flip(sprites):
    """Flip the sprite images horizontally."""
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    """Load sprite sheets from the specified directory and return a dictionary of sprites."""
    path = join("assets", dir1, dir2)  # Construct the path to the sprite sheet directory
    images = [f for f in listdir(path) if isfile(join(path, f))]  # List all files in the directory
    
    all_sprites = {}  # Dictionary to hold all sprites
    
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()  # Load each sprite sheet
        
        sprites = []  # List to hold individual sprites
        for i in range(sprite_sheet.get_width() // width):  # Iterate over the sprite sheet width
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)  # Create a new surface for each sprite
            rect = pygame.Rect(i * width, 0, width, height)  # Define the area of the sprite
            surface.blit(sprite_sheet, (0, 0), rect)  # Blit the sprite onto the surface
            sprites.append(pygame.transform.scale2x(surface))  # Scale the sprite and add to the list
            
        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites  # Add right-facing sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)  # Add left-facing sprites
        else:
            all_sprites[image.replace(".png", "")] = sprites  # Add non-directional sprites
    
    return all_sprites  # Return the dictionary of loaded sprites

def draw_main_menu(window):
    """Draw the main menu and handle input for starting or quitting the game."""
    while True:
        window.fill((0, 0, 0))  # Clear the screen with black
        title_surface = font.render("Eco Game", True, (255, 255, 255))  # Render the title
        start_surface = font_score.render("Press ENTER to Start", True, (255, 255, 255))  # Render start text
        exit_surface = font_score.render("Press Q to Quit", True, (255, 255, 255))  # Render exit text

        # Center the text
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        start_rect = start_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        exit_rect = exit_surface.get_rect(center=(WIDTH // 2, HEIGHT * 3 // 4))

        # Draw the title and options on the window
        window.blit(title_surface, title_rect)
        window.blit(start_surface, start_rect)
        window.blit(exit_surface, exit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit Pygame if the window is closed
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start the game
                    return  # Exit menu to start the game
                elif event.key == pygame.K_q:  # Quit the game
                    pygame.quit()  # Quit Pygame if 'Q' is pressed
                    return

        pygame.display.flip()  # Update the display with drawn content
        pygame.time.Clock().tick(FPS)  # Control the frame rate

def load_block(size):
    """Load a block image from the tileset."""
    path = join("assets", "tileset", "terrain.png")  # Path to the terrain image
    image = pygame.image.load(path).convert_alpha()  # Load the terrain image
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)  # Create a surface for the block
    rect = pygame.Rect(272, 64, size, size)  # Defines the coordinates of the desired block in the terrain image
    surface.blit(image, (0, 0), rect)  # Blit the terrain image onto the surface
    return pygame.transform.scale2x(surface)  # Scale the block and return

def Level1_maze(block_size, height):
    """Generate a list of blocks for Level 1 in a maze-like pattern."""
    blocks = [
        Block(0, height - block_size * 6, block_size),  # Elevated starting block
        Block(-1, height - block_size * 6, block_size),  # Block slightly off-screen
        Block(block_size * 2, height - block_size * 4, block_size),  # Lower block
        Block(block_size * 4, height - block_size * 2, block_size),  # Near-ground block
        Block(block_size * 6, height - block_size * 3, block_size),  # Mid-height block
        Block(block_size * 8, height - block_size * 5, block_size),  # Higher block
        Block(block_size * 10, height - block_size * 6, block_size),  # Further elevated block
        Block(block_size * 12, height - block_size * 3, block_size),  # Floating block for jump challenge
        Block(block_size * 14, height - block_size * 5, block_size),  # Another floating block
        Block(block_size * 16, height - block_size * 7, block_size),  # Yet another floating block
        Block(block_size * 18, height - block_size, block_size),  # Lower final block
        Block(block_size * 20, height - block_size * 4, block_size)  # Mid-height block
    ]
    return blocks  # Return the list of blocks

def draw_health_bar(player):
    """Draw the player's health bar on the window."""
    bar_width = 250  # Width of the health bar
    bar_height = 10  # Height of the health bar
    health_ratio = player.current_health / player.max_health  # Ratio of current health to max health
    
    # Calculate position for the health bar (top right corner)
    x_position = WIDTH - bar_width - 10  # Right-aligned position
    y_position = 10  # Top position

    # Draw the background of the health bar
    pygame.draw.rect(window, (red), (10, 10, bar_width, bar_height))  # Red background
    # Draw the current health in green
    pygame.draw.rect(window, (    green), (10, 10, bar_width * health_ratio, bar_height))  # Green health bar
    # Create a font object for health display
    font = pygame.font.SysFont('Arial', 20)  # You can change the font and size as needed
    # Render the health text
    health_text = f'Health: {player.current_health}/{player.max_health}'  # Format the health text
    text_surface = font.render(health_text, True, (255, 255, 255))  # Create a surface for the health text
    text = text_surface.get_rect(center=(x_position + bar_width // 2, y_position + bar_height // 2))  # Center the text

def draw_score(window, score):
    """Draw the player's score on the window."""
    font = pygame.font.SysFont('Arial', 24)  # Define font for the score display
    score_surface = font.render(f'Score: {score}', True, (255, 255, 255))  # Render the score text
    window.blit(score_surface, (20, 20))  # Draw score in the top-left corner of the window

class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)  # Color for the player (not used in the current implementation)
    GRAVITY = 1  # Gravity effect
    SPRITES = load_sprite_sheets("MainCharacters", "MaskDude", 32, 32, True)  # Load player sprite sheets
    anime_delay = 3  # Delay for sprite animation
    
    def __init__(self, x, y, width, height):
        super().__init__()  # Initialize the parent class
        self.start_x = x  # Store the starting x position
        self.start_y = y  # Store the starting y position
        self.rect = pygame.Rect(x, y, width, height)  # Create a rectangle for player position
        self.x_vel = 0  # Horizontal velocity
        self.y_vel = 0  # Vertical velocity
        self.mask = None  # Mask for collision detection
        self.direction = "left"  # Initial direction
        self.current_health = 300  # Starting health
        self.max_health = 300  # Maximum health
        self.animation_count = 0  # Animation frame counter
        self.fall_count = 0  # Count for falling
        self.jumpcount = 0  # Count for jumps
        self.hit = False  # Flag for hit state
        self.hit_count = 0  # Count for hit state

    def jump(self):
        """Make the player jump."""
        self.y_vel = -self.GRAVITY * 8  # Set upward velocity
        self.animation_count = 0  # Reset animation count
        self.jumpcount += 1  # Increment jump count
        if self.jumpcount == 1:  # Reset fall count for first jump
            self.fall_count = 0
        jump_fx.play()  # Play jump sound

    def move(self, dx, dy):
        """Move the player by dx and dy."""
        self.rect.x += dx  # Update x position
        self.rect.y += dy  # Update y position

    def reset(self):
        """Reset player position and health."""
        self.rect.x = self.start_x  # Reset to starting x position
        self.rect.y = self.start_y  # Reset to starting y position
        self.current_health = self.max_health  # Reset health to max

    def make_hit(self):
        """Register a hit on the player."""
        self.hit = True  # Set hit flag

    def move_left(self, vel):
        """Move the player to the left."""
        self.x_vel = -vel  # Set horizontal velocity to the left
        if self.direction != "left":
            self.direction = "left"  # Update direction
            self.animation_count = 0  # Reset animation count

    def move_right(self, vel):
        """Move the player to the right."""
        self.x_vel = vel  # Set horizontal velocity to the right
        if self.direction != "right":
            self.direction = "right"  # Update direction
            self.animation_count = 0  # Reset animation count
            
    def loop(self, fps):
        """Update player state for each frame."""
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)  # Apply gravity
        self.move(self.x_vel, self.y_vel)  # Move the player
        
        if self.hit:
            self.hit_count += 1  # Increment hit count if hit
        if self.hit_count > fps * 2:  # Reset hit after 2 seconds
            self.hit = False
            self.hit_count = 0
        
        self.fall_count += 1  # Increment fall count
        self.update_sprite()  # Update sprite based on current state
        
    def land(self):
        """Handle landing on a surface."""
        self.fall_count = 0  # Reset fall count
        self.y_vel = 0  # Reset vertical velocity
        self.jumpcount = 0  # Reset jump count
        
    def hit_head(self):
        """Handle hitting a ceiling."""
        self.count = 0  # Reset count
        self.y_vel *= -1  # Reverse vertical velocity
    
    def collide_with_fire(self):
        """Apply fire damage to the player."""
        fire_damage = 5  # Damage amount
        self.current_health -= fire_damage  # Decrease health
        
    def update_sprite(self):
        """Update the player's sprite based on movement and actions."""
        sprite_sheet = "idle"  # Default sprite sheet
        if self.hit:
            sprite_sheet = "hit"  # Use hit sprite if hit
        if self.y_vel < 0:    
            if self.jumpcount == 1:
                sprite_sheet = "jump"  # Use jump sprite for first jump
            elif self.jumpcount == 2:
                sprite_sheet = "flip"  # Use flip sprite for second jump
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"  # Use fall sprite if falling
        elif self.x_vel != 0:
            sprite_sheet = "run"  # Use run sprite if moving
            
        sprite_sheet_name = sprite_sheet + "_" + self.direction  # Determine sprite based on direction
        sprites = self.SPRITES[sprite_sheet_name]  # Get sprites for current action
        sprite_index = (self.animation_count // self.anime_delay) % len(sprites)  # Get current sprite index
        self.sprite = sprites[sprite_index]  # Set the current sprite
        self.animation_count += 1  # Increment animation count
        self.update()  # Update the player rectangle
        
    def update(self):
        """Update the player's rectangle and mask for collision detection."""
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))  # Update rect position
        self.mask = pygame.mask.from_surface(self.sprite)  # Create mask for collision detection
         
    def draw(self, win, offset_x, offset_y):
        """Draw the player on the window."""
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))  # Blit player sprite on window

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()  # Initialize the parent class
        self.rect = pygame.Rect(x, y, width, height)  # Create rectangle for the object
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # Create a surface for the object
        self.width = width  # Store width
        self.height = height  # Store height
        self.name = name  # Store name (for identification)

    def draw(self, win, offset_x, offset_y):
        """Draw the object on the window."""
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))  # Blit object image

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)  # Initialize as a square block
        block = load_block(size)  # Load block image
        self.image.blit(block, (0, 0))  # Blit block image onto the surface
        self.mask = pygame.mask.from_surface(self.image)  # Create mask for collision detection

class Coin(Object):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20, "coin")  # Set size for the coin
        self.image = coin  # Load the coin image
        self.rect = self.image.get_rect(topleft=(x, y))  # Set the position of the coin
        self.original_y = y  # Store the original vertical position for movement
        self.direction = 1  # 1 for moving down, -1 for moving up
        self.amplitude = 8  # Amplitude of the up and down movement

    def update(self):
        """Update the coin's position to create up and down movement."""
        self.rect.y += self.direction  # Move the coin
        if self.rect.y >= self.original_y + self.amplitude:  # Change direction if it exceeds the amplitude
            self.direction = -1  # Change direction to up
        elif self.rect.y <= self.original_y - self.amplitude:  # Change direction if it goes below the original position
            self.direction = 1  # Change direction to down
            
    def draw(self, win, offset_x, offset_y):
        """Draw the coin on the window."""
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))  # Blit coin image on window

class Fire(Object):
    anime_delay = 3  # Delay for fire animation
    
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")  # Initialize the fire object
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)  # Load fire sprites
        self.image = self.fire["on"][0]  # Set the initial fire image
        self.mask = pygame.mask.from_surface(self.image)  # Create mask for collision detection
        self.animation_count = 0  # Animation frame counter
        self.animation_name = "on"  # State of fire (on)
        
    def on(self):
        """Turn the fire on."""
        self.animation_name = "on"
    
    def loop(self):
        """Update the fire animation."""
        sprites = self.fire[self.animation_name]  # Get the sprites for the current animation state
        sprite_index = (self.animation_count // self.anime_delay) % len(sprites)  # Get current sprite index
        self.image = sprites[sprite_index]  # Update the image to the current sprite
        self.animation_count += 1  # Increment animation count

        # Update rectangle and mask for the fire object
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.anime_delay > len(sprites):
            self.animation_count = 0  # Reset animation count if it exceeds the number of sprites

class Exit(Object):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, "exit")  # Initialize the exit object
        self.image = exit_img  # Set the exit image

def get_background(name):
    """Load the background image and return its tile positions."""
    image = pygame.image.load(join("assets", "Background", name))  # Load the background image
    _, _, width, height = image.get_rect()  # Get dimensions of the background image
    tiles = []  # List to hold tile positions
     
    for i in range(WIDTH // width + 1):  # Loop through the width of the window
        for j in range(HEIGHT // height + 1):  # Loop through the height of the window
            pos = [i * width, j * height]  # Calculate tile position
            tiles.append(pos)  # Add position to the list
            
    return tiles, image  # Return the list of tile positions and the background image

def draw(window, background, bg_image, player, objects, exit_obj, coins, score, offset_x, offset_y):
    """Draw all game elements on the window."""
    for tile in background:
        window.blit(bg_image, tile)  # Draw the background tiles
        
    for obj in objects:
        obj.draw(window, offset_x, offset_y)  # Draw each game object
        
    player.draw(window, offset_x, offset_y)  # Draw the player
    exit_obj.draw(window, offset_x, offset_y)  # Draw the exit
    draw_health_bar(player)  # Draw the player's health bar
    
    # Draw each coin
    for coin in coins:
        coin.draw(window, offset_x, offset_y)  # Draw each coin on the window
    
    draw_score(window, score)  # Display the score
    pygame.display.update()  # Update the display with drawn content

def handle_downward_collision(player, objects, dy):
    """Handle collisions when the player moves downwards."""
    collided_objects = []  # List to hold collided objects
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):  # Check for collision
            if dy > 0:  # Moving down
                player.rect.bottom = obj.rect.top  # Place player on top of the object
                player.land()  # Handle landing logic
            elif dy < 0:  # Moving up
                player.rect.top = obj.rect.bottom  # Place player below the object
                player.hit_head()  # Handle hitting head logic
                
            collided_objects.append(obj)  # Add collided object to the list
        
    return collided_objects  # Return the list of collided objects

def collide(player, objects, dx):
    """Check for collisions when moving the player."""
    player.move(dx, 0)  # Move player horizontally
    player.update()  # Update player's rectangle
    collided_object = None  # Variable to hold collided object
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):  # Check for collision
            collided_object = obj  # Set collided object
            break
        
    player.move(-dx, 0)  # Move player back to original position
    player.update()  # Update player's rectangle again
    return collided_object  # Return the collided object

def handle_move(player, objects):
    """Handle player movement based on keyboard input."""
    keys = pygame.key.get_pressed()  # Get the state of all keyboard keys
    
    player.x_vel = 0  # Reset horizontal velocity
    collide_left = collide(player, objects, -player_speed * 2)  # Check collision moving left
    collide_right = collide(player, objects, player_speed * 2)  # Check collision moving right
    
    if keys[pygame.K_LEFT] and not collide_left:  # Move left if the left key is pressed and no collision
        player.move_left(player_speed)
    if keys[pygame.K_RIGHT] and not collide_right:  # Move right if the right key is pressed and no collision
        player.move_right(player_speed)
        
    downward_collision = handle_downward_collision(player, objects, player.y_vel)  # Handle downward collisions
    check = [collide_left, collide_right, *downward_collision]  # Check all collision states
    
    for obj in check:
        if obj and obj.name == "fire":  # Check if the player collided with fire
            player.make_hit()  # Mark the player as hit
            health_loss = 20  # Set the health loss amount
            player.current_health -= health_loss  # Reduce player's health

def show_game_over_menu(window, score):
    """Display the game over menu and handle user input."""
    while True:
        window.fill((0, 0, 0))  # Clear the screen with black
        game_over_surface = font.render("Game Over", True, (255, 255, 255))  # Render the game over text
        score_surface = font_score.render(f'Final Score: {score}', True, (255, 255, 255))  # Render final score
        restart_surface = font_score.render("Press R to Restart", True, (255, 255, 255))  # Render restart option
        exit_surface = font_score.render("Press Q to Quit", True, (255, 255, 255))  # Render quit option

        # Center the text
        game_over_rect = game_over_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        score_rect = score_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        restart_rect = restart_surface.get_rect(center=(WIDTH // 2, HEIGHT * 3 // 4))
        exit_rect = exit_surface.get_rect(center=(WIDTH // 2, HEIGHT * 5 // 6))

        # Blit the rendered surfaces onto the window
        window.blit(game_over_surface, game_over_rect)
        window.blit(score_surface, score_rect)
        window.blit(restart_surface, restart_rect)
        window.blit(exit_surface, exit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Handle quit event
                pygame.quit()
                return
            
            if event.type == pygame.KEYDOWN:  # Handle key presses
                if event.key == pygame.K_r:  # Restart the game if 'R' is pressed
                    return  # Exit the game over menu to restart
                elif event.key == pygame.K_q:  # Quit the game if 'Q' is pressed
                    pygame.quit()
                    return

        pygame.display.flip()  # Update the display with drawn content
        pygame.time.Clock().tick(FPS)  # Control the frame rate

def cleanup():
    """Cleanup resources and quit Pygame."""
    pygame.mixer.quit()  # Stop the mixer
    pygame.quit()  # Uninitialize all Pygame modules
    sys.exit()  # Exit the program

def main(window):
    """Main game loop and setup."""
    clock = pygame.time.Clock()  # Create a clock to control the frame rate
    # Show the main menu
    draw_main_menu(window)
    
    background, bg_image = get_background("plx-1.png")  # Load background image and its tile positions
    
    block_size = 96  # Set block size
    
    
    # Initialize player, fire objects and the exit
    player = Player(50, 50, 25, 25)
    fire = Fire(100, HEIGHT - block_size - 64, 16, 32)
    fire.on()
    floor = [Block(i * block_size, HEIGHT - block_size, block_size) 
             for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    
    maze_blocks = Level1_maze(block_size, HEIGHT)  # Assumes Level1_maze returns a list of Block objects
    objects = [*floor, *maze_blocks, fire]  # Combine floor and maze blocks
    exit_obj = Exit(WIDTH - 100, HEIGHT - block_size - 50)  # Create the exit object
    
    
    # Create a list to hold coin objects
     # Create coins positioned on blocks
    coins = []
    for block in maze_blocks:
        coin_x = block.rect.x + (block_size // 4)  # Centered on the block
        coin_y = block.rect.y - 30  # Positioned above the block
        coins.append(Coin(coin_x, coin_y))  # Create and store the coin
    
    # Scrolling variables
    offset_x = 0
    offset_y = 0
    scroll_area_width = 200
    scroll_area_height = 150


    score = 0
    run = True
    while run:
        
        clock.tick(FPS)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player.jumpcount < 2:
                    player.jump()
        

        player.loop(FPS)
        fire.loop()
        handle_move(player, objects)
        
        for coin in coins:
            coin.update()  # Update the position of each coin

        draw(window, background, bg_image, player, objects, exit_obj, coins, score, offset_x, offset_y)
        
        # Drawing coins
        for coin in coins:
            coin.draw(window, 0, 0)  # Draw coins on the window
        
         # Check for collisions with coins
        for coin in coins[:]:  # Iterate over a copy of the list
            if player.rect.colliderect(coin.rect):  # Check for collision
                coins.remove(coin)
                score += 5
                coin_fx.play()
        
        # Check for game over conditions
        if player.current_health <= 0:
            pygame.mixer.music.stop()
            game_over_fx.play()
            show_game_over_menu(window, score)
            player.reset()
            score = 0  # Reset score when restarting the game
            coins = []  # Reset coins
            for block in maze_blocks:  # Reinitialize coins
                    coin_x = block.rect.x + (block_size // 4)
                    coin_y = block.rect.y - 30
                    coins.append(Coin(coin_x, coin_y))
            offset_x = 0
            offset_y = 0
            pygame.mixer.music.play(-1, 0.0, 5000)
        elif player.rect.colliderect(exit_obj.rect):
            pygame.mixer.music.stop()
            exit_game_fx.play()
            show_game_over_menu(window, score)
            player.reset()  # Reset the player to starting position and health
            score = 0  # Reset score when restarting the game
            coins = []  # Reset coins
            for block in maze_blocks:  # Reinitialize coins
                    coin_x = block.rect.x + (block_size // 4)
                    coin_y = block.rect.y - 30
                    coins.append(Coin(coin_x, coin_y))
            offset_x = 0
            offset_y = 0
            if pygame.mixer.get_init():
                pygame.mixer.music.play(-1, 0.0, 5000)  # Resume background music
        
        # Update scrolling offsets based on player position
        if (player.rect.right - offset_x >= WIDTH - scroll_area_width and player.x_vel > 0) or (
            player.rect.left - offset_x <= scroll_area_width and player.x_vel < 0):
            offset_x += player.x_vel
            
        if (player.rect.bottom - offset_y >= HEIGHT - scroll_area_height and player.y_vel > 0) or (
            player.rect.top - offset_y <= scroll_area_height and player.y_vel < 0):
            offset_y += player.y_vel
        
    if pygame.mixer.get_init():  # Ensure mixer is initialized before quitting
        pygame.mixer.music.stop()  # Stop any music before quitting
        
    pygame.quit()
    quit()
    cleanup()

        
if __name__ == "__main__":
    main(window) 