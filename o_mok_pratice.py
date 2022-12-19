from o_mok import *
import cv2
import mediapipe as mp
import numpy as np

#mediapipe 초기 설정
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_drawing.DrawingSpec

#스쿼트 설정
stage = None
squat_cnt = 0

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
omok_play = False

#각도 계
def calculateAngle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

def button(mouse, width, height, height_pos, text, text_x):
    if width / 2 - 70 <= mouse[0] <= width / 2 + 70 and height - height_pos <= mouse[1] <= height - height_pos + 40:
        pygame.draw.rect(SURFACE, color_light, [width / 2 - 70, height - height_pos, 140, 40])

    else:
        pygame.draw.rect(SURFACE, color_dark, [width / 2 - 70, height - height_pos, 140, 40])

    SURFACE.blit(text, (width / 2 - text_x, height - height_pos + 10))


while running:

    if main_menu == True:
        mouse = pygame.mouse.get_pos()

        for e in pygame.event.get():

            if e.type == pygame.QUIT:
                pygame.quit()

            if e.type == pygame.MOUSEBUTTONDOWN:

                if w / 2 - 70 <= mouse[0] <= w / 2 + 70 and h - 310 <= mouse[1] <= h - 310 + 40:
                    pygame.quit()
                elif w / 2 - 70 <= mouse[0] <= w / 2 + 70 and h - 410 <= mouse[1] <= h - 410 + 40:
                    main_menu = False

        draw_board(SURFACE)
        button(mouse, w, h, 310, quit_text, 30)
        button(mouse, w, h, 410, start_text, 40)
        pygame.display.update()
        clock.tick(10)

    else:

        win = 0
        cap = cv2.VideoCapture(0)

        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                ret, frame = cap.read()

                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                results = pose.process(image)

                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # 랜드마크 추출
                try:
                    landmarks = results.pose_landmarks.landmark

                    # 힙, 무릎, 발목 좌표값
                    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                    # 앵글 계산
                    angle = calculateAngle(hip, knee, ankle)

                    cv2.putText(image, str(angle),
                                tuple(np.multiply(knee, [640, 480]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )

                    # 카운트 로직
                    if angle > 170:
                        stage = "SQUAT_UP"
                    elif 130 < angle <= 170 and stage == 'SQUAT_UP':
                        stage = "DOWNING"
                    elif 90 < angle <= 130 and stage == "DOWNING":
                        stage = "SQUAT_DOWN"
                        if squat_cnt == 10:
                            squat_cnt = 0
                            stage = None
                        else:
                            squat_cnt = squat_cnt + 1
                            stage = None


                except:
                    pass

                # 카운터 출력
                cv2.rectangle(image, (0, 0), (360, 70), (0, 0, 0), -1)
                cv2.putText(image, "STATE : ", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, "COUNT : ", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, str(squat_cnt),
                            (150, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                cv2.putText(image, stage,
                            (140, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                # 포즈 감지
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                          )

                img_resize = cv2.resize(image, dsize=(500, 500), interpolation=cv2.INTER_AREA)

                cv2.imshow('Squat Counter', img_resize)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

                if squat_cnt >= 1:
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
                                        squat_cnt = 0
                                        if checkOmok(i_new, j_new, black_turn):
                                            win = board[i_new][j_new]
                                            print(win)
                                        black_turn = not black_turn
                SURFACE.fill(YELLOW)
                draw_board(SURFACE)
                draw_dols_order(SURFACE, 0, len(dols_order))
                pygame.display.update()
                clock.tick(10)

                if win:
                    win_text = "Black Team " if win == BLACK_DOL else "White Team "
                    win_text += " WIN!"
                    text_surface = myfont.render(win_text, False, (0, 0, 255))
                    SURFACE.blit(text_surface, (w // 2 - 200, h // 2 - font_size))
                    pygame.display.update()
                    for i in range(6):
                        clock.tick(1)
                    main_menu = True
                    for i in range(board_height):
                        for j in range(board_width):
                            board[i][j] = 0

                    dols_order.clear()
                    black_turn = True
                    cap.release()
                    cv2.destroyAllWindows()














