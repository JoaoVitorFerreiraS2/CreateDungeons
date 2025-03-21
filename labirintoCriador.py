import random
import cairo as ca

def init_grid(width, height):
    return [[0 for _ in range(height)] for _ in range(width)]

def is_valid_move(grid, x, y, width, height):
    return 0 <= x < width and 0 <= y < height and grid[x][y] == 0

def generate_labyrinth(grid, width, height):
    stack = [(1, 1)]  # Começa no canto superior esquerdo
    directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]  # Movimentos possíveis
    
    while stack:
        x, y = stack[-1]
        grid[x][y] = 1  # Marca como caminho
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid_move(grid, nx, ny, width, height):
                grid[x + dx // 2][y + dy // 2] = 1  # Remove a parede
                stack.append((nx, ny))
                break
        else:
            stack.pop()

def draw_maze(grid, width, height, scale, filename):
    img_w, img_h = width * scale, height * scale
    surf = ca.ImageSurface(ca.FORMAT_ARGB32, img_w, img_h)
    ctx = ca.Context(surf)
    
    ctx.set_source_rgb(0, 0, 0)  # Fundo preto
    ctx.rectangle(0, 0, img_w, img_h)
    ctx.fill()
    
    ctx.set_source_rgb(1, 1, 1)  # Caminhos brancos
    for x in range(width):
        for y in range(height):
            if grid[x][y] == 1:
                ctx.rectangle(x * scale, y * scale, scale, scale)
                ctx.fill()
    
    surf.write_to_png(filename)

# Configurações do usuário
WIDTH, HEIGHT = 91, 91  # Deve ser ímpar para garantir bordas
SCALE = 200  # Tamanho dos pixels
FILENAME = "labirinto.png"

# Gerar e desenhar labirinto
grid = init_grid(WIDTH, HEIGHT)
generate_labyrinth(grid, WIDTH, HEIGHT)
draw_maze(grid, WIDTH, HEIGHT, SCALE, FILENAME)

print(f"Labirinto gerado e salvo como {FILENAME}")
