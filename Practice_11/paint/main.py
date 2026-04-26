import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Simple Paint")
    clock = pygame.time.Clock()

    radius = 15
    tool = 'pen'
    drawing = False
    start_pos = None

    points = []

    colors = {
        'black': (0, 0, 0),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 100, 255),
        'yellow': (255, 255, 0),
        'purple': (200, 0, 255),
        'orange': (255, 165, 0)
    }

    current_color = colors['black']

    screen.fill((255, 255, 255))

    font = pygame.font.SysFont("consolas", 16)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: tool = 'pen'
                elif event.key == pygame.K_e: tool = 'eraser'
                elif event.key == pygame.K_r: tool = 'rectangle'
                elif event.key == pygame.K_c: tool = 'circle'
                elif event.key == pygame.K_s: tool = 'square'
                elif event.key == pygame.K_t: tool = 'rt_triangle'
                elif event.key == pygame.K_q: tool = 'eq_triangle'
                elif event.key == pygame.K_d: tool = 'rhombus'

                elif event.key == pygame.K_1: current_color = colors['black']
                elif event.key == pygame.K_2: current_color = colors['red']
                elif event.key == pygame.K_3: current_color = colors['green']
                elif event.key == pygame.K_4: current_color = colors['blue']
                elif event.key == pygame.K_5: current_color = colors['yellow']
                elif event.key == pygame.K_6: current_color = colors['purple']
                elif event.key == pygame.K_7: current_color = colors['orange']

                elif event.key in (pygame.K_DELETE, pygame.K_BACKSPACE):
                    screen.fill((255, 255, 255))
                    points.clear()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                drawing = True
                start_pos = event.pos
                if tool == 'pen':
                    points = [event.pos]

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if drawing:
                    drawing = False
                    x1, y1 = start_pos
                    x2, y2 = event.pos

                    if tool == 'rectangle':
                        rect = pygame.Rect(min(x1, x2), min(y1, y2),
                                           abs(x2 - x1), abs(y2 - y1))
                        pygame.draw.rect(screen, current_color, rect)

                    elif tool == 'square':
                        side = min(abs(x2 - x1), abs(y2 - y1))
                        rect = pygame.Rect(x1, y1, side, side)
                        pygame.draw.rect(screen, current_color, rect)

                    elif tool == 'circle':
                        dx = x2 - x1
                        dy = y2 - y1
                        radius_circle = int((dx**2 + dy**2) ** 0.5)
                        pygame.draw.circle(screen, current_color, start_pos, radius_circle)

                    elif tool == 'rt_triangle':
                        pygame.draw.polygon(screen, current_color, [(x1, y1), (x2, y1), (x1, y2)])

                    elif tool == 'eq_triangle':
                        side = abs(x2 - x1)
                        height = int(side * math.sqrt(3) / 2)
                        p1 = (x1, y1)
                        p2 = (x1 + side, y1)
                        p3 = (x1 + side // 2, y1 - height)
                        pygame.draw.polygon(screen, current_color, [p1, p2, p3])

                    elif tool == 'rhombus':
                        cx = (x1 + x2) // 2
                        cy = (y1 + y2) // 2
                        dx = abs(x2 - x1) // 2
                        dy = abs(y2 - y1) // 2
                        points_rhomb = [
                            (cx, cy - dy),
                            (cx + dx, cy),
                            (cx, cy + dy),
                            (cx - dx, cy)
                        ]
                        pygame.draw.polygon(screen, current_color, points_rhomb)

                    points.clear()
                    start_pos = None

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if tool == 'pen':
                        points.append(event.pos)
                        points = points[-1024:]
                    elif tool == 'eraser':
                        pygame.draw.circle(screen, (255, 255, 255), event.pos, radius + 8)

        if tool == 'pen' and len(points) > 1:
            for i in range(len(points) - 1):
                drawLineBetween(screen, points[i], points[i + 1], radius, current_color)

        # ───────── UI ─────────

        col1 = [
            "TOOLS",
            "P - Pen",
            "E - Eraser",
            "DEL - Clear"
        ]

        col2 = [
            "SHAPES",
            "R - Rectangle",
            "S - Square",
            "C - Circle",
            "T - Right Triangle",
            "Q - Equilateral",
            "D - Rhombus"
        ]

        col3 = [
            "COLORS",
            "1 Black",
            "2 Red",
            "3 Green",
            "4 Blue",
            "5 Yellow",
            "6 Purple",
            "7 Orange"
        ]

        for i, text in enumerate(col1):
            screen.blit(font.render(text, True, (80, 80, 80)), (10, 10 + i * 18))

        for i, text in enumerate(col2):
            screen.blit(font.render(text, True, (80, 80, 80)), (300, 10 + i * 18))

        for i, text in enumerate(col3):
            screen.blit(font.render(text, True, (80, 80, 80)), (550, 10 + i * 18))

        status = font.render(f"Tool: {tool.upper()}", True, (0, 0, 0))
        screen.blit(status, (10, 570))

        pygame.display.flip()
        clock.tick(120)


def drawLineBetween(screen, start, end, width, color):
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy)) + 1

    for i in range(iterations):
        t = i / iterations
        x = int(start[0] * (1 - t) + end[0] * t)
        y = int(start[1] * (1 - t) + end[1] * t)
        pygame.draw.circle(screen, color, (x, y), width)


if __name__ == "__main__":
    main()