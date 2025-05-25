from abc import ABC, abstractmethod
from .constants import COLOR
from typing import Tuple, Optional, Self
from .utils import show_msg, LEVEL
import pygame

# ======= Signal Class =======
class Signal:
    def __init__(self):
        self._events = {
            "clicked": [],
            "hovered": [],
            "scrolled": [],
            "dragged": []
        }

    def connect(self, event, callback):
        if event in self._events:
            self._events[event].append(callback)

    def emit(self, *args, **kwargs):
        for event, callbacks in self._events.items():
            if event in kwargs:
                for callback in callbacks:
                    callback(*args, **kwargs[event])

    def disconnect(self, event, callback):
        if event in self._events:
            if callback in self._events[event]:
                self._events[event].remove(callback)

# ======= Focus Manager =======
class FocusManager:
    def __init__(self):
        self._focused = None

    def set_focus(self, ui_element):
        if self._focused and self._focused is not ui_element:
            self._focused.clear_focus()
        self._focused = ui_element
        ui_element.set_focus()

    def clear_focus(self):
        if self._focused:
            self._focused.clear_focus()
        self._focused = None

    def get_focused(self):
        return self._focused

focus_manager = FocusManager()

# ======= UIElement Base Class =======
class UIElement(ABC):
    """
    Abstract base class for UI elements in a pygame application.
    Provides basic functionality for positioning, coloring, and event handling.
    """
    def __init__(self, position: Tuple[int, int] = (0, 0),
                 color: Tuple[int, int, int] = COLOR["light_blue"],
                 hover_color: Tuple[int, int, int] = COLOR["deep_sky_blue"],
                 disabled_color: Tuple[int, int, int] = COLOR["dim_gray"]):
        self.position = position
        # colors
        self.color = color
        self.hover_color = hover_color
        self.disabled_color = disabled_color
        self._original_color = color
        # placeholder
        self._rect = pygame.Rect(0, 0, 0, 0)
        # flags
        self._enabled = True
        self._focused = False
        self._hovered = False
        # signal
        self.signal = Signal()

    @property
    def enabled(self) -> None:
        return self._enabled
    
    @enabled.setter
    def enabled(self, flag: bool) -> None:
        self._enabled = flag
        self.color = self._original_color if flag else self.disabled_color
        if not flag:
            self.signal.emit(disabled=[])
            show_msg(LEVEL["WARNING"], "UIElement is disabled.")

    def _center_on(self, param) -> Self:
        """Center the UI element on a given parameter."""
        if isinstance(param, (pygame.Surface, pygame.Rect)):
            self._rect.center = param.get_rect().center if isinstance(param, pygame.Surface) else param.center
        elif isinstance(param, tuple) and len(param) == 2:
            self._rect.center = param
        else:
            show_msg(LEVEL["ERROR"], "Invalid parameter type for center_on. Expected pygame.Surface, pygame.Rect or tuple.")
            return self
        self.position = self._rect.topleft
        return self

    def _center_x(self, param) -> Self:
        """Center the UI element on the x-axis."""
        if not isinstance(param, (int, float)):
            show_msg(LEVEL["ERROR"], "Invalid type for center_x. Expected int or float.")
            return self
        self._rect.centerx = param
        self.position = self._rect.topleft
        return self

    def _center_y(self, param) -> Self:
        """Center the UI element on the y-axis."""
        if not isinstance(param, (int, float)):
            show_msg(LEVEL["ERROR"], "Invalid type for center_y. Expected int or float.")
            return self
        self._rect.centery = param
        self.position = self._rect.topleft
        return self

    def _set_position(self, position) -> Self:
        """Set the position of the UI element."""
        if not isinstance(position, tuple) or len(position) != 2:
            show_msg(LEVEL["ERROR"], "Invalid position type. Expected tuple of (x, y).")
            return self
        self._rect.topleft = position
        self.position = position
        return self

    def update(self, mouse_pos) -> None:
        """Update the UI element's state."""
        if not self._enabled:
            self.color = self.disabled_color
            self._after_color_update(mouse_pos)
            return

        is_hovering = self._rect.collidepoint(mouse_pos)
        if is_hovering and not self._hovered:
            self.color = self.hover_color
            self._hovered = True
            self.signal.emit(hovered={})
            self._after_color_update(mouse_pos)
        elif not is_hovering and self._hovered:
            self.color = self._original_color
            self._hovered = False
            self._after_color_update(mouse_pos)

    def _after_color_update(self, mouse_pos) -> None:
        """Hook method for child classes to implement custom behavior after color updates."""
        pass

    @abstractmethod
    def draw(self, screen) -> None:
        """Draw the UI element on the screen."""
        pass

    def set_focus(self) -> None:
        self._focused = True

    def clear_focus(self) -> None:
        self._focused = False

    def is_focused(self) -> bool:
        return self._focused

    def move(self, dx, dy) -> None:
        if not isinstance(dx, (int, float)) or not isinstance(dy, (int, float)):
            show_msg(LEVEL["ERROR"], "Invalid type for move. Expected int or float.")
            return
        self._rect = self._rect.move(dx, dy)

    def move_ip(self, dx, dy) -> Self:
        if not isinstance(dx, (int, float)) or not isinstance(dy, (int, float)):
            show_msg(LEVEL["ERROR"], "Invalid type for move_ip. Expected int or float.")
            return self
        self._rect.move_ip(dx, dy)
        return self

    def connect(self, event: str, callback: callable) -> None:
        self.signal.connect(event, callback)
        show_msg(LEVEL["SUCCESS"], f"Connected {event} signal to {callback.__name__}")

    def disconnect(self, event: str, callback: callable) -> None:
        self.signal.disconnect(event, callback)
        show_msg(LEVEL["SUCCESS"], f"Disconnected {event} signal from {callback.__name__}")

    def execute(self, event: pygame.event.Event, mouse_pos: tuple[int, int]) -> None:
        if not self._enabled:
            return

        self._hovered = self._rect.collidepoint(mouse_pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._hovered:
                focus_manager.set_focus(self)
                self.signal.emit(clicked={})
            else:
                if self._focused:
                    focus_manager.clear_focus()
