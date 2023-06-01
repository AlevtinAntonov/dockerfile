import random as r
import sys
import os
import tkinter as tk
from tkinter import messagebox
from minimax_algorithm import get_symbol, find_best_move, update_state, is_draw


sys.setrecursionlimit(10000)
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

def build_gui(dim):
    root = tk.Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (dim[0] / 2)
    y = (screen_height / 2) - (dim[1] / 2)
    root.geometry(f'{dim[0]}x{dim[1]}+{int(x)}+{int(y)}')

    App(root, dim).pack(side="top", fill="both", expand=True)
    root.mainloop()


class App(tk.Frame):
    def __init__(self, parent, dim, **kw):
        super().__init__(parent, **kw)
        parent.minsize(dim[0], dim[1])
        parent.title("Крестики-Нолики")
        self.define_display_widgets()
        messagebox.showinfo("Приветствие", "Добро пожаловать в  игру! ")
        self.ttt_grid = Grid(self, {"tile_color": "black"})

    def define_display_widgets(self):
        self.reset = tk.Button(self, text="Новая игра", bg="grey", fg="white", command=self.reset_all)
        self.reset.pack()

    def reset_all(self):
        self.ttt_grid.disable_or_reset(disable=False)


class Grid(tk.Frame):

    def __init__(self, parent, config, **kw):
        super().__init__(parent, **kw)
        self.b = [[], [], []]
        self.config = config
        self.draw_grid()
        self.pack(pady=15)
        self.set_algo()

    def draw_grid(self):
        for i in range(3):
            for j in range(3):
                self.b[i].append(self.button())
                self.b[i][j].config(command=lambda row=i, col=j: self.fill(row, col))
                self.b[i][j].grid(row=i, column=j)

    def button(self):
        return tk.Button(self, bd=5, width=3, font=('arial', 30, 'bold'), relief=tk.GROOVE)

    def fill(self, i, j):
        self.b[i][j].config(text=get_symbol(self.turn), state=tk.DISABLED, fg="white")
        self.algo_value[i * 3 + j] = get_symbol(self.turn)
        status = self.check_if_game_ended("Игрок")
        if status: return
        self.turn = update_state(self.algo_value, i, j, self.turn)
        self.ai_move()

    def ai_move(self, start=None):
        if start:
            move, s = start, 0
        else:
            move, s = find_best_move(self.algo_value, True, self.turn)
        index = 0
        for i in range(9):
            if self.algo_value[i] != move[i]:
                index = i
                break
        self.algo_value = move
        self.b[index // 3][index % 3].config(text=get_symbol(self.turn), state=tk.DISABLED, fg="white")
        self.turn = not self.turn
        self.check_if_game_ended("Компьютер")

    def check_if_game_ended(self, player):
        if is_draw(self.algo_value):
            messagebox.showinfo("Информация", "        Ничья !!!           ")
            return True
        is_own, v = self.has_won()
        if is_own:
            self.highlight(v)
            messagebox.showinfo("Информация", "   {}    Победил !".format(player))

            return True
        return False

    def highlight(self, v):
        for x in v:
            self.b[x // 3][x % 3].config(fg="black", bg="red")
        self.disable_or_reset()

    def disable_or_reset(self, disable=True):
        for i in range(3):
            for j in range(3):
                if disable:
                    self.b[i][j].config(state=tk.DISABLED)
                else:
                    self.b[i][j].config(text="", bg=self.cget('bg'), fg="black", state=tk.NORMAL)
        if not disable: self.set_algo()

    def set_algo(self):
        val = messagebox.askquestion("Информация", "Могу я начать первым ?")
        self.algo_value = [-1] * 9
        self.turn = True
        if val == "yes":
            i = r.choice([2, 0, 6, 8, 1, 3, 5, 7])
            m = self.algo_value[:]
            m[i] = 'X'
            self.ai_move(m)

    def has_won(self):
        curr = self.algo_value
        for i in range(3):
            if curr[3 * i] == curr[3 * i + 1] == curr[3 * i + 2] != -1:
                return True, (3 * i, 3 * i + 1, 3 * i + 2)
            if curr[0 + i] == curr[3 + i] == curr[6 + i] != -1:
                return True, (0 + i, 3 + i, 6 + i)
        if curr[0] == curr[4] == curr[8] != -1:
            return True, (0, 4, 8)
        if curr[2] == curr[4] == curr[6] != -1:
            return True, (2, 4, 6)
        return False, None


if __name__ == '__main__':
    build_gui(dim=(400, 400))
