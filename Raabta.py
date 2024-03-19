import pygame
import sys

# Initialize the game engine
pygame.init()

# Set the height and width of the screen
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode([screen_width, screen_height])

# Set the name of the window
pygame.display.set_caption("Platformer with Jump and Camera")

# Set colors
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
black = (0, 0, 0)
pink = (255, 182, 193)  # Rose color
green = (0, 255, 0)

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

    def collision(self, sprite):
        if pygame.sprite.collide_rect(sprite, self):
            sprite.rect.y = self.rect.y - sprite.rect.height
            sprite.velocity_y = 0
            sprite.on_ground = True

class Wall(pygame.sprite.Sprite):
    def __init__(self, color, rect):
        super().__init__()

        self.image = pygame.Surface([rect.width, rect.height])
        self.image.fill(color)

        self.rect = rect

        # Collider rect
        self.collider_rect = pygame.Rect(rect.x, rect.y, rect.width, rect.height)

    def collision(self, sprite):
        if self.collider_rect.colliderect(sprite.rect):
            sprite.rect.x = self.rect.right
            sprite.velocity_y = 0
            sprite.on_ground = True

class MovingBlock(pygame.sprite.Sprite):
    def __init__(self, color, rect, distance):
        super().__init__()

        self.image = pygame.Surface([rect.width, rect.height])
        self.image.fill(color)

        self.rect = rect
        self.speed = 2  # Vitesse constante
        self.distance = distance
        self.start_x = rect.x  # Enregistre la position initiale du bloc

    def update(self):
        # Move le bloc horizontalement
        self.rect.x += self.speed

        # Inverser la direction lorsque le bloc atteint la distance maximale
        if abs(self.rect.x - self.start_x) >= self.distance:
            self.speed = -self.speed

# Initialize sprite groups
all_sprites = pygame.sprite.Group()

# Create player
player = Player(red, 50, 50)
all_sprites.add(player)

# Create platforms
platform_rect1 = pygame.Rect(0, screen_height - 100, 800, 100)  # First part of platform
platform_rect2 = pygame.Rect(1120, screen_height - 100, 800, 100)  # Second part of platform
platform = Platform(blue, platform_rect1)
platform2 = Platform(blue, platform_rect2)
all_sprites.add(platform, platform2)

# Create wall
wall_rect = pygame.Rect(0, 0, 20, screen_height)  # Wall position
wall = Wall(green, wall_rect)
all_sprites.add(wall)

# Create black block
black_block_rect = pygame.Rect(800, screen_height - 60, 320, 60)  # Black block position with reduced height
black_block = Platform(black, black_block_rect)
all_sprites.add(black_block)

# Create floating platform above black block
floating_platform_rect = pygame.Rect(910, screen_height - 200, 80, 20)  # Floating platform position
floating_platform = Platform(blue, floating_platform_rect)
all_sprites.add(floating_platform)

# Create moving block
moving_block_rect = pygame.Rect(1500, screen_height - 130, 30, 20)  # Moving block position
moving_block = MovingBlock(pink, moving_block_rect, 200)  # 400 pixels de distance
all_sprites.add(moving_block)

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

    # Check for collisions with platform and wall
    platform.collision(player)
    platform2.collision(player)
    wall.collision(player)

    # Check for collision with the floating platform
    if pygame.sprite.collide_rect(player, floating_platform):
        player.rect.y = floating_platform.rect.y - player.rect.height
        player.velocity_y = 0
        player.on_ground = True

    # Check for collision with the moving block
    if pygame.sprite.collide_rect(player, moving_block):
        # Reset player position and velocity
        player.rect.x = 50
        player.rect.y = 50

    # Check for collision with the black block
    if pygame.sprite.collide_rect(player, black_block):
        # Reset player position
        player.rect.x = 50
        player.rect.y = 50

    # Draw
    screen.fill(white)

    # Draw sprites with camera offset
    for sprite in all_sprites:
        screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)
