import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
clock = pygame.time.Clock()

# Tile and player settings
TILE_SIZE = 40
PLAYER_SIZE = 30

# Load images
wall_image = pygame.image.load('wall.png')
wall_image = pygame.transform.scale(wall_image, (TILE_SIZE, TILE_SIZE))
player_image = pygame.image.load('player.png')
player_image = pygame.transform.scale(player_image, (PLAYER_SIZE, PLAYER_SIZE))

# Maze class to handle the maze generation and rendering
class Maze:
    def __init__(self):
        self.tiles = {}  # Dictionary to store maze tiles

    def get_tile(self, x, y):
        if (x, y) not in self.tiles:
            # Generate new tile (1 for wall, 0 for path)
            if random.random() < 0.2:  # 20% chance of being a wall
                self.tiles[(x, y)] = 1
            else:
                self.tiles[(x, y)] = 0
        return self.tiles[(x, y)]

    def draw(self, camera_x, camera_y):
        for y in range(-1, SCREEN_HEIGHT // TILE_SIZE + 1):
            for x in range(-1, SCREEN_WIDTH // TILE_SIZE + 1):
                maze_x = (camera_x // TILE_SIZE) + x
                maze_y = (camera_y // TILE_SIZE) + y
                tile = self.get_tile(maze_x, maze_y)
                if tile == 1:  # Draw wall
                    screen.blit(
                        wall_image,
                        (x * TILE_SIZE - camera_x % TILE_SIZE,
                         y * TILE_SIZE - camera_y % TILE_SIZE)
                    )

# Player class to handle the player’s movement and rendering
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5

    def move(self, maze):
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

        if self.can_move_to(new_x, self.y, maze):
            self.x = new_x
        if self.can_move_to(self.x, new_y, maze):
            self.y = new_y

    def can_move_to(self, new_x, new_y, maze):
        tile_x = new_x // TILE_SIZE
        tile_y = new_y // TILE_SIZE
        corners = [
            (tile_x, tile_y),  # Top-left
            (tile_x + PLAYER_SIZE // TILE_SIZE, tile_y),  # Top-right
            (tile_x, tile_y + PLAYER_SIZE // TILE_SIZE),  # Bottom-left
            (tile_x + PLAYER_SIZE // TILE_SIZE, tile_y + PLAYER_SIZE // TILE_SIZE),  # Bottom-right
        ]
        for corner in corners:
            if maze.get_tile(*corner) == 1:  # If any corner collides with a wall
                return False
        return True

    def draw(self, camera_x, camera_y):
        screen.blit(
            player_image,
            (self.x - camera_x, self.y - camera_y)
        )

# Initialize maze and player
maze = Maze()
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the player and update camera position
    player.move(maze)
    camera_x = player.x - SCREEN_WIDTH // 2
    camera_y = player.y - SCREEN_HEIGHT // 2

    # Fill screen with background color
    screen.fill((0, 0, 0))

    # Draw the maze and player
    maze.draw(camera_x, camera_y)
    player.draw(camera_x, camera_y)

    # Double buffering: Flip the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

pygame.quit()
