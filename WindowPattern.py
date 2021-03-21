import tkinter as tk
from tkinter import filedialog


class WindowPattern:
    _destroy_objects = []

    def __init__(self, frame_name):
        self.window = tk.Tk()
        self.window.title(frame_name)
        self.window.geometry("600x600+300+100")

        file_menu = tk.Menu()
        file_menu.add_command(label="new", command=self._new_command)
        file_menu.add_command(label="open", command=self._open_command)
        file_menu.add_separator()
        file_menu.add_command(label="exit", command=self._exit_command)

        menu = tk.Menu()
        menu.add_cascade(label="File", menu=file_menu)
        self.window.config(menu=menu)

        self.window.mainloop()

    def _new_command(self):
        """Method invokes when new-button clicked"""
        pass

    def _open_command(self):
        """Method invokes when open-button clicked"""
        self.file = filedialog.askopenfilename(filetypes=(("Comma separate values", "*.csv"), ("all files", "*.*")))

    def _exit_command(self):
        self.window.quit()

    def _clean_frame(self):
        for obj in self._destroy_objects:
            obj.destroy()
