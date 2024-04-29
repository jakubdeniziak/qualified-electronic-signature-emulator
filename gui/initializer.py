import json
from abc import ABC, abstractmethod


class GuiInitializer(ABC):
    def __init__(self):
        self._window = None
        self._config = None
        self._app_name = None
        self._width = None
        self._height = None
        self._background_color = None

    def _load_config(self):
        with open("../../gui/static/visual_identity.json", 'r') as file:
            self._config = json.load(file)

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def _set_window_params(self):
        pass

    @abstractmethod
    def _add_content(self):
        pass
