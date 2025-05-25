from .base import UIElement, COLOR
import pygame

class Text(UIElement):
    def __init__(self, text, font_size, position, color=COLOR["white"]):
        super().__init__(position, color, hover_color=COLOR["deep_sky_blue"], disabled_color=COLOR["dim_gray"])
        self.font = pygame.font.SysFont("Arial", font_size)
        self._text = text
        self.rendered_text = self.font.render(self.text, True, self.color)
        self._rect = self.rendered_text.get_rect(topleft=position)
        self._render()

    @property
    def rect(self): return self._rect

    @property
    def text(self): return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self._render()

    def _render(self): self.rendered_text = self.font.render(self.text, True, self.color)
    def _center_on(self, param): super()._center_on(param); return self
    def _center_x(self, param): super()._center_x(param); return self
    def _center_y(self, param): super()._center_y(param); return self
    def _set_position(self, position): super()._set_position(position); return self
    def _after_color_update(self, mouse_pos): self._render()
    def update(self, mouse_pos): super().update(mouse_pos)
    def draw(self, screen): screen.blit(self.rendered_text, self._rect)
    def draw_rect(self, screen): pygame.draw.rect(screen, self.color, self._rect, 2)
