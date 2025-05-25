from .uielement import UIElement, Optional, COLOR, show_msg
import pygame

# class Text
class Text(UIElement):
    def __init__(self, text, font_size, position, color = COLOR["white"]):
        super().__init__(position, color, 
                         hover_color=COLOR["deep_sky_blue"],
                         disabled_color=COLOR["dim_gray"])
        self.font = pygame.font.SysFont("Arial", font_size)
        self.text = text
        self.rendered_text = self.font.render(self.text, True, self.color)
        self._rect = self.rendered_text.get_rect(topleft=position)
        self._render()

    def _render(self) -> None:
        self.rendered_text = self.font.render(self.text, True, self.color)

    def _center_on(self, param):
        super()._center_on(param)
        return self

    def _center_x(self, param):
        super()._center_x(param)
        return self

    def _center_y(self, param):
        super()._center_y(param)
        return self

    def _set_position(self, position):
        super()._set_position(position)
        return self

    def _after_color_update(self, mouse_pos) -> None:
        self._render()

    def update(self, mouse_pos) -> None:
        super().update(mouse_pos)      

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.rendered_text, self._rect)

    def draw_rect(self, screen) -> None:
        pygame.draw.rect(screen, self.color, self._rect, 2)


# class Button
class Button(UIElement):
    def __init__(self, position, size, color, text: Optional[Text] = None, image_path = None):
        super().__init__(position, color)
        self._rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.text = text
        self.image = None
        if image_path:
            self._load_image(image_path)
        if text:
            self.text._rect.center = self._rect.center

    def _load_image(self, image_path: str) -> None:
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, self._rect.size)
        except pygame.error as e:
            show_msg(2, f"Failed to load image '{image_path}': {e}")
            self.image = None

    def _center_on(self, param):
        super()._center_on(param)
        if self.text:
            self.text._rect.center = self._rect.center
        return self

    def _center_x(self, param):
        super()._center_x(param)
        if self.text:
            self.text._rect.centerx = param
        return self

    def _center_y(self, param):
        super()._center_y(param)
        if self.text:
            self.text._rect.centery = param
        return self

    def _set_position(self, position):
        super()._set_position(position)
        if self.text:
            self.text._rect.center = self._rect.center
        return self

    def _after_color_update(self, mouse_pos) -> None:
        if self.text:
            self.text.update(mouse_pos)

    def update(self, mouse_pos) -> None:
        super().update(mouse_pos)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.color, self._rect)
        pygame.draw.rect(screen, COLOR["black"], self._rect, 2)
        if self.image:
            screen.blit(self.image, self._rect)
        if self.text:
            self.text.draw(screen)


# class Canvas

