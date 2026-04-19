import pygame

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

    current_color = colors['blue']

    screen.fill((255, 255, 255))

    font = pygame.font.SysFont("consolas", 16)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: tool = 'pen'
                elif event.key == pygame.K_r: tool = 'rectangle'
                elif event.key == pygame.K_c: tool = 'circle'
                elif event.key == pygame.K_e: tool = 'eraser'

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

                    if tool == 'rectangle' and start_pos:
                        x1, y1 = start_pos
                        x2, y2 = event.pos
                        rect = pygame.Rect(min(x1, x2), min(y1, y2),
                                           abs(x2 - x1), abs(y2 - y1))
                        pygame.draw.rect(screen, current_color, rect)

                    elif tool == 'circle' and start_pos:
                        dx = event.pos[0] - start_pos[0]
                        dy = event.pos[1] - start_pos[1]
                        radius_circle = int((dx**2 + dy**2) ** 0.5)
                        pygame.draw.circle(screen, current_color, start_pos, radius_circle)

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

        instructions = [
            "P - Кисть    R - Прямоугольник    C - Круг    E - Ластик",
            "1-Black  2-Red  3-Green  4-Blue  5-Yellow  6-Purple  7-Orange",
            "DELETE / BACKSPACE - Очистить экран"
        ]

        for i, text in enumerate(instructions):
            txt = font.render(text, True, (80, 80, 80))
            screen.blit(txt, (10, 10 + i * 22))

        status = font.render(f"Tool: {tool.upper()}   Color: {current_color}", True, (0, 0, 0))
        screen.blit(status, (10, 570))

        pygame.display.flip()
        clock.tick(120)


def drawLineBetween(screen, start, end, width, color):
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy)) + 1

    for i in range(iterations):
        progress = i / iterations
        x = int(start[0] * (1 - progress) + end[0] * progress)
        y = int(start[1] * (1 - progress) + end[1] * progress)
        pygame.draw.circle(screen, color, (x, y), width)


if __name__ == "__main__":
    main()