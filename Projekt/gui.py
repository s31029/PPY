import tkinter as tk
import threading
import time


class GameOfLifeApp:
    """
    Aplikacja GUI Conway's Game of Life.

    :param settings: słownik z ustawieniami gry (rozmiar siatki, prędkość, motyw)
    :type settings: dict
    """
    def __init__(self, settings):
        self.grid_w, self.grid_h = settings['grid_size']
        self.cell_size = settings['cell_size']
        self.speed = settings['speed']
        self.theme = settings['theme']
        self.running = False
        self.grid = [[0] * self.grid_w for _ in range(self.grid_h)]

        self.root = tk.Tk()
        self.root.title("Gra w życie")

        self.bg_color = 'white' if self.theme == 'light' else 'black'
        self.cell_color = 'black' if self.theme == 'light' else 'white'
        self.grid_color = '#ddd' if self.theme == 'light' else '#444'

        self.canvas = tk.Canvas(self.root, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(side='top', fill='both', expand=True)

        self.rects = []
        for y in range(self.grid_h):
            row = []
            for x in range(self.grid_w):
                x1, y1 = x*self.cell_size, y*self.cell_size
                x2, y2 = x1+self.cell_size, y1+self.cell_size
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.bg_color, outline=self.grid_color)
                row.append(rect)
            self.rects.append(row)

        self.canvas.bind("<Button-1>", self.toggle_cell)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(side='bottom', fill='x')
        tk.Button(btn_frame, text="Start", command=self.start).pack(side='left', padx=5, pady=5)
        tk.Button(btn_frame, text="Stop", command=self.stop).pack(side='left', padx=5, pady=5)
        tk.Button(btn_frame, text="Clear", command=self.clear).pack(side='left', padx=5, pady=5)

    def toggle_cell(self, event):
        """Zamienia stan komórki po kliknięciu."""
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        if 0 <= x < self.grid_w and 0 <= y < self.grid_h:
            self.grid[y][x] ^= 1
            color = self.cell_color if self.grid[y][x] else self.bg_color
            self.canvas.itemconfig(self.rects[y][x], fill=color)

    def step(self):
        """Wykonuje jedną generację gry zgodnie z regułami Conwaye'a."""
        new = [[0]*self.grid_w for _ in range(self.grid_h)]
        for y in range(self.grid_h):
            for x in range(self.grid_w):
                neighbors = sum(
                    self.grid[(y+dy)%self.grid_h][(x+dx)%self.grid_w]
                    for dx in (-1,0,1) for dy in (-1,0,1)
                    if not (dx==dy==0)
                )
                if self.grid[y][x] and neighbors in (2,3):
                    new[y][x] = 1
                elif not self.grid[y][x] and neighbors == 3:
                    new[y][x] = 1
        for y in range(self.grid_h):
            for x in range(self.grid_w):
                if new[y][x] != self.grid[y][x]:
                    color = self.cell_color if new[y][x] else self.bg_color
                    self.canvas.itemconfig(self.rects[y][x], fill=color)
        self.grid = new

    def run(self):
        """Uruchamia nieskończoną pętlę gry (w osobnym wątku)."""
        while self.running:
            start = time.time()
            self.step()
            elapsed = time.time() - start
            time.sleep(max(0, 1/self.speed - elapsed))

    def start(self):
        """Rozpoczyna symulację gry."""
        if not self.running:
            self.running = True
            threading.Thread(target=self.run, daemon=True).start()

    def stop(self):
        """Zatrzymuje symulację gry."""
        self.running = False

    def clear(self):
        """Czyści siatkę komórek (ustawia wszystkie na martwe)."""
        self.grid = [[0]*self.grid_w for _ in range(self.grid_h)]
        for row in self.rects:
            for rect in row:
                self.canvas.itemconfig(rect, fill=self.bg_color)