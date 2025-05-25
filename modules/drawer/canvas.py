from .base import UIElement, COLOR
import pygame

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
