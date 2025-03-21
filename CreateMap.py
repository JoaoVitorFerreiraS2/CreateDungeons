import random
import cairo as ca
import os

# Perguntas referentes
while True:
    mini_mapa = input('MINI-MAPA [S | N]: ').strip().upper()
    if mini_mapa in ["S", "N"]:
        mini_mapa = mini_mapa == "S"
        break
    print("Por favor, digite [S | N]")

while True:
    grade = input('Grade [S | N]: ').strip().upper()
    if grade in ["S", "N"]:
        grade = grade == "S"
        break
    print("Por favor, digite [S | N]")

while True:
    WIDTH = input('Digite a Largura (Em pixel): ').strip()
    if WIDTH.isdigit():
        WIDTH = int(WIDTH)
        break
    print("Somente é aceito números")

while True:
    HEIGHT = input('Digite a Altura (Em pixel): ').strip()
    if HEIGHT.isdigit():
        HEIGHT = int(HEIGHT)
        break
    print("Somente é aceito números")

while True:
    pasta_destino = input("Digite o caminho da pasta onde deseja salvar: (Se deixar em branco, salvará no diretório atual) ")
    if pasta_destino == "":
        pasta_destino = os.getcwd()
        break
    elif os.path.isdir(pasta_destino):
        break
    else:
        print("O Caminho fornecido não é valido")


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

        # Gradiente para paredes (cinza escuro para claro)
        for x in range(self.width):
            for y in range(self.height):
                if self.m.get(x, y) == 1:
                    gradient = ca.LinearGradient(x * scale, y * scale, (x + 1) * scale, (y + 1) * scale)
                    gradient.add_color_stop_rgb(0, 0.3, 0.3, 0.3)  # Cinza escuro
                    gradient.add_color_stop_rgb(1, 0.6, 0.6, 0.6)  # Cinza claro
                    ctx.set_source(gradient)
                    ctx.rectangle(x * scale, y * scale, scale, scale)
                    ctx.fill()

                    # Sombras para paredes
                    ctx.set_source_rgba(0, 0, 0, 0.4)  # Transparência leve
                    ctx.rectangle((x + 0.1) * scale, (y + 0.1) * scale, scale, scale)
                    ctx.fill()

                    # Borda para paredes
                    ctx.set_source_rgb(0, 0, 0)
                    ctx.set_line_width(1)
                    ctx.rectangle(x * scale, y * scale, scale, scale)
                    ctx.stroke()

        # Corredores com textura sólida branca
        ctx.set_source_rgb(1, 1, 1)
        for x in range(self.width):
            for y in range(self.height):
                if self.m.get(x, y) == 1:
                    ctx.rectangle(x * scale, y * scale, scale, scale)
                    ctx.fill()

        # Sombras para corredores
        for x in range(self.width):
            for y in range(self.height):
                if self.m.get(x, y) == 1:
                    ctx.set_source_rgba(0, 0, 0, 0.3)  # Transparência
                    ctx.rectangle((x + 0.1) * scale, (y + 0.1) * scale, scale, scale)
                    ctx.fill()

        # Desenhar grade (linhas cinza-escuro)
        if grade:
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
            mini_x = img_w - (self.width * mini_scale) + 10
            mini_y = img_h - (self.height * mini_scale) + 10

            # Fundo do mini-mapa (cinza escuro)
            ctx.set_source_rgb(0.2, 0.2, 0.2)
            ctx.rectangle(mini_x, mini_y, self.width * mini_scale, self.height * mini_scale)
            ctx.fill()

            # Borda do mini-mapa (branca)
            ctx.set_source_rgb(1, 1, 1)
            ctx.set_line_width(2)
            ctx.rectangle(mini_x, mini_y, self.width * mini_scale, self.height * mini_scale)
            ctx.stroke()

            # Desenhar paredes no mini-mapa (cinza claro)
            ctx.set_source_rgb(0.6, 0.6, 0.6)
            for x in range(self.width):
                for y in range(self.height):
                    if self.m.get(x, y) == 1:
                        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nx, ny = x + dx, y + dy
                            if self.outofbounds(nx, ny) or self.m.get(nx, ny) == 0:
                                ctx.rectangle(mini_x + x * mini_scale, mini_y + y * mini_scale, mini_scale, mini_scale)
                                ctx.fill()

            # Desenhar corredores no mini-mapa (branco)
            ctx.set_source_rgb(1, 1, 1)
            for x in range(self.width):
                for y in range(self.height):
                    if self.m.get(x, y) == 1:
                        ctx.rectangle(mini_x + x * mini_scale, mini_y + y * mini_scale, mini_scale, mini_scale)
                        ctx.fill()

        surf.write_to_png(fname)


# Gerar mapa e salvar como PNG
print('Aguarde enquanto carrega...')
g = generate(WIDTH, HEIGHT)
g.corridors()
nomedugeon = os.path.join(pasta_destino, input('Digite o nome da imagem: ').strip().lower() + ".png")
g.draw(nomedugeon)

print('-_-'*30)
print(f'''
Largura do mapa {WIDTH} pixels
Altura do mapa {HEIGHT} pixels
Nome do Mapa: {nomedugeon}
MiniMap: {mini_mapa}
Grade: {grade}
Quantidade de pixel {WIDTH * HEIGHT}''')
print('-_-'*30)