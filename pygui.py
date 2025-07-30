import pygame
import random

# Initialize pygame
pygame.init()

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Shooter")

# Clock to control framerate
clock = pygame.time.Clock()

# Load images
player_img = pygame.image.load("spaceship.png")
bullet_img = pygame.image.load("bullet.png")
alien_img = pygame.image.load("space.png")

# Scale assets
player_img = pygame.transform.scale(player_img, (60, 60))
bullet_img = pygame.transform.scale(bullet_img, (20, 40))
alien_img = pygame.transform.scale(alien_img, (50, 50))

# Player settings
player_x = screen_width // 2
player_y = screen_height - 80
player_speed = 6

# Bullet settings
bullet_x = 0
bullet_y = player_y
bullet_speed = 17
bullet_state = "ready"  # "ready" means not visible, "fire" means moving

# Alien settings
num_aliens = 5
alien_x = [random.randint(0, screen_width - 50) for _ in range(num_aliens)]
alien_y = [random.randint(50, 150) for _ in range(num_aliens)]
alien_speed = [4 for _ in range(num_aliens)]

# Score
score = 0
font = pygame.font.Font("Cream Beige.ttf", 32)
def show_score():
    score_text = font.render(f"SCORE: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def player(x, y):
    screen.blit(player_img, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 20, y))

def is_collision(alien_x, alien_y, bullet_x, bullet_y):
    alien_rect = pygame.Rect(alien_x, alien_y, 30, 30)
    bullet_rect = pygame.Rect(bullet_x, bullet_y, 20, 30)
    return alien_rect.colliderect(bullet_rect)

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear screen
    show_score()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Keyboard input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_x += player_speed
    if keys[pygame.K_SPACE] and bullet_state == "ready":
        bullet_x = player_x
        fire_bullet(bullet_x, bullet_y)

    # Keep player on screen
    player_x = max(0, min(screen_width - 60, player_x))

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_speed
        if bullet_y < 0:
            bullet_y = player_y
            bullet_state = "ready"

    # Alien movement and collision
    for i in range(num_aliens):
        alien_x[i] += alien_speed[i]
        if alien_x[i] <= 0 or alien_x[i] >= screen_width - 50:
            alien_speed[i] *= -1
            alien_y[i] += 40

        # Collision check
        if is_collision(alien_x[i], alien_y[i], bullet_x, bullet_y):
            bullet_y = player_y
            bullet_state = "ready"
            score += 1
            alien_x[i] = random.randint(0, screen_width - 50)
            alien_y[i] = random.randint(50, 150)

        screen.blit(alien_img, (alien_x[i], alien_y[i]))

    # Draw player
    player(player_x, player_y)

    pygame.display.update()
    clock.tick(30)  # Slow down game to 30 FPS
