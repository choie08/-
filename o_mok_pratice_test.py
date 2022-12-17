from o_mok import *

#game 초기화
pygame.init()

#window와 바둑판 size
SURFACE = pygame.display.set_mode((w,h))

#color 설정
color = (255, 255, 255)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)
#font 설정
smallfont = pygame.font.SysFont('Corbel', 35)
quit_text = smallfont.render('QUIT', True, color)
start_text = smallfont.render('START', True, color)

clock = pygame.time.Clock()
black_turn = True
running = True
is_down = False
is_valid = False
new_pos = (0,0)

main_menu = True
game_start = False

def button(mouse, width, height, height_pos, text, text_x):
	if width / 2 - 70 <= mouse[0] <= width / 2 + 70 and height - height_pos <= mouse[1] <= height - height_pos + 40:
		pygame.draw.rect(SURFACE, color_light, [width / 2 - 70, height - height_pos, 140, 40])

	else:
		pygame.draw.rect(SURFACE, color_dark, [width / 2 - 70, height - height_pos, 140, 40])

	SURFACE.blit(text, (width / 2 - text_x, height - height_pos + 10))


while running:

	if main_menu == True:
		mouse = pygame.mouse.get_pos()
		button(mouse, w, h, 310, quit_text, 30)
		button(mouse, w, h, 410, start_text, 40)

		for e in pygame.event.get():

			if e.type == pygame.QUIT:
				pygame.quit()

			if e.type == pygame.MOUSEBUTTONDOWN:

				if w / 2 - 70 <= mouse[0] <= w / 2 + 70 and h - 310 <= mouse[1] <= h - 310 + 40:
					pygame.quit()
				elif w / 2 - 70 <= mouse[0] <= w / 2 + 70 and h - 410 <= mouse[1] <= h - 410 + 40:
					pygame.quit()

		SURFACE.fill(YELLOW)
		draw_board(SURFACE)
		draw_dols_order(SURFACE, 0, len(dols_order))
		pygame.display.update()
		clock.tick(30)

	else:
		for e in pygame.event.get():
			if e.type == QUIT:
				running = False
			elif e.type == MOUSEBUTTONDOWN:
				is_down = True
			elif e.type == MOUSEBUTTONUP:
				if is_down:
					is_valid, i_new, j_new = checkValid(pygame.mouse.get_pos())
					if is_valid:
						is_down = False
						if board[i_new][j_new] == NO_DOL:
							board[i_new][j_new] = BLACK_DOL if black_turn else WHITE_DOL
							dols_order.append((i_new, j_new, board[i_new][j_new]))
							printBoard()
							if checkOmok(i_new, j_new, black_turn):
								running = False
								win = board[i_new][j_new]
							black_turn = not black_turn
		SURFACE.fill(YELLOW)
		draw_board(SURFACE)
		draw_dols_order(SURFACE, 0, len(dols_order))
		pygame.display.update()
		clock.tick(30)


if win:
	win_text = "Black Team " if win == BLACK_DOL else "White Team "
	win_text += " WIN!"
	text_surface = myfont.render(win_text, False, (0, 0, 255))
	SURFACE.blit(text_surface, (w//2 - 200, h//2-font_size))
	pygame.display.update()
	for i in range(6):
		clock.tick(1)



pygame.quit()

