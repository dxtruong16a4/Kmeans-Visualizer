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

    def connect(self, event: str, callback: callable) -> None:
            """Connect a callback to an event with type checking."""
            if not isinstance(event, str):
                raise ValueError("Event must be a string")
            if not callable(callback):
                raise ValueError("Callback must be callable")
                
            if event in self._events:
                self._events[event].append(callback)
            else:
                raise KeyError(f"Unknown event type: {event}")

    def emit(self, *args, **kwargs) -> None:
            """Emit events with error handling."""
            for event, callbacks in self._events.items():
                if event in kwargs:
                    for callback in callbacks:
                        try:
                            callback(*args, **kwargs[event])
                        except Exception as e:
                            show_msg(LEVEL["ERROR"], f"Error in {event} callback: {str(e)}")

    def disconnect(self, event: str, callback: callable) -> None:
        """Disconnect a callback from an event."""
        if event in self._events:
            try:
                self._events[event].remove(callback)
            except ValueError:
                show_msg(LEVEL["WARNING"], f"Callback not found for event {event}")

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
            if hasattr(self._focused, '_active'):
                self._focused._active = False
                self._focused._update_color_state()
        self._focused = None

    def get_focused(self):
        return self._focused

focus_manager = FocusManager()

# ======= UIElement Base Class =======
class UIElement(ABC):
    """
    Abstract base class for UI elements in a pygame application.
    Provides basic functionality for positioning, coloring, and event handling.
    Enhanced with better visual feedback for interactions.
    """
    def __init__(self, position: Tuple[int, int] = (0, 0),
                 color: Tuple[int, int, int] = COLOR["light_blue"],
                 hover_color: Tuple[int, int, int] = COLOR["deep_sky_blue"],
                 active_color: Tuple[int, int, int] = COLOR["dodger_blue"],
                 disabled_color: Tuple[int, int, int] = COLOR["dim_gray"]):
        self.position = position
        # colors
        self._original_color = color
        self.color = color
        self.hover_color = hover_color
        self.active_color = active_color
        self.disabled_color = disabled_color
        # placeholder
        self._rect = pygame.Rect(0, 0, 0, 0)
        # flags
        self._enabled = True
        self._focused = False
        self._hovered = False
        self._active = False
        # signal
        self.signal = Signal()

    @property
    def enabled(self) -> bool:
        return self._enabled
    
    @enabled.setter
    def enabled(self, flag: bool) -> None:
        self._enabled = flag
        if flag:
            self.color = self._original_color
            self._active = False
        else:
            self.color = self.disabled_color
            self._active = False
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

    def _update_color_state(self) -> None:
        """Update the element's color based on its current state."""
        if not self._enabled:
            self.color = self.disabled_color
            return
            
        if self._active:
            self.color = self.active_color
        elif self._hovered:
            self.color = self.hover_color
        else:
            self.color = self._original_color

    def update(self, mouse_pos) -> None:
        """Update the UI element's state."""
        prev_hovered = self._hovered
        self._hovered = self._rect.collidepoint(mouse_pos) if self._enabled else False        
        if self._hovered != prev_hovered:
            if self._hovered:
                self.signal.emit(hovered={})
            self._update_color_state()
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
        prev_hovered = self._hovered
        self._hovered = self._rect.collidepoint(mouse_pos)
        if self._hovered != prev_hovered:
            if self._hovered:
                self.signal.emit(hovered={})
            self._update_color_state()
            self._after_color_update(mouse_pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._hovered:
                focus_manager.set_focus(self)
                self._active = True
                self._update_color_state()
                self.signal.emit(clicked={})
            elif self._focused:
                focus_manager.clear_focus()        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self._active:
                self._active = False
                self._update_color_state()
                if self._hovered:
                    self.signal.emit(clicked_release={})        
        if not self._focused and self._active:
            self._active = False
            self._update_color_state()
