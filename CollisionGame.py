import pygame

# Initialize the game engine
pygame.init()

# Set the height and width of the screen
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])

# This sets the name of the window
pygame.display.set_caption("Control Character with Arrows")

# Set the background color
background_color = (232, 170, 190)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(background_color)

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, radius):
        super().__init__()
        self.image = pygame.Surface([radius * 2, radius * 2], pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.velocity = pygame.math.Vector2(0, 0)

    def move(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # Limit the character to stay within the screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

    def draw_circle(self):
        screen.blit(self.image, self.rect.topleft)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = (screen_width - width) // 2
        self.rect.y = (screen_height - height) // 2

if __name__ == "__main__":
    ball = Ball((219, 106, 143), 15)
    ball.rect.x = 100
    ball.rect.y = 100

    obstacle = Obstacle((202, 60, 102), 100, 200)  # Adjusted color, width, and height

    all_sprites_list = pygame.sprite.Group()
    all_sprites_list.add(ball, obstacle)

    clock = pygame.time.Clock()

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    ball.velocity.x = -3
                elif event.key == pygame.K_RIGHT:
                    ball.velocity.x = 3
                elif event.key == pygame.K_UP:
                    ball.velocity.y = -3
                elif event.key == pygame.K_DOWN:
                    ball.velocity.y = 3
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    ball.velocity.x = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    ball.velocity.y = 0

        ball.move()

        # Check for collision with the obstacle
        if pygame.sprite.collide_rect(ball, obstacle):
            ball.rect.x -= ball.velocity.x
            ball.rect.y -= ball.velocity.y

        screen.fill(background_color)
        all_sprites_list.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
