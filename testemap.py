import random
import cairo as ca

#Perguntas referentes
while(True):
    mini_mapa = str(input('MINI-MAPA [S | N]: ')).upper()
    if (mini_mapa == "S"):
        mini_mapa = True
        break
    elif (mini_mapa == "N"):
        mini_mapa = False
        break
    else:
        print("Por favor, digite [S | N]")    

while(True):
    grade = str(input('Grade [S | N]: ')).upper()
    if (grade == "S"):
        grade = True
        break
    elif (grade == "N"):
        grade = False
        break

    else: 
        print("Por favor, digite [S | N]")


while(True):
    WIDTH = str(input('Digite a Largura (Em pixel): ')).upper()
    if (WIDTH.isdigit()):
        WIDTH = int(WIDTH)
        break
    else: 
        print("Somente é aceito números")

while(True):
    HEIGHT = str(input('Digite a Altura (Em pixel): ')).upper()
    if (HEIGHT.isdigit()):
        HEIGHT = int(HEIGHT)
        break
    else: 
        print("Somente é aceito números")


nomedugeon = str(input('Digite o nome da imagem: ')).lower()
nomedugeon = nomedugeon + ".png"


class dir:
    def __init__(self, r):
        self.le = r
        self.arr = self.__rng__()
        self.cursor = -1

    def __rng__(self):
        return [random.randint(-1, 1) for _ in range(self.le)]

    def get(self):
        if self.cursor == len(self.arr) - 1:
            self.arr = self.__rng__()
            random.shuffle(self.arr)
            self.cursor = -1
        self.cursor += 1
        return self.arr[self.cursor]

class mapboard:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.board = [[0 for _ in range(h)] for _ in range(w)]

    def get(self, x, y):
        return self.board[x][y]

    def set(self, x, y, i):
        self.board[x][y] = i

class generate:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.m = mapboard(w, h)
        self.root = (w // 2, h // 2)

    def outofbounds(self, x, y):
        return x < 0 or x >= self.width or y < 0 or y >= self.height

    def setwidth(self, x, y, ty):
        for i in [x, x + 1, x - 1]:
            for j in [y, y + 1, y - 1]:
                if not self.outofbounds(i, j):
                    g = self.m.get(i, j)
                    if g in (0, 1, 2):
                        self.m.set(i, j, ty)

    def corridors(self):
        x, y = self.root
        rng = dir(12)
        cx, cy = x, y
        while not self.outofbounds(cx, cy):
            self.setwidth(cx, cy, 1)
            cx += rng.get()
            cy += rng.get()

    def draw(self, fname):
        scale = 10  # Escala do mapa principal
        mini_scale = 2  # Escala do mini-mapa
        img_w, img_h = self.width * scale, self.height * scale
        surf = ca.ImageSurface(ca.FORMAT_ARGB32, img_w, img_h)
        ctx = ca.Context(surf)

        # Fundo preto
        ctx.set_source_rgb(0, 0, 0)
        ctx.rectangle(0, 0, img_w, img_h)
        ctx.fill()

        # Desenhar paredes (cinza escuro)
        ctx.set_source_rgb(0.4, 0.4, 0.4)
        for x in range(self.width):
            for y in range(self.height):
                if self.m.get(x, y) == 1:
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if self.outofbounds(nx, ny) or self.m.get(nx, ny) == 0:
                            ctx.rectangle(x * scale, y * scale, scale, scale)
                            ctx.fill()

        # Desenhar corredores (branco)
        ctx.set_source_rgb(1, 1, 1)
        for x in range(self.width):
            for y in range(self.height):
                if self.m.get(x, y) == 1:
                    ctx.rectangle(x * scale, y * scale, scale, scale)
                    ctx.fill()

        # Desenhar grade (linhas cinza-escuro)
        if (grade == True):    
            ctx.set_source_rgb(0.2, 0.2, 0.2)
            ctx.set_line_width(1)
            for x in range(0, img_w, scale):
                ctx.move_to(x, 0)
                ctx.line_to(x, img_h)
            for y in range(0, img_h, scale):
                ctx.move_to(0, y)
                ctx.line_to(img_w, y)
            ctx.stroke()

        # Mini-mapa no canto inferior direito
        if mini_mapa:
            mini_x = img_w - (self.width * mini_scale) - 10
            mini_y = img_h - (self.height * mini_scale) - 10

            # Fundo do mini-mapa (cinza escuro)
            ctx.set_source_rgb(0.2, 0.2, 0.2)
            ctx.rectangle(mini_x, mini_y, self.width * mini_scale, self.height * mini_scale)
            ctx.fill()

            # Desenhar corredores no mini-mapa
            ctx.set_source_rgb(1, 1, 1)
            for x in range(self.width):
                for y in range(self.height):
                    if self.m.get(x, y) == 1:
                        ctx.rectangle(mini_x + x * mini_scale, mini_y + y * mini_scale, mini_scale, mini_scale)
                        ctx.fill()

        surf.write_to_png(fname)

# Gerar mapa e salvar como PNG
g = generate(WIDTH, HEIGHT)
g.corridors()
g.draw(nomedugeon)
