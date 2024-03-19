import pygame
import sys

# Initialize the game engine
pygame.init()

# Set the height and width of the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])

# Set the name of the window
pygame.display.set_caption("Platformer with Jump and Camera")

# Set colors
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
black = (0, 0, 0)
pink = (255, 182, 193)  # Rose color

# Set gravity
gravity = 1

class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50

        self.velocity_y = 0
        self.on_ground = False

    def update(self):
        # Apply gravity
        self.velocity_y += gravity

        # Move the player along the y-axis
        self.rect.y += self.velocity_y

        # Check if the player is on the ground
        if self.rect.y >= screen_height - self.rect.height:
            self.rect.y = screen_height - self.rect.height
            self.velocity_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

    def jump(self):
        if self.on_ground:
            self.velocity_y = -15  # Adjust the jump height as needed

class Platform(pygame.sprite.Sprite):
    def __init__(self, color, rect):
        super().__init__()

        self.image = pygame.Surface([rect.width, rect.height])
        self.image.fill(color)

        self.rect = rect

class RestartBlock(pygame.sprite.Sprite):
    def __init__(self, color, rect):
        super().__init__()

        self.image = pygame.Surface([rect.width, rect.height])
        self.image.fill(color)

        self.rect = rect

class MovingBlock(pygame.sprite.Sprite):
    def __init__(self, color, rect, speed):
        super().__init__()

        self.image = pygame.Surface([rect.width, rect.height])
        self.image.fill(color)

        self.rect = rect
        self.speed = speed

    def update(self):
        # Move the block horizontally
        self.rect.x += self.speed

        # Reverse direction if it reaches the screen boundaries
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed = -self.speed

all_sprites = pygame.sprite.Group()
player = Player(red, 50, 50)
platform_rect = pygame.Rect(0, screen_height - 70, screen_width, 20)  # Adjusted platform position
platform = Platform(blue, platform_rect)
restart_block_rect = pygame.Rect(300, screen_height - 90, 50, 20)  # Restart block position (adjusted y)
restart_block = RestartBlock(black, restart_block_rect)
moving_block_rect = pygame.Rect(500, screen_height - 130, 30, 20)  # Moving block position
moving_block = MovingBlock(pink, moving_block_rect, 2)
all_sprites.add(player, platform, restart_block, moving_block)

clock = pygame.time.Clock()

camera_x = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.rect.x -= 5
    if keys[pygame.K_RIGHT]:
        player.rect.x += 5

    # Update
    all_sprites.update()

    # Update camera position
    camera_x = player.rect.x - screen_width // 2

    # Check for collisions
    if pygame.sprite.collide_rect(player, platform):
        player.rect.y = platform.rect.y - player.rect.height
        player.velocity_y = 0
        player.on_ground = True

    # Check for collision with the restart block
    if pygame.sprite.collide_rect(player, restart_block):
        # Reset player position and velocity
        player.rect.x = 50
        player.rect.y = 50
        player.velocity_y = 0
        player.on_ground = False

    # Check for collision with the moving block
    if pygame.sprite.collide_rect(player, moving_block):
        # Reset player position and velocity
        player.rect.x = 50
        player.rect.y = 50
        player.velocity_y = 0
        player.on_ground = False

    # Draw
    screen.fill(white)

    # Draw sprites with camera offset
    for sprite in all_sprites:
        screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)
