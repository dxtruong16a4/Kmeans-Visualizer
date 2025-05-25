# Singleton decorator
def singleton(func):
    has_run = {"status": False}

    def wrapper(*args, **kwargs):
        if not has_run["status"]:
            has_run["status"] = True
            return func(*args, **kwargs)
        else:
            from modules.utils import show_msg, LEVEL
            show_msg(LEVEL["ERROR"], "Game is already running!")
    return wrapper

@singleton
def run_game(title="untitled"):
    from modules.constants import COLOR, FPS, WINDOW_WIDTH, WINDOW_HEIGHT
    from modules.drawer import Text, Button, Label, Canvas
    import pygame

    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(title)
    clock = pygame.time.Clock()

    button = Button((620, 20), (150, 50), COLOR["primary"], Text("Run", 20, (0, 0), COLOR["black"]))
    boundary_button = Button((620, 80), (150, 50), COLOR["steel_blue"], Text("Draw Boundary", 20, (0, 0), COLOR["black"]))
    remove_button = Button((620, 150), (150, 50), COLOR["warning"], Text("Remove Last Point", 20, (0, 0), COLOR["black"]))
    clear_button = Button((620, 210), (150, 50), COLOR["secondary"], Text("Clear Canvas", 20, (0, 0), COLOR["black"]))

    k = 3
    k_label = Label(f"k = {k}", 24, (670, 280))
    k_inc_button = Button((730, 275), (40, 40), COLOR["add"], Text("+", 30, (0, 0)))
    k_dec_button = Button((620, 275), (40, 40), COLOR["warning"], Text("-", 30, (0, 0)))

    points_info_label = Label("Points: 0", 20, (620, 340))
    cluster_labels = []

    canvas = Canvas((0, 0), (600, 600), COLOR["white"])
    show_boundary = False

    def update_points_info():
        total = len(canvas.points)
        cluster_labels.clear()
        points_info_label.text = (f"Points: {total}")
        if hasattr(canvas, "_labels") and hasattr(canvas, "centroids"):
            from collections import Counter
            counts = Counter(canvas._labels)
            k = len(canvas.centroids)
            cluster_colors = []
            for i in range(k):
                for idx, label in enumerate(canvas._labels):
                    if label == i:
                        cluster_colors.append(canvas.points[idx][2])
                        break
                else:
                    cluster_colors.append((0, 0, 0))
            for i in range(k):
                color = cluster_colors[i]
                cx, cy = canvas.centroids[i]
                text = f"C{i+1}: {counts[i]} point(s) - Centroid: ({int(cx)}, {int(cy)})"
                label = Label(text, 20, (620, 360 + i * 24), color=color)
                cluster_labels.append(label)

    def run_kmeans_on_canvas():
        canvas.run_kmeans(k=k)
        update_points_info()
    button.connect("clicked", run_kmeans_on_canvas)
    remove_button.connect("clicked", canvas.remove_last_point)
    clear_button.connect("clicked", canvas.clear_canvas)

    def increase_k():
        nonlocal k
        if k < 10:
            k += 1
            k_label.set_text(f"k = {k}")

    def decrease_k():
        nonlocal k
        if k > 1:
            k -= 1
            k_label.set_text(f"k = {k}")

    k_inc_button.connect("clicked", increase_k)
    k_dec_button.connect("clicked", decrease_k)

    def toggle_boundary():
        nonlocal show_boundary
        show_boundary = not show_boundary
    boundary_button.connect("clicked", toggle_boundary)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            button.execute(event, pygame.mouse.get_pos())
            boundary_button.execute(event, pygame.mouse.get_pos())
            remove_button.execute(event, pygame.mouse.get_pos())
            clear_button.execute(event, pygame.mouse.get_pos())
            k_inc_button.execute(event, pygame.mouse.get_pos())
            k_dec_button.execute(event, pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONDOWN:
                canvas.add_point(event.pos)
                update_points_info()
            mouse_pos = pygame.mouse.get_pos()
            canvas.hovered_point_index = canvas.get_point_near(mouse_pos)

        screen.fill(COLOR["background"])

        button.draw(screen)
        boundary_button.draw(screen)
        remove_button.draw(screen)
        clear_button.draw(screen)
        k_label.draw(screen)
        k_inc_button.draw(screen)
        k_dec_button.draw(screen)
        points_info_label.draw(screen)
        for label in cluster_labels:
            label.draw(screen)
        button.update(pygame.mouse.get_pos())
        boundary_button.update(pygame.mouse.get_pos())
        remove_button.update(pygame.mouse.get_pos())
        clear_button.update(pygame.mouse.get_pos())
        k_inc_button.update(pygame.mouse.get_pos())
        k_dec_button.update(pygame.mouse.get_pos())
        
        canvas.draw(screen)
        canvas.update(pygame.mouse.get_pos())
        if show_boundary:
            canvas.draw_clusters_boundary(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    run_game("Kmean")