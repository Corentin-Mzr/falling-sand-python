import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import time


class FallingSand:
    def __init__(self, width: int, height: int):
        self.array = np.zeros((height, width), dtype=np.uint8)
        self.nx = width
        self.ny = height

    def update(self):
        for i in range(self.ny - 1, 0, -1):
            # Cells that contain a grain of sand on previous height
            previous_height, = np.where(self.array[i - 1] > 0)

            # Cells that contain a grain of sand on current height
            current_height, = np.where(self.array[i] > 0)

            # Check where the grains of sand can fall
            for j in previous_height:
                # Clear cell
                self.array[i - 1, j] = 0

                # Below cell is not filled yet, sand can fall
                if j not in current_height:
                    self.array[i, j] = 1

                # Below cell is already filled, check if cells next to it are also filled
                # Left column
                elif j == 0:
                    if self.array[i, j + 1] == 0:
                        self.array[i, j + 1] = 1
                    else:
                        self.array[i - 1, j] = 1

                # Right column
                elif j == self.ny - 1:
                    if self.array[i, j - 1] == 0:
                        self.array[i, j - 1] = 1
                    else:
                        self.array[i - 1, j] = 1

                # Other cases
                elif 0 < j < self.ny - 1:
                    if self.array[i, j - 1] == self.array[i, j + 1] == 0:
                        self.array[i, np.random.choice([j - 1, j + 1])] = 1
                    elif self.array[i, j - 1] == 0:
                        self.array[i, j - 1] = 1
                    elif self.array[i, j + 1] == 0:
                        self.array[i, j + 1] = 1
                    else:
                        self.array[i - 1, j] = 1

                # All below cells are already filled
                else:
                    self.array[i - 1, j] = 1


class Display:
    def __init__(self, mat: FallingSand):
        self.mat = mat

        self.fig, self.ax = plt.subplots()
        self.im = self.ax.imshow(self.mat.array, cmap='gray', vmin=0, vmax=1, interpolation=None)
        self.ax.grid(True, which='both', color='gray', linewidth=1, linestyle='--')
        self.ax.axis('off')

        plt.show(block=False)

    def draw(self):
        self.im.set_data(self.mat.array)
        self.fig.canvas.flush_events()
        self.fig.canvas.draw()
        time.sleep(1.0 / 60.0)

    def run(self):
        is_running = True
        while is_running:
            self.mat.update()
            self.draw()
            if not plt.fignum_exists(self.fig.number):
                is_running = False


class Controller:
    def __init__(self, display: Display):
        self.display = display

        self.cid_press = self.display.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_release = self.display.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_drag = self.display.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_drag)

        self.dragging = False

    def on_press(self, event):
        if event.button == 1:  # Left mouse button
            self.dragging = True

    def on_release(self, event):
        if event.button == 1:
            self.dragging = False

    def on_drag(self, event):
        if self.dragging and event.button == 1:
            def generate_sand_at_position(x, y):
                if x is None or y is None:
                    return
                self.display.mat.array[int(y), int(x)] = 1

            generate_sand_at_position(event.xdata, event.ydata)


def main():
    matplotlib.use('TkAgg')
    nx = 50
    ny = 50

    falling_sand = FallingSand(nx, ny)
    matplotlib_window = Display(falling_sand)
    controller = Controller(matplotlib_window)

    controller.display.run()


if __name__ == '__main__':
    main()
