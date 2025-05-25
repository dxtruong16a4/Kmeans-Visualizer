from .base import UIElement, COLOR
import pygame

class Label(UIElement):
    def __init__(self, text, font_size, position, color=COLOR["black"]):
        super().__init__(position, color)
        self._font = pygame.font.SysFont("Arial", font_size)
        self._text = text
        self._rect = pygame.Rect(position[0], position[1], 0, 0)
        self._render()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self._render()

    def _render(self):
        lines = self.text.split('\n')
        self.rendered_lines = [self._font.render(line, True, self.color) for line in lines]
        self._rect.width = max(r.get_width() for r in self.rendered_lines)
        self._rect.height = sum(r.get_height() for r in self.rendered_lines)

    def draw(self, screen):
        y = self._rect.top
        for line in self.rendered_lines:
            screen.blit(line, (self._rect.left, y))
            y += line.get_height()
