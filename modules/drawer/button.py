from .base import UIElement, COLOR, show_msg
import pygame

class Button(UIElement):
    def __init__(self, position, size, color, text=None, image_path=None):
        super().__init__(position, color)
        self._rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self._text = text
        self._image = None
        if image_path: self._load_image(image_path)
        if text: self._center_text()

    def _load_image(self, path):
        try:
            self._image = pygame.image.load(path).convert_alpha()
            self._image = pygame.transform.scale(self._image, self._rect.size)
        except Exception as e:
            show_msg(2, f"Failed to load image '{path}': {e}")
            self._image = None

    def _center_text(self):
        if self._text:
            self._text._rect.center = self._rect.center

    def _center_on(self, param): super()._center_on(param); self._center_text(); return self
    def _center_x(self, param): super()._center_x(param); self._center_text(); return self
    def _center_y(self, param): super()._center_y(param); self._center_text(); return self
    def _set_position(self, position): super()._set_position(position); self._center_text(); return self
    def _after_color_update(self, mouse_pos): 
        if self._text: self._text.update(mouse_pos)
    def update(self, mouse_pos): super().update(mouse_pos)
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self._rect)
        pygame.draw.rect(screen, COLOR["black"], self._rect, 2)
        if self._image: screen.blit(self._image, self._rect)
        if self._text: self._text.draw(screen)