class Canvas(UIElement):
    def __init__(self, position, size, color=COLOR["white"]):
        super().__init__(position, color)
        self.size = size
        self._rect = pygame.Rect(*position, *size)
        self.points: list[tuple[int, int, tuple[int, int, int]]] = []
        self.hover_color = COLOR["light_gray"]
        self.point_hover_color = COLOR["black"]
        self.hovered_point_index = None

    def add_point(self, pos: tuple[int, int], color: tuple[int, int, int] = COLOR["black"]) -> None:
        """Add point with color if it's inside the canvas."""
        if self._rect.collidepoint(pos):
            self.points.append((pos[0], pos[1], color))
            if hasattr(self, "_labels"):
                del self._labels
            if hasattr(self, "centroids"):
                del self.centroids

    def change_point_color(self, index: int, color: tuple[int, int, int]) -> None:
        """Change color of point at given index."""
        if 0 <= index < len(self.points):
            x, y, _ = self.points[index]
            self.points[index] = (x, y, color)

    def remove_last_point(self):
        if self.points:
            self.points.pop()
            if hasattr(self, "_labels"):
                del self._labels
            if hasattr(self, "centroids"):
                del self.centroids

    def remove_point_near(self, pos: tuple[int, int], radius: int = 10):
        old_len = len(self.points)
        self.points = [
            (x, y, c) for (x, y, c) in self.points
            if (x - pos[0])**2 + (y - pos[1])**2 > radius**2
        ]
        if len(self.points) != old_len:
            if hasattr(self, "_labels"):
                del self._labels
            if hasattr(self, "centroids"):
                del self.centroids

    def clear_points(self) -> None:
        """Remove all points from canvas."""
        self.points.clear()
        if hasattr(self, "_labels"):
            del self._labels
        if hasattr(self, "centroids"):
            del self.centroids

    def clear_canvas(self) -> None:
        """Remove all points and centroids from canvas."""
        self.points.clear()
        if hasattr(self, "_labels"):
            del self._labels
        if hasattr(self, "centroids"):
            del self.centroids

    def get_point_near(self, pos: tuple[int, int], radius: int = 10) -> int | None:
        """Get the index of a point near the given position."""
        for i, (x, y, _) in enumerate(self.points):
            if (x - pos[0])**2 + (y - pos[1])**2 < radius**2:
                return i
        return None

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.color, self._rect)
        for i, (x, y, color) in enumerate(self.points):
            point_color = self.point_hover_color if i == self.hovered_point_index else color
            pygame.draw.circle(screen, point_color, (x, y), 5)
        if hasattr(self, "centroids"):
            for cx, cy in self.centroids:
                pygame.draw.circle(screen, COLOR["black"], (int(cx), int(cy)), 10, 2)

        if self.hovered_point_index is not None:
            x, y, _ = self.points[self.hovered_point_index]
            font = pygame.font.Font(None, 24)
            text_surface = font.render(f"({x}, {y})", True, COLOR["black"])
            screen.blit(text_surface, (x + 10, y + 10))

    def draw_clusters_boundary(self, screen: pygame.Surface):
        """Draw convex hull boundary for each cluster if kmeans has been run."""
        if not hasattr(self, "centroids") or not hasattr(self, "points") or not self.points:
            return
        try:
            import numpy as np
            from scipy.spatial import ConvexHull
        except ImportError:
            return

        if not hasattr(self, "_labels"):
            return

        data = np.array([[x, y] for x, y, _ in self.points])
        labels = self._labels
        if len(data) != len(labels):
            return

        k = len(self.centroids)
        for cluster_idx in range(k):
            cluster_points = data[labels == cluster_idx]
            if len(cluster_points) >= 3:
                hull = ConvexHull(cluster_points)
                hull_points = cluster_points[hull.vertices]
                pygame.draw.polygon(screen, (0, 0, 0), hull_points, 2)

    def run_kmeans(self, k=3, colors=None):
        import numpy as np
        from sklearn.cluster import KMeans
        if colors is None:
            base_colors = [
                COLOR["red"],
                COLOR["lime"],
                COLOR["blue"],
                COLOR["cyan"],
                COLOR["magenta"],
                COLOR["orange"],
                COLOR["green_yellow"],
                COLOR["deep_pink"],
                COLOR["steel_blue"],
                COLOR["brown"],
            ]
            colors = base_colors[:10]
        if len(self.points) < k:
            return

        data = np.array([[x, y] for x, y, _ in self.points])
        kmeans = KMeans(n_clusters=k, n_init=10)
        labels = kmeans.fit_predict(data)
        for i, label in enumerate(labels):
            self.change_point_color(i, colors[label % len(colors)])
        self.centroids = kmeans.cluster_centers_
        self._labels = np.array(labels)


# class Label
class Label(UIElement):
    def __init__(self, text, font_size, position, color=COLOR["black"]):
        super().__init__(position, color)
        self.font = pygame.font.SysFont("Arial", font_size)
        self.text = text
        self.font_size = font_size
        self._rect = pygame.Rect(position[0], position[1], 0, 0)
        self._render()

    def set_text(self, text):
        self.text = text
        self._render()

    def _render(self):
        # Hỗ trợ xuống dòng
        lines = self.text.split('\n')
        self.rendered_lines = [self.font.render(line, True, self.color) for line in lines]
        width = max(line.get_width() for line in self.rendered_lines)
        height = sum(line.get_height() for line in self.rendered_lines)
        self._rect.width = width
        self._rect.height = height

    def draw(self, screen: pygame.Surface) -> None:
        y = self._rect.top
        for line in self.rendered_lines:
            screen.blit(line, (self._rect.left, y))
            y += line.get_height()

# Example usage for k control (to be used in main.py):
# k_label = Label("k = 3", 24, (420, 200))
# k_inc_button = Button((530, 200), (40, 40), COLOR["lime"], Text("+", 30, (0, 0)))
# k_dec_button = Button((370, 200), (40, 40), COLOR["red"], Text("-", 30, (0, 0)))