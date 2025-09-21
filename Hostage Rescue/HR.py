import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
TILE_SIZE = 40
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rescue the Hostage - Local Search")

# Colors
WHITE = (240, 248, 255)
RED = (255, 69, 0)      # Hostage color
BLUE = (30, 144, 255)   # Player color
LIGHT_GREY = (211, 211, 211) # Background grid color
FLASH_COLOR = (50, 205, 50) # Victory flash color
BUTTON_COLOR = (50, 205, 50) # Button color
BUTTON_TEXT_COLOR = (255, 255, 255) # Button text color

# Load images for player, hostage, and walls
player_image = pygame.image.load("AI1.png")  
hostage_image = pygame.image.load("AI2.png")  
wall_images = [
    pygame.image.load("AI3.png"),
    pygame.image.load("AI4.png"),
    pygame.image.load("AI5.png")
]

# Resize images to fit the grid
wall_images = [pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) for img in wall_images]
player_image = pygame.transform.scale(player_image, (TILE_SIZE, TILE_SIZE))
hostage_image = pygame.transform.scale(hostage_image, (TILE_SIZE, TILE_SIZE))

# Constants for recent positions
MAX_RECENT_POSITIONS = 10
GENERATION_LIMIT = 50
MUTATION_RATE = 0.1

# Function to generate obstacles
def generate_obstacles(num_obstacles):
    obstacles = []
    while len(obstacles) < num_obstacles:
        new_obstacle = [random.randint(0, COLS-1), random.randint(0, ROWS-1)]
        if new_obstacle not in obstacles:  # Make sure obstacles are not overlapping
            obstacles.append(new_obstacle)
    obstacle_images = [random.choice(wall_images) for _ in obstacles]
    return obstacles, obstacle_images

# Function to start a new game
def start_new_game():
    global player_pos, hostage_pos, recent_positions, obstacles, obstacle_images
    obstacles, obstacle_images = generate_obstacles(20)
    recent_positions = []

    # Generate player and hostage positions with a larger distance
    while True:
        player_pos = [random.randint(0, COLS-1), random.randint(0, ROWS-1)]
        hostage_pos = [random.randint(0, COLS-1), random.randint(0, ROWS-1)]
        distance = math.dist(player_pos, hostage_pos)
        if distance > 8 and player_pos not in obstacles and hostage_pos not in obstacles:
            break

# Function to move the player closer to the hostage using Hill Climbing algorithm
def hill_climbing(player, hostage, obstacles):
    #todo 
    pass
 

# Function for Simulated Annealing
def simulated_annealing(player, hostage, obstacles):
    temperature = 100  # Initial temperature
    cooling_rate = 0.99
    #todo
    pass

    # Acceptance probability function
    def acceptance_probability(old_cost, new_cost, temp):
        #todo
        pass

# Function for Genetic Algorithm
def genetic_algorithm(player, hostage, obstacles):
    population_size = 20
    generations = 50
    # todo
    # Return the best individual
    pass

    # Fitness function
    def fitness(individual):
        #todo
        pass

    # Generate random population
    def generate_population():
        #todo
        pass

    # Crossover function
    def crossover(parent1, parent2):
        #todo
        pass

    # Mutation function
    def mutate(individual):
        #todo
        pass
    

#Objective: Check if the player is stuck in a repeating loop.
def in_loop(recent_positions, player):
    #todo
    pass

#Objective: Make a random safe move to escape loops or being stuck.
def random_move(player, obstacles):
    #todo
    pass

#Objective: Update the list of recent positions. 
def store_recent_position(recent_positions, new_player_pos, max_positions=MAX_RECENT_POSITIONS):
    #todo
    pass

# Function to show victory flash
def victory_flash():
    for _ in range(5):
        screen.fill(FLASH_COLOR)
        pygame.display.flip()
        pygame.time.delay(100)
        screen.fill(WHITE)
        pygame.display.flip()
        pygame.time.delay(100)

# Function to show a button and wait for player's input
def show_button_and_wait(message, button_rect):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, BUTTON_TEXT_COLOR)
    button_rect.width = text.get_width() + 20
    button_rect.height = text.get_height() + 10
    button_rect.center = (WIDTH // 2, HEIGHT // 2)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    screen.blit(text, (button_rect.x + (button_rect.width - text.get_width()) // 2,
                       button_rect.y + (button_rect.height - text.get_height()) // 2))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False

# Function to get the algorithm choice from the player
def get_algorithm_choice():
    print("Choose an algorithm:")
    print("1: Hill Climbing")
    print("2: Simulated Annealing")
    print("3: Genetic Algorithm")

    while True:
        choice = input("Enter the number of the algorithm you want to use (1/2/3): ")
        if choice == "1":
            return hill_climbing
        elif choice == "2":
            return simulated_annealing
        elif choice == "3":
            return genetic_algorithm
        else:
            print("Invalid choice. Please choose 1, 2, or 3.")

# Main game loop
running = True
clock = pygame.time.Clock()
start_new_game()
button_rect = pygame.Rect(0, 0, 0, 0)

# Get the algorithm choice from the player
chosen_algorithm = get_algorithm_choice()

while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Perform the chosen algorithm step
    new_player_pos = chosen_algorithm(player_pos, hostage_pos, obstacles)

    # Check for stuck situations
    if new_player_pos == player_pos or in_loop(recent_positions, new_player_pos):
        # Perform a random move when stuck
        new_player_pos = random_move(player_pos, obstacles)

    # Update recent positions
    store_recent_position(recent_positions, new_player_pos)
    # Update player's position
    player_pos = new_player_pos

    # Draw the grid background
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, LIGHT_GREY, rect, 1)

    # Draw obstacles
    for idx, obs in enumerate(obstacles):
        obs_rect = pygame.Rect(obs[0] * TILE_SIZE, obs[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        screen.blit(obstacle_images[idx], obs_rect)

    # Draw player
    player_rect = pygame.Rect(player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    screen.blit(player_image, player_rect)

    # Draw hostage
    hostage_rect = pygame.Rect(hostage_pos[0] * TILE_SIZE, hostage_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    screen.blit(hostage_image, hostage_rect)

    # Check if player reached the hostage
    if player_pos == hostage_pos:
        print("Hostage Rescued!")
        victory_flash()  # Show the victory flash
        show_button_and_wait("New Game", button_rect)
        start_new_game()

    # Update the display
    pygame.display.flip()
    clock.tick(5)  # Lower frame rate for smoother performance

pygame.quit()
