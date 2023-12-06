import pygame
import sys
import math
import random

# Inicializar Pygame
pygame.init()

# Configuraciones generales
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Shooter Game")

# Colores
black = (0, 0, 0)
white = (255, 255, 255)

# Jugador
player_size = 50
player_speed = 5
player = pygame.Rect(width // 2 - player_size // 2, height // 2 - player_size // 2, player_size, player_size)

# Proyectiles del jugador
player_projectiles = []

# Enemigos
num_enemies = 3
enemies = []
enemy_shoot_timers = []

# Frecuencia de aparición de enemigos
spawn_frequency = 180

# Estado del juego
game_over = False
menu_active = True
num_lives = 3

# Menú
menu_options = ["Number of Enemies", "Spawn Frequency"]
current_option = 0

# Función para mostrar el menú
def show_menu():
    screen.fill(black)
    font = pygame.font.Font(None, 36)
    title = font.render("Game Menu", True, white)
    screen.blit(title, (width // 2 - 100, 50))

    for i, option in enumerate(menu_options):
        text_color = white if i == current_option else (100, 100, 100)
        option_text = font.render(f"{option}: {get_option_value(option)}", True, text_color)
        screen.blit(option_text, (width // 2 - 200, 150 + i * 50))

    pygame.display.flip()

# Función para manejar eventos de teclado en el menú
def handle_menu_events():
    global num_enemies, spawn_frequency, current_option
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        # Mover hacia arriba en el menú
        current_option = (current_option - 1) % len(menu_options)
    elif keys[pygame.K_DOWN]:
        # Mover hacia abajo en el menú
        current_option = (current_option + 1) % len(menu_options)
    elif keys[pygame.K_LEFT] and menu_options[current_option] == "Number of Enemies":
        # Decrementar el valor de "Number of Enemies"
        num_enemies = max(1, num_enemies - 1)
    elif keys[pygame.K_RIGHT] and menu_options[current_option] == "Number of Enemies":
        # Incrementar el valor de "Number of Enemies"
        num_enemies += 1
    elif keys[pygame.K_LEFT] and menu_options[current_option] == "Spawn Frequency":
        # Decrementar el valor de "Spawn Frequency"
        spawn_frequency = max(60, spawn_frequency - 60)  # Ajustar al menos 1 segundo
    elif keys[pygame.K_RIGHT] and menu_options[current_option] == "Spawn Frequency":
        # Incrementar el valor de "Spawn Frequency"
        spawn_frequency += 60  # Ajustar al menos 1 segundo

# Función para obtener el valor actual de la opción del menú
def get_option_value(option):
    if option == "Number of Enemies":
        return num_enemies
    elif option == "Spawn Frequency":
        return spawn_frequency // 60  # Convertir a segundos

# Función para dibujar al jugador en la pantalla
def draw_player():
    pygame.draw.rect(screen, white, player)

# Función para dibujar los proyectiles del jugador en la pantalla
def draw_player_projectiles():
    for projectile in player_projectiles:
        pygame.draw.circle(screen, white, (int(projectile[0]), int(projectile[1])), 5)

# Función para dibujar los proyectiles de los enemigos en la pantalla
def draw_enemy_projectiles():
    for enemy in enemies:
        for projectile in enemy['projectiles']:
            pygame.draw.circle(screen, white, (int(projectile[0]), int(projectile[1])), 5)

# Función para dibujar a los enemigos en la pantalla
def draw_enemies():
    for enemy in enemies:
        pygame.draw.rect(screen, white, enemy['rect'])

# Función para mover a los enemigos hacia el jugador
def move_enemies_towards_player():
    for enemy in enemies:
        if enemy['rect'].centerx > player.centerx:
            enemy['rect'].move_ip(-2, 0)
        elif enemy['rect'].centerx < player.centerx:
            enemy['rect'].move_ip(2, 0)

# Función para hacer que los enemigos disparen proyectiles
def shoot_projectiles_from_enemies():
    for i, enemy in enumerate(enemies):
        if enemy_shoot_timers[i] <= 0:
            enemy['projectiles'].append([enemy['rect'].centerx, enemy['rect'].centery, math.atan2(player.centery - enemy['rect'].centery, player.centerx - enemy['rect'].centerx)])
            enemy_shoot_timers[i] = spawn_frequency
        else:
            enemy_shoot_timers[i] -= 1

# Función para mostrar el estado del juego (vidas restantes)
def show_game_state():
    font = pygame.font.Font(None, 36)
    lives_text = font.render(f"Lives: {num_lives}", True, white)
    screen.blit(lives_text, (10, 10))

def handle_mouse_click(mouse_x, mouse_y):
    # Calcular la dirección del clic del mouse desde el jugador
    angle = math.atan2(mouse_y - player.centery, mouse_x - player.centerx)

    # Agregar un proyectil desde el jugador en la dirección del clic del mouse
    player_projectiles.append([player.centerx, player.centery, angle])

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and not menu_active:
              # Obtener las coordenadas del clic del mouse
            mouse_x, mouse_y = pygame.mouse.get_pos()
            handle_mouse_click(mouse_x, mouse_y)

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if menu_active:
                menu_active = False
                game_over = False
                num_lives = 3
                enemies = []
                enemy_shoot_timers = []
                for _ in range(num_enemies):
                    enemy_size = random.randint(10, 30)
                    enemy = {
                        'rect': pygame.Rect(width, random.randint(0, height - enemy_size), enemy_size, enemy_size),
                        'projectiles': []
                    }
                    enemies.append(enemy)
                    enemy_shoot_timers.append(random.randint(0, spawn_frequency))
                player.x = width // 2 - player_size // 2
                player.y = height // 2 - player_size // 2
                player_projectiles = []
            elif game_over:
                game_over = False
                num_lives = 3
                enemies = []
                enemy_shoot_timers = []
                for _ in range(num_enemies):
                    enemy_size = random.randint(10, 30)
                    enemy = {
                        'rect': pygame.Rect(width, random.randint(0, height - enemy_size), enemy_size, enemy_size),
                        'projectiles': []
                    }
                    enemies.append(enemy)
                    enemy_shoot_timers.append(random.randint(0, spawn_frequency))
                player.x = width // 2 - player_size // 2
                player.y = height // 2 - player_size // 2
                player_projectiles = []

        elif event.type == pygame.KEYDOWN and not menu_active:
            handle_menu_events()  # Manejar eventos de teclado en el menú

    if not menu_active:
        keys = pygame.key.get_pressed()

        if not game_over:
            # Mover al jugador
            if keys[pygame.K_w] and player.top > 0:
                player.move_ip(0, -player_speed)
            if keys[pygame.K_s] and player.bottom < height:
                player.move_ip(0, player_speed)
            if keys[pygame.K_a] and player.left > 0:
                player.move_ip(-player_speed, 0)
            if keys[pygame.K_d] and player.right < width:
                player.move_ip(player_speed, 0)

            # Mover proyectiles del jugador
            for projectile in player_projectiles:
                projectile[0] += 8 * math.cos(projectile[2])
                projectile[1] += 8 * math.sin(projectile[2])

            # Limpiar proyectiles del jugador fuera de pantalla
            player_projectiles = [p for p in player_projectiles if 0 < p[0] < width and 0 < p[1] < height]

            # Mover enemigos hacia el jugador
            move_enemies_towards_player()

            # Disparar proyectiles desde los enemigos
            shoot_projectiles_from_enemies()

            # Mover proyectiles de los enemigos
            for enemy in enemies:
                for projectile in enemy['projectiles']:
                    projectile[0] += 8 * math.cos(projectile[2])
                    projectile[1] += 8 * math.sin(projectile[2])

            # Limpiar proyectiles de los enemigos fuera de pantalla
            for enemy in enemies:
                enemy['projectiles'] = [p for p in enemy['projectiles'] if 0 < p[0] < width and 0 < p[1] < height]

            # Verificar colisiones entre proyectiles del jugador y enemigos
            for projectile in player_projectiles:
                for enemy in enemies:
                    if enemy['rect'].colliderect(pygame.Rect(projectile[0], projectile[1], 5, 5)):
                        enemies.remove(enemy)
                        player_projectiles.remove(projectile)

            # Verificar colisiones entre proyectiles de los enemigos y jugador
            for enemy in enemies:
                for projectile in enemy['projectiles']:
                    if player.colliderect(pygame.Rect(projectile[0], projectile[1], 5, 5)):
                        num_lives -= 1
                        if num_lives == 0:
                            game_over = True
                        else:
                            player.x = width // 2 - player_size // 2
                            player.y = height // 2 - player_size // 2
                            player_projectiles = []

            # Generar nuevos enemigos aleatorios
            if random.randint(0, 100) < 5 and len(enemies) < num_enemies:
                enemy_size = random.randint(10, 30)
                enemy = {
                    'rect': pygame.Rect(width, random.randint(0, height - enemy_size), enemy_size, enemy_size),
                    'projectiles': []
                }
                enemies.append(enemy)
                enemy_shoot_timers.append(random.randint(0, spawn_frequency))

            # Limpiar enemigos fuera de pantalla
            enemies = [enemy for enemy in enemies if enemy['rect'].right > 0]

        # Dibujar la pantalla
        screen.fill(black)
        draw_player()
        draw_player_projectiles()
        draw_enemy_projectiles()
        draw_enemies()
        show_game_state()

        if game_over:
            # Mostrar pantalla de "Game Over"
            font = pygame.font.Font(None, 36)
            game_over_text = font.render("Game Over", True, white)
            screen.blit(game_over_text, (width // 2 - 100, height // 2))
            # Mostrar mensaje de reinicio
            restart_text = font.render("Press SPACE to Restart", True, white)
            screen.blit(restart_text, (width // 2 - 150, height // 2 + 50))

        pygame.display.flip()

    else:
        # Mostrar el menú si está activo
        show_menu()

    # Controlar la velocidad del juego
    pygame.time.Clock().tick(60)
