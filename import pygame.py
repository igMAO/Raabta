import pygame
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre du jeu
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (56, 61, 77)
ORANGE = (212, 115, 212)
GREEN = (145, 40, 59)
BLUE = (0, 0, 255)
BARBIE_PINK = (255, 79, 191)  # Couleur rose Barbie

# Variables
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 120
BALL_RADIUS = 15
PADDLE_SPEED = 5
BALL_SPEED = 8
WINNING_SCORE = 10

# Création des raquettes
player_paddle = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Création de la balle
ball = pygame.Rect(WIDTH//2 - BALL_RADIUS//2, HEIGHT//2 - BALL_RADIUS//2, BALL_RADIUS, BALL_RADIUS)

# Direction de la balle
ball_dx = BALL_SPEED
ball_dy = 0

# Score
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 36)

# Fonction pour redessiner la fenêtre du jeu
def draw_window(winner=None):
    WIN.fill(BLACK)
    pygame.draw.rect(WIN, ORANGE, player_paddle)
    pygame.draw.rect(WIN, GREEN, opponent_paddle)
    pygame.draw.ellipse(WIN, BARBIE_PINK, ball)  # Dessiner la balle en rose Barbie
    
    # Affichage du score du joueur en orange
    player_score_text = font.render(str(player_score), True, ORANGE)
    WIN.blit(player_score_text, (WIDTH//4 - player_score_text.get_width()//2, 20))
    
    # Affichage du score de l'adversaire en vert
    opponent_score_text = font.render(str(opponent_score), True, GREEN)
    WIN.blit(opponent_score_text, (WIDTH*3//4 - opponent_score_text.get_width()//2, 20))
    
    # Affichage du gagnant s'il y en a un
    if winner:
        winner_text = font.render(f"{winner} gagne !", True, BLUE)  # Message final en bleu
        WIN.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, HEIGHT//2 - winner_text.get_height()//2))
        restart_text = font.render("Appuyez sur R pour recommencer", True, WHITE)
        WIN.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))
    
    pygame.display.update()

# Fonction principale
def main():
    global ball_dx, ball_dy, player_score, opponent_score

    clock = pygame.time.Clock()
    run = True
    winner = None

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # Si la partie est terminée, relancer une nouvelle partie en réinitialisant les scores et la position de la balle
                if winner:
                    player_score = 0
                    opponent_score = 0
                    ball.x = WIDTH//2 - BALL_RADIUS//2
                    ball.y = HEIGHT//2 - BALL_RADIUS//2
                    ball_dx = BALL_SPEED
                    ball_dy = 0
                    winner = None

        # Déplacement de la raquette du joueur
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_paddle.top > 0:
            player_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and player_paddle.bottom < HEIGHT:
            player_paddle.y += PADDLE_SPEED

        # Déplacement de la raquette de l'adversaire
        if ball_dx > 0:  # Se déplace seulement lorsque la balle se dirige vers l'adversaire
            # Calcul de la position anticipée de la balle
            anticipated_ball_y = ball.y + (ball_dy / ball_dx) * (opponent_paddle.x - ball.x)
            # Ajustement de la position de l'adversaire pour intercepter la balle
            if opponent_paddle.centery < anticipated_ball_y:
                opponent_paddle.y += PADDLE_SPEED
            elif opponent_paddle.centery > anticipated_ball_y:
                opponent_paddle.y -= PADDLE_SPEED

        # Déplacement de la balle
        ball.x += ball_dx
        ball.y += ball_dy

        # Collision avec les bords de la fenêtre
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_dy *= -1

        # Collision avec les raquettes
        if ball.colliderect(player_paddle):
            ball_dx = BALL_SPEED
            ball_dy = (ball.y + BALL_RADIUS/2 - player_paddle.y - PADDLE_HEIGHT/2) / (PADDLE_HEIGHT/2) * BALL_SPEED
        elif ball.colliderect(opponent_paddle):
            ball_dx = -BALL_SPEED
            ball_dy = (ball.y + BALL_RADIUS/2 - opponent_paddle.y - PADDLE_HEIGHT/2) / (PADDLE_HEIGHT/2) * BALL_SPEED

        # Gestion des scores et réinitialisation de la position de la balle
        if ball.left <= 0:
            opponent_score += 1
            if opponent_score >= WINNING_SCORE:
                winner = "Adversaire"
            else:
                ball_dx = BALL_SPEED
                ball_dy = 0
                ball.x = WIDTH//2 - BALL_RADIUS//2
                ball.y = HEIGHT//2 - BALL_RADIUS//2
        elif ball.right >= WIDTH:
            player_score += 1
            if player_score >= WINNING_SCORE:
                winner = "Joueur"
            else:
                ball_dx = -BALL_SPEED
                ball_dy = 0
                ball.x = WIDTH//2 - BALL_RADIUS//2
                ball.y = HEIGHT//2 - BALL_RADIUS//2

        draw_window(winner)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                main()

if __name__ == "__main__":
    main()
