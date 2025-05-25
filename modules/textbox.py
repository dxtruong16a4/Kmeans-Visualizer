from uielement import UIElement, Self, Tuple
import pygame

class TextBox(UIElement):
    def __init__(self, text: str, font_size: int, size: Tuple[int, int], position: Tuple[int, int], color: Tuple[int, int, int]):
        super().__init__(position, color)
        self.font = pygame.font.SysFont(None, font_size)
        self.text = text
        self._visible_text = ""
        self.width, self.height = size
        self._rect = pygame.Rect(position, size)

        self.active = False
        self.caret_pos = len(text)
        self.caret_visible = True
        self._caret_timer = 0
        self._caret_interval = 12000  # ms
        self.scroll_offset = 0

        self._render()

    def _render(self):
        self.rendered_text = self.font.render(self.text, True, self.color)
        self._update_scroll_offset()

    def _update_scroll_offset(self):
        caret_x = self.font.size(self.text[:self.caret_pos])[0]
        max_x = self._rect.width - 10
        if caret_x - self.scroll_offset > max_x:
            self.scroll_offset = caret_x - max_x
        elif caret_x - self.scroll_offset < 0:
            self.scroll_offset = caret_x

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self._rect, 2)
        padding = 5
        text_surface = self.font.render(self.text, True, self.color)

        screen.blit(text_surface, (self._rect.x + padding - self.scroll_offset, self._rect.y + padding))

        if self.active and self.caret_visible:
            caret_x = self.font.size(self.text[:self.caret_pos])[0] - self.scroll_offset
            caret_rect = pygame.Rect(
                self._rect.x + padding + caret_x,
                self._rect.y + padding,
                2,
                self.font.get_height()
            )
            pygame.draw.rect(screen, (255, 255, 255), caret_rect)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and hasattr(event, 'pos'):
            self.active = self._rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE and self.caret_pos > 0:
                self.text = self.text[:self.caret_pos - 1] + self.text[self.caret_pos:]
                self.caret_pos -= 1
            elif event.key == pygame.K_LEFT:
                if self.caret_pos > 0:
                    self.caret_pos -= 1
            elif event.key == pygame.K_RIGHT:
                if self.caret_pos < len(self.text):
                    self.caret_pos += 1
            elif event.unicode.isprintable():
                self.text = self.text[:self.caret_pos] + event.unicode + self.text[self.caret_pos:]
                self.caret_pos += 1
            self._render()

    def update(self) -> None:
        self.color = self.hover_color if self.active else self._original_color

        self._caret_timer += pygame.time.get_ticks() % 1000
        if self._caret_timer >= self._caret_interval:
            self.caret_visible = not self.caret_visible
            self._caret_timer = 0

    def _set_position(self, position: Tuple[int, int]) -> Self:
        self._rect.topleft = position
        return self

    def _center_on(self, param) -> Self:
        self._rect.center = param
        return self

    def _center_x(self, param) -> Self:
        self._rect.centerx = param
        return self

    def _center_y(self, param) -> Self:
        self._rect.centery = param
        return self

# usage example

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    textbox = TextBox(
        text="Hello",
        font_size=28,
        size=(200, 40),
        position=(200, 200),
        color=(0, 255, 255)
    )

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            textbox.handle_event(event)

        screen.fill((0, 0, 0))
        textbox.update()
        textbox.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()