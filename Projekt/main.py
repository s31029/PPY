from gui import GameOfLifeApp
from start_screen import start_screen


def main():
    """
    Główna funkcja uruchamiająca ekran startowy,
    a następnie aplikację Game of Life.
    """
    def launch(settings: dict):
        app = GameOfLifeApp(settings)
        app.root.mainloop()

    start_screen(launch)


if __name__ == '__main__':
    main()