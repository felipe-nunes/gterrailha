import tkinter as tk
import random

def logging_decorator(func):
    """Decorator para registrar o início e o fim da execução de uma função.

    Args:
        func (function): Função a ser decorada.

    Returns:
        function: Função decorada com capacidades de log.
    """
    def wrapper(*args, **kwargs):
        print(f"Executing {func.__name__}...")
        result = func(*args, **kwargs)
        print(f"Done executing {func.__name__}.")
        return result
    return wrapper

# Decorator para atribuição de nomes aos terrenos
def assign_names_decorator(func):
    """Decorator para inicializar e embaralhar os nomes dos terrenos.

    Args:
        func (function): Função a ser decorada.

    Returns:
        function: Função decorada com inicialização de nomes dos terrenos.
    """
    def wrapper(self, *args, **kwargs):
        self.terrain_names = [
            "Jardim Sussurrante", "Jardim Uivante", "Caverna das Sombras", 
            "Caverna das Chamas", "Palácio de Coral", "Palácio das Marés", 
            "Templo da Lua", "Templo do Sol", "Rocha Fantasma", 
            "Floresta Carmesim", "Clareira do Crepúsculo", "Torre de Vigia"
        ]
        random.shuffle(self.terrain_names)
        return func(self, *args, **kwargs)
    return wrapper

# Decorator para status do terreno
def tile_status_decorator(func):
    """Decorator para definir o status dos terrenos.

    Args:
        func (function): Função a ser decorada.

    Returns:
        function: Função decorada com a lógica de status dos terrenos.
    """
    def wrapper(self, row, col, terrain_index, *args, **kwargs):
        tile_number = row * self.grid_size + col + 1
        status = "Normal"
        if self.sunk_tile_number and tile_number == self.sunk_tile_number:
            status = "Afundado"
        elif self.sinking_tiles and tile_number in self.sinking_tiles:
            status = "Afundando"
        return func(self, row, col, terrain_index, status, *args, **kwargs)
    return wrapper

# Decorator para tesouros nas diagonais
def treasure_decorator(func):
    """Decorator para criar e embaralhar os nomes dos tesouros.

    Args:
        func (function): Função a ser decorada.

    Returns:
        function: Função decorada com inicialização de nomes dos tesouros.
    """
    def wrapper(self, *args, **kwargs):
        self.treasure_names = ["Cálice da Maré", "Cristal de Fogo", "Estátua de Pedra", "Orbe Terrestre"]
        random.shuffle(self.treasure_names)
        return func(self, *args, **kwargs)
    return wrapper

class ForbiddenIslandBoard:
    """Representa o tabuleiro do jogo 'Ilha Proibida'.

    Args:
        root (Tk): Instância do tkinter.
        grid_size (int): Tamanho do grid do tabuleiro.
        tile_size (int): Tamanho visual de cada tile.

    Attributes:
        root (Tk): Instância do tkinter.
        grid_size (int): Tamanho do grid do tabuleiro.
        tile_size (int): Tamanho visual de cada tile.
        canvas_width (int): Largura do canvas.
        canvas_height (int): Altura do canvas.
        canvas (Canvas): Canvas do tkinter para desenho.
        black_tiles_numbers (set): Conjunto de números dos tiles não utilizáveis.
        terrain_names (list): Nomes dos terrenos.
        sunk_tile_number (int): Número do tile afundado.
        sinking_tiles (set): Conjunto de tiles afundando.
        treasure_names (list): Nomes dos tesouros.
    """
    def __init__(self, root, grid_size=6, tile_size=110):
        self.root = root
        self.grid_size = grid_size
        self.tile_size = tile_size
        self.canvas_width = grid_size * tile_size
        self.canvas_height = grid_size * tile_size
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        self.black_tiles_numbers = {1, 2, 5, 6, 7, 12, 25, 30, 31, 32, 35, 36}
        self.initialize_terrain_names()
        # Inicialmente, não há terrenos com status especial
        self.sunk_tile_number = None
        self.sinking_tiles = set()
        self.initialize_treasures()

    @assign_names_decorator
    def initialize_terrain_names(self):
        pass

    @treasure_decorator
    def initialize_treasures(self):
        pass

    @logging_decorator
    def draw_grid(self):
        terrain_index = 0
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.draw_tile(row, col, terrain_index)
                terrain_index += 1
        self.place_treasures()

    @tile_status_decorator
    def draw_tile(self, row, col, terrain_index, status):
        x1 = col * self.tile_size
        y1 = row * self.tile_size
        x2 = x1 + self.tile_size
        y2 = y1 + self.tile_size

        if row * self.grid_size + col + 1 not in self.black_tiles_numbers:
            self.canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='black')
            terrain_name = self.terrain_names[terrain_index % len(self.terrain_names)]
            self.canvas.create_text(x1 + self.tile_size/2, y1 + self.tile_size - 30, text=terrain_name, fill='black', font=('Helvetica', 8))

            if status == "Afundando":
                self.canvas.create_text(x1 + self.tile_size/2, y1 + self.tile_size - 15, text=status, fill='blue', font=('Helvetica', 8))
            elif status == "Afundado":
                self.canvas.create_text(x1 + self.tile_size/2, y1 + self.tile_size - 15, text=status, fill='red', font=('Helvetica', 8))

    def place_treasures(self):
        treasure_index = 0
        for i in range(self.grid_size):
            if i == 0 or i == self.grid_size - 1:
                for j in [0, self.grid_size - 1]:
                    if (i, j) not in self.black_tiles_numbers:
                        x1 = j * self.tile_size
                        y1 = i * self.tile_size
                        treasure_name = self.treasure_names[treasure_index % len(self.treasure_names)]
                        treasure_index += 1
                        self.canvas.create_text(x1 + self.tile_size/2, y1 + self.tile_size/2, text=treasure_name, fill='green', font=('Helvetica', 10, 'bold'))

# Inicialização da janela principal do tkinter
root = tk.Tk()
root.title("Ilha Proibida Grid de Terrenos")

# Criação da instância da classe ForbiddenIslandBoard e desenho do grid
board = ForbiddenIslandBoard(root)
board.draw_grid()

# Execução do loop do tkinter
root.mainloop()
