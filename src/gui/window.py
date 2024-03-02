import tkinter as tk

from abc import ABC, abstractmethod
from tkinter import filedialog


def choose_file():
    file_path = tk.filedialog.askopenfilename()
    if file_path:
        return file_path
    else:
        print('No file selected')
        return None


class Window(ABC):
    def __init__(self):
        self._title = None
        self._width = None
        self._height = None
        self._background_color = None

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def exit(self):
        pass

    @abstractmethod
    def add_label(self, text, config):
        pass

    @abstractmethod
    def add_button(self, text, command, config):
        pass

    @abstractmethod
    def set_title(self, title):
        pass

    @abstractmethod
    def set_background_color(self, background_color):
        pass

    @abstractmethod
    def set_size(self, width, height):
        pass


class TkWindow(Window):
    def __init__(self):
        super().__init__()
        self.__root = tk.Tk()

    def init(self):
        self.__root.mainloop()

    def exit(self):
        self.__root.destroy()

    def add_label(self, text, config):
        label = tk.Label(self.__root,
                         text=text,
                         background=self._background_color,
                         foreground=config['text_color'],
                         font=(config['font'], config['font_size']))
        label.pack()

    def add_button(self, text, command, config):
        button = tk.Button(self.__root,
                           text=text,
                           command=command,
                           width=config['width'],
                           height=config['height'])
        button.pack()

    def set_title(self, title):
        self.__root.title(title)
        self._title = title

    def set_background_color(self, background_color):
        self.__root.configure(background=background_color)
        self._background_color = background_color

    def set_size(self, width, height):
        self.__root.geometry('{}x{}'.format(width, height))
        self._width = width
        self._height = height
