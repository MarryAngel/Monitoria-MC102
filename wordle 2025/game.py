# https://www.ime.usp.br/~pf/dicios/ -> lista de palavras usado

import pygame
import sys
import random
from player import pensar, chutar_palavra, retorno

# Configurações
WIDTH, HEIGHT = 400, 500
GRID_SIZE = 5  # Quantidade de letras por palavra
ATTEMPTS = 1  # Número de tentativas
CELL_SIZE = 50
MARGIN = 10
FONT_SIZE = 40
camera_y = 0
ganhei = False
n_chutes = 0

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 200, 0)
YELLOW = (200, 200, 0)
DARK_GRAY = (50, 50, 50)

# Inicialização do Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle Pygame")
font = pygame.font.Font(None, FONT_SIZE)

# Carregar palavras do arquivo
with open("palavras.txt", "r", encoding="utf-8") as file:
    words = [line.strip().upper() for line in file.readlines() if len(line.strip()) == 5]

# Escolher uma palavra aleatória
correct_word = random.choice(words)
#correct_word = "ABACO"
print(correct_word)

grid = [["" for _ in range(GRID_SIZE)] for _ in range(ATTEMPTS)]
colors = [[GRAY for _ in range(GRID_SIZE)] for _ in range(ATTEMPTS)]
print(f"{colors=}")
current_row, current_col = 0, 0


def draw_grid():
    screen.fill(WHITE)
    for row in range(ATTEMPTS):
        for col in range(GRID_SIZE):
            x, y = col * (CELL_SIZE + MARGIN) + 50, row * (CELL_SIZE + MARGIN) + 50 + camera_y
            pygame.draw.rect(screen, colors[row][col], (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 2)
            if grid[row][col]:
                text = font.render(grid[row][col], True, BLACK)
                screen.blit(text, (x + 15, y + 5))
            if row == current_row and col == current_col:
                pygame.draw.line(screen, BLACK, (x + 5, y + CELL_SIZE - 5), (x + CELL_SIZE - 5, y + CELL_SIZE - 5), 2)
    pygame.display.flip()


def check_word():
    global current_row, ATTEMPTS, ganhei, n_chutes
    n_chutes += 1
    guess = "".join(grid[current_row])
    if len(guess) == GRID_SIZE and guess in words:
        if guess == correct_word:
            for i in range(GRID_SIZE):
                colors[current_row][i] = GREEN
            print(f"Você venceu em {n_chutes} chutes!")
            ganhei = True
        else:
            correct_letters = list(correct_word)
            guessed_letters = list(guess)
            
            # Primeiro, marca os verdes
            for i in range(GRID_SIZE):
                if guessed_letters[i] == correct_letters[i]:
                    colors[current_row][i] = GREEN
                    correct_letters[i] = None  # Marca como usada
            
            # Depois, marca os amarelos
            for i in range(GRID_SIZE):
                if colors[current_row][i] != GREEN and guessed_letters[i] in correct_letters:
                    colors[current_row][i] = YELLOW
                    correct_letters[correct_letters.index(guessed_letters[i])] = None  # Marca como usada
            
            # Por fim, os que não estão na palavra
            for i in range(GRID_SIZE):
                if colors[current_row][i] not in [GREEN, YELLOW]:
                    colors[current_row][i] = DARK_GRAY
        
        #current_row += 1 # Vai para a próxima linha
        grid.insert(0,["" for _ in range(GRID_SIZE)])
        colors.insert(0,[GRAY for _ in range(GRID_SIZE)])
        
        ATTEMPTS += 1

        

def automatizar():
    pensar()
    chute = chutar_palavra().upper()
    for i in range(GRID_SIZE):
        if len(chute) <= i:
            break
        grid[current_row][i] = chute[i]
    check_word()
    retorno(colors[current_row])

draw_grid()

running = True
clock = pygame.time.Clock()
while running:
    clock.tick(60)  # rodar a 60 FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif ganhei:
            continue
        elif event.type == pygame.KEYDOWN:
            if pygame.K_a <= event.key <= pygame.K_z and current_col < GRID_SIZE:
                grid[current_row][current_col] = chr(event.key).upper()
                current_col +=1
                camera_y = 0
            elif event.key == pygame.K_BACKSPACE:
                if current_col < GRID_SIZE and grid[current_row][current_col] != '':
                    grid[current_row][current_col] = ''
                    continue                    
                current_col = max(current_col - 1, 0)
                grid[current_row][current_col] = ""
                camera_y = 0
            elif event.key == pygame.K_RETURN:
                check_word()
                current_col = 0
                camera_y = 0
            elif event.key == pygame.K_LEFT and current_col > 0:
                current_col -= 1
                camera_y = 0
            elif event.key == pygame.K_RIGHT and current_col < GRID_SIZE - 1:
                current_col += 1
                camera_y = 0
            elif event.key == pygame.K_UP:
                camera_y = min(camera_y + (CELL_SIZE + MARGIN),0)
            elif event.key == pygame.K_DOWN:
                if ATTEMPTS + camera_y / (CELL_SIZE + MARGIN) > 7 :
                    camera_y = max(camera_y -(CELL_SIZE + MARGIN), -(CELL_SIZE + MARGIN) * (ATTEMPTS))
    
    if not ganhei:
        automatizar()
        
        draw_grid()
    
    if ganhei:
        draw_grid() # e adiciona o da vitória

pygame.quit()
sys.exit()
