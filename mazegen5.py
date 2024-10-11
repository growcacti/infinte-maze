import pygame
import random

# Initialize Pygame with double buffering
pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF)
clock = pygame.time.Clock()

# Maze settings
TILE_SIZE = 40
VISIBLE_TILES_X = 800 // TILE_SIZE
VISIBLE_TILES_Y = 600 // TILE_SIZE

# Player settings
PLAYER_SPEED = 5
PLAYER_SIZE = 30  # Size of the player

class Maze:
    def __init__(self):
        self.maze = {}  # Dictionary to store maze tiles

    def get_tile(self, x, y):
        if (x, y) not in self.maze:
            # Generate new tile (1 for wall, 0 for path)
            if random.random() < 0.2:  # 20% chance of being a wall
                self.maze[(x, y)] = 1
            else:
                self.maze[(x, y)] = 0
        return self.maze[(x, y)]

    def draw(self, camera_x, camera_y):
        # Draw visible part of the maze
        for y in range(-1, VISIBLE_TILES_Y + 1):
            for x in range(-1, VISIBLE_TILES_X + 1):
                maze_x = (camera_x // TILE_SIZE) + x
                maze_y = (camera_y // TILE_SIZE) + y
                tile = self.get_tile(maze_x, maze_y)
                if tile == 1:  # Draw wall
                    pygame.draw.rect(
                        screen, (255, 255, 255),
                        (x * TILE_SIZE - camera_x % TILE_SIZE,
                         y * TILE_SIZE - camera_y % TILE_SIZE,
                         TILE_SIZE, TILE_SIZE)
                    )

class Player:
    def __init__(self, x, y, maze):
        self.x = x
        self.y = y
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.maze = maze  # Reference to the maze for collision detection

    def can_move_to(self, new_x, new_y):
        # Calculate player's tile coordinates
        tile_x = new_x // TILE_SIZE
        tile_y = new_y // TILE_SIZE
        # Check all corners of the player's bounding box
        corners = [
            (tile_x, tile_y),  # Top-left
            (tile_x + self.size // TILE_SIZE, tile_y),  # Top-right
            (tile_x, tile_y + self.size // TILE_SIZE),  # Bottom-left
            (tile_x + self.size // TILE_SIZE, tile_y + self.size // TILE_SIZE),  # Bottom-right
        ]
        for corner in corners:
            if self.maze.get_tile(*corner) == 1:  # If any corner collides with a wall
                return False
        return True

    def move(self):
        keys = pygame.key.get_pressed()
        new_x, new_y = self.x, self.y

        if keys[pygame.K_LEFT]:
            new_x -= self.speed
        if keys[pygame.K_RIGHT]:
            new_x += self.speed
        if keys[pygame.K_UP]:
            new_y -= self.speed
        if keys[pygame.K_DOWN]:
            new_y += self.speed

        # Check for collision before moving
        if self.can_move_to(new_x, self.y):
            self.x = new_x
        if self.can_move_to(self.x, new_y):
            self.y = new_y

    def draw(self, camera_x, camera_y):
        # Draw the player
        pygame.draw.rect(
            screen, (0, 0, 255),
            (self.x - camera_x, self.y - camera_y, self.size, self.size)
        )

# Game setup
maze = Maze()
player = Player(400, 300, maze)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player movement
    player.move()

    # Update camera position
    camera_x = player.x - 400  # Half of screen width
    camera_y = player.y - 300  # Half of screen height

    # Fill screen (use the background color)
    screen.fill((0, 0, 0))

    # Draw maze and player
    maze.draw(camera_x, camera_y)
    player.draw(camera_x, camera_y)

    # Double buffering: Flip the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

pygame.quit()
