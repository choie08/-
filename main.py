import pygame

def button(mouse, width, height, height_pos, text, text_x):
    if width / 2 - 70 <= mouse[0] <= width / 2 + 70 and height - height_pos <= mouse[1] <= height - height_pos + 40:
        pygame.draw.rect(screen, color_light, [width / 2 - 70, height - height_pos, 140, 40])

    else:
        pygame.draw.rect(screen, color_dark, [width / 2 - 70, height - height_pos, 140, 40])

    screen.blit(text, (width / 2 - text_x, height - height_pos + 10))

pygame.init()

screen_size = (960, 720)
screen = pygame.display.set_mode(screen_size)
width = screen.get_width()
height = screen.get_height()

pygame.display.set_caption("OMOK")

color = (255, 255, 255)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)
smallfont = pygame.font.SysFont('Corbel', 35)
quit_text = smallfont.render('QUIT', True, color)
start_text = smallfont.render('START', True, color)
mediapipe_text = smallfont.render('MEDIAPIPE', True, color)

while True:

    screen.fill((60, 25, 60))
    mouse = pygame.mouse.get_pos()
    button(mouse, width, height, 310, quit_text, 30)
    button(mouse, width, height, 360, mediapipe_text, 68)
    button(mouse, width, height, 410, start_text, 40)

    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            pygame.quit()

        if ev.type == pygame.MOUSEBUTTONDOWN:

            if width / 2 -70 <= mouse[0] <= width / 2 + 70 and height - 310 <= mouse[1] <= height - 310 + 40:
                pygame.quit()

    pygame.display.update()
