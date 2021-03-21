from tkinter import messagebox

import matplotlib
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.offsetbox import AnchoredText

from WindowPattern import WindowPattern
import tkinter as tk


class MainWindow(WindowPattern):
    str_eval = ""
    points_x = []
    points_y = []
    accuracy = 0.0
    limits = [0, 0]
    answers = []
    _pairs = []

    def __init__(self):
        super().__init__("Approximation Method")
        matplotlib.use("TkAgg")

    def _open_command(self):
        super()._open_command()
        super()._clean_frame()  # fix 16.03
        self.answers.clear()
        self.points_x.clear()
        self.points_y.clear()
        self._pairs.clear()
        self.limits = [0, 0]
        self._read_from_file()
        self._start_calculation()

    def _read_from_file(self):
        with open(self.file, 'r') as f:
            lines = f.readlines()
            self.str_eval = lines[0]
            self.accuracy, self.limits[0], self.limits[1] = lines[1].split(',')
            self.accuracy = float(self.accuracy)
            self.limits[0] = float(self.limits[0])
            self.limits[1] = float(self.limits[1])

    def _new_command(self):
        super()._clean_frame()
        self.answers.clear()
        self.points_x.clear()
        self.points_y.clear()
        self._pairs.clear()
        self.limits = [0, 0]

        line1 = tk.Frame(self.window)
        line2 = tk.Frame(self.window)
        line3 = tk.Frame(self.window)
        line3.pack(side=tk.BOTTOM)
        line2.pack(side=tk.BOTTOM)
        line1.pack(side=tk.BOTTOM)

        tmp = tk.Label(line1, text="f(x) = ")
        super()._destroy_objects.append(tmp)
        tmp.pack(side=tk.LEFT)

        self.inp_str = tk.StringVar()
        tmp = tk.Entry(line1, textvariable=self.inp_str, width=35)
        super()._destroy_objects.append(tmp)
        tmp.pack(side=tk.BOTTOM)

        tmp = tk.Label(line2, text="e = ")
        super()._destroy_objects.append(tmp)
        tmp.pack(side=tk.LEFT)

        self.acc_field = tk.Spinbox(line2, from_=0.0001, to=0.1, increment=0.0001)
        super()._destroy_objects.append(self.acc_field)
        self.acc_field.pack(side=tk.LEFT)

        tmp = tk.Label(line2, text="left lim = ")
        super()._destroy_objects.append(tmp)
        tmp.pack(side=tk.LEFT)

        self.left_lim_field = tk.StringVar()
        tmp = tk.Entry(line2, textvariable=self.left_lim_field)
        super()._destroy_objects.append(tmp)
        tmp.pack(side=tk.LEFT)

        tmp = tk.Label(line2, text="right lim = ")
        super()._destroy_objects.append(tmp)
        tmp.pack(side=tk.LEFT)

        self.right_lim_field = tk.StringVar()
        tmp = tk.Entry(line2, textvariable=self.right_lim_field)
        super()._destroy_objects.append(tmp)
        tmp.pack(side=tk.LEFT)

        tmp = tk.Button(line3, text="Расчитать", command=self._get_values)
        super()._destroy_objects.append(tmp)
        tmp.pack(side=tk.BOTTOM)

        super()._destroy_objects.append(line1)
        super()._destroy_objects.append(line2)
        super()._destroy_objects.append(line3)

    def _get_values(self):
        try:
            self.accuracy = float(self.acc_field.get())
            self.limits[0] = float(self.left_lim_field.get())
            self.limits[1] = float(self.right_lim_field.get())
            self.str_eval = self.inp_str.get()
        except Exception:
            messagebox.showerror("Ошибка", "Ожидается ввод числа")
            return  # Fix 15.03
        self.str_eval = self.str_eval.replace('^', '**').replace(',', '.')
        self._start_calculation()

    def _start_calculation(self):
        for i in np.arange(self.limits[0], self.limits[1] + 0.1, 0.1):
            self.points_x.append(i)

        for x in self.points_x:
            y = self._eval_func(x)
            if y is None:
                messagebox.showerror("Ошибка", "Ошибка в функции f(x)")
                break
            elif y == 'z':
                messagebox.showerror("Ошибка", "Деление на 0")
                break
            else:
                self.points_y.append(y)

        self._pairs = []
        for i in range(0, len(self.points_x) - 1):
            if not (round(self.points_y[i], 6) == 0):
                if self.points_y[i] > self.points_y[i + 1]:
                    if self.points_y[i + 1] < 0 < self.points_y[i]:
                        self._pairs.append((i + 1, i))
                elif self.points_y[i] < self.points_y[i + 1]:
                    if self.points_y[i] < 0 < self.points_y[i + 1]:
                        self._pairs.append((i, i + 1))
            else:
                self._pairs.append((i, i))

        for a, b in self._pairs:
            if a == b:
                self.answers.append(self._eval_func(self.points_x[a]))
                break
            x1 = self.points_x[a]
            x2 = self.points_x[b]
            while True:
                f_a = self._eval_func(x1)
                f_b = self._eval_func(x2)
                if abs(x2 - x1) < 2 * self.accuracy:
                    self.answers.append((x2 + x1) / 2)
                    break

                c = (x2 + x1) / 2
                f_c = self._eval_func(c)
                tmp = [abs(f_a), abs(f_b), abs(f_c)]
                if min(tmp) == abs(f_a):
                    new_a = x1
                elif min(tmp) == abs(f_b):
                    new_a = x2
                elif min(tmp) == abs(f_c):
                    new_a = c
                tmp.remove(min(tmp))
                if min(tmp) == abs(f_a):
                    new_b = x1
                elif min(tmp) == abs(f_b):
                    new_b = x2
                elif min(tmp) == abs(f_c):
                    new_b = c
                x1 = new_a
                x2 = new_b

        self._build_plot()

    def _eval_func(self, x):
        try:
            return eval(self.str_eval.replace('x', '({})'.format(x)))
        except ZeroDivisionError:
            return 'z'
        except Exception:
            return None

    def _build_plot(self):
        answ = [self._eval_func(item) for item in self.answers]
        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot()
        a.plot(self.points_x, self.points_y, "bo", self.answers, answ, "ro")
        a.scatter(self.answers, answ, c='r')
        for i in range(0, len(answ)):
            a.text(self.answers[i] + 0.2, answ[i] + 0.5, '{}'.format(round(self.answers[i], 4)))
        a.spines['left'].set_position('zero')
        a.spines['bottom'].set_position('zero')
        a.spines['top'].set_visible(False)
        a.spines['right'].set_visible(False)
        str_answ = ""
        for item in self.answers:
            str_answ += str(round(item, 5)) + '\n'
        a.add_artist(AnchoredText(str_answ, loc=2))

        canvas = FigureCanvasTkAgg(f)
        super()._destroy_objects.append(canvas._tkcanvas)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
