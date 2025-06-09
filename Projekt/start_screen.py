import tkinter as tk
from tkinter import ttk
from settings import load_settings, save_settings


def start_screen(on_start):
    """
    Wyświetla ekran startowy GUI do konfiguracji gry.

    Po kliknięciu "Start Game", zapisuje ustawienia i uruchamia aplikację.

    :param on_start: funkcja przyjmująca `settings`, uruchamiająca główną aplikację
    :type on_start: Callable[[dict], None]
    """
    settings = load_settings()
    root = tk.Tk()
    root.title("Gra w życie - Start")

    frame = ttk.Frame(root, padding=20)
    frame.pack()

    ttk.Label(frame, text="Grid Size (cols, rows):").grid(row=0, column=0, sticky="w")
    grid_entry = ttk.Entry(frame)
    grid_entry.insert(0, f"{settings['grid_size'][0]}, {settings['grid_size'][1]}")
    grid_entry.grid(row=0, column=1)

    ttk.Label(frame, text="Cell Size (px):").grid(row=1, column=0, sticky="w")
    cell_entry = ttk.Entry(frame)
    cell_entry.insert(0, str(settings['cell_size']))
    cell_entry.grid(row=1, column=1)

    ttk.Label(frame, text="Speed (gen/s):").grid(row=2, column=0, sticky="w")
    speed_entry = ttk.Entry(frame)
    speed_entry.insert(0, str(settings['speed']))
    speed_entry.grid(row=2, column=1)

    ttk.Label(frame, text="Theme:").grid(row=3, column=0, sticky="w")
    theme_var = tk.StringVar(value=settings['theme'])
    theme_menu = ttk.OptionMenu(frame, theme_var, settings['theme'], "light", "dark")
    theme_menu.grid(row=3, column=1)

    def on_ok():
        raw = grid_entry.get()
        try:
            parts = [p.strip() for p in raw.replace(';', ',').split(',')]
            if len(parts) != 2:
                raise ValueError
            cols, rows = map(int, parts)
        except Exception:
            tk.messagebox.showerror("Błąd", "Niepoprawny format siatki.")
            return
        settings['grid_size'] = [cols, rows]
        try:
            settings['cell_size'] = int(cell_entry.get())
            settings['speed'] = int(speed_entry.get())
        except ValueError:
            tk.messagebox.showerror("Błąd", "Rozmiar komórki i prędkość muszą być liczbami.")
            return
        settings['theme'] = theme_var.get()
        save_settings(settings)
        root.destroy()
        on_start(settings)

    ttk.Button(frame, text="Start Game", command=on_ok).grid(row=4, columnspan=2, pady=10)
    root.mainloop()