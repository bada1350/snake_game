import pygame as pg
import time
import random

WIDTH = 400
HEIGHT = 400
CS = 20                             # 셀 한 칸의 크기
TC = 20                             # Total_Count, TC = 20이면 20(행) * 20(열)
A_x = random.randint(0, CS - 1)     # Apple_X, Y // 사과 좌표
A_y = random.randint(0, CS - 1)
P_x = 10                            # Player_X, Y
P_y = 10
SL = 5                              # 뱀 몸통의 최대 길이(사과를 먹으면 증가함)
SCORE = 0
PLAYER_LIFE = 3
list_snake_pos = []                 # 뱀 몸통의 전체좌표가 저장되는 리스트
x_dir = 0                           # 뱀 이동 방향(x)
y_dir = 0                           # 뱀 이동 방향(y)
count = 0

GAME_INTRO = True
GAME_RUNNING = True
ENDING_SCREEN = False
GAME_START = False

# 게임 보드 그리기
def draw_board():
    GAME_SCREEN.fill((0, 0, 0))
    for r in range(TC):
        for c in range(TC):
            pg.draw.rect(GAME_SCREEN, (125, 125, 125), (c * CS, r * CS, CS, CS), 1)

# 우측 상단에 점수 그리기
def draw_score():
    score_txt = FONT_40.render(str(SCORE), True, (255, 255, 255))
    GAME_SCREEN.blit(score_txt, (340, 10))

# 우측 하단에 남은 플레이어 목숨 그리기
def draw_player_life():
    player_life_txt = FONT_40.render(str(PLAYER_LIFE), True, (255, 0, 0))
    GAME_SCREEN.blit(player_life_txt, (340, 340))

# 뱀(플레이어) 그리기
def draw_snake():
    for idx, s in enumerate(list_snake_pos):
        if idx == 0:
            pg.draw.rect(GAME_SCREEN, (0, 255, 0), (s[0] * CS, s[1] * CS, CS, CS))
            pg.draw.circle(GAME_SCREEN, (0, 0, 0), (s[0] * CS + 5, s[1] * CS + 5), 3)
            pg.draw.circle(GAME_SCREEN, (0, 0, 0), (s[0] * CS + 15, s[1] * CS + 5), 3)
        else:
            pg.draw.rect(GAME_SCREEN, (0, 255, 0), (s[0] * CS, s[1] * CS, CS, CS))

# 사과 그리기
def draw_apple():
    pg.draw.circle(GAME_SCREEN, (255, 0, 0), (A_x * CS + 10, A_y * CS + 10), 10)

# 뱀 이동 및 계산
def move_snake():
    global P_x, P_y, SL, SCORE, PLAYER_LIFE, count, ENDING_SCREEN
    # 뱀 이동
    P_x += x_dir
    P_y += y_dir
    
    # 뱀이 이동하면 뱀의 좌표를 리스트의 첫번째 요소로 저장
    list_snake_pos.insert(0, (P_x, P_y))
    
    # 뱀 몸통의 최대 길이(SL)보다 꼬리가 길어지면 꼬리를 버림
    while (len(list_snake_pos) > SL):
        list_snake_pos.pop()
    
    # 뱀이 화면을 벗어나면 화면의 반대편에서 뱀이 등장
    if P_x < 0:
        P_x = 20
    elif P_x > 19:
        P_x = -1
    else:
        pass

    if P_y < 0:
        P_y = 20
    elif P_y > 19:
        P_y = -1
    else:
        pass

    # 뱀이 사과를 먹으면, 뱀 몸통의 최대 길이와 점수를 1씩 증가 & 사운드 재생 & 랜덤한 위치에 사과 생성
    if (P_x, P_y) == (A_x, A_y):
        SL += 1
        SCORE += 1
        APPLE_SND.play()
        reset_apple()

    # 뱀이 자신의 몸과 부딪히면, 뱀 몸통의 최대 길이를 기본값 5로 리셋하고 플레이어의 목숨을 1 감소 & 사운드 재생
    if GAME_START == True and count >= 10:
        for s in list_snake_pos[1:]:
            if list_snake_pos[0] == s:
                SL = 5
                COLLISION_SND.play()
                PLAYER_LIFE -= 1
                count = 0
            else:
                pass
    else:
        pass
    
    # 플레이어의 목숨이 0이 되면 게임을 종료
    if PLAYER_LIFE == 0:
        ENDING_SCREEN = True
    else:
        pass

    count += 1

# 뱀의 좌표와 사과의 좌표가 같으면(= 뱀이 사과를 먹으면) 랜덤한 위치에 사과를 생성
def reset_apple():
    global A_x, A_y
    if (P_x, P_y) == (A_x, A_y):
        A_x = random.randint(0, CS - 1)
        A_y = random.randint(0, CS - 1)

# 게임 안내 화면 그리기
def draw_intro():
    GAME_SCREEN.fill((0, 0, 0))
    game_name_txt = FONT_40.render("스네이크 게임", True, (255, 255, 255))
    copyright_display_txt = FONT_24.render("made by bada1350", True, (255, 255, 0))
    how_to_play_txt_1 = FONT_24.render("[조작 방법]", True, (255, 255, 255))
    how_to_play_txt_2 = FONT_24.render("이동 - 방향키", True, (255, 255, 255))
    how_to_play_txt_3 = FONT_24.render("게임 종료 - q", True, (255, 255, 255))
    game_start_txt = FONT_24.render("PRESS ANY KEY TO START", True, (255, 255, 255))
    
    GAME_SCREEN.blit(game_name_txt, (50, 70))
    GAME_SCREEN.blit(copyright_display_txt, (50, 120))
    GAME_SCREEN.blit(how_to_play_txt_1, (50, 200))
    GAME_SCREEN.blit(how_to_play_txt_2, (50, 240))
    GAME_SCREEN.blit(how_to_play_txt_3, (50, 270))
    GAME_SCREEN.blit(game_start_txt, (50, 350))

# 게임 엔딩 화면 그리기
def draw_ending():
    GAME_SCREEN.fill((0, 0, 0))
    game_score_txt_1 = FONT_40.render("YOUR SCORE", True, (255, 255, 0))
    game_score_txt_2 = FONT_40.render(str(SCORE), True, (255, 255, 255))
    game_end_txt = FONT_24.render("PRESS <Q> TO QUIT", True, (255, 255, 255))
    
    GAME_SCREEN.blit(game_score_txt_1, (70, 120))
    GAME_SCREEN.blit(game_score_txt_2, (180, 180))
    GAME_SCREEN.blit(game_end_txt, (90, 350))

pg.init()
pg.display.set_caption("스네이크 게임")
GAME_SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
pg.key.set_repeat(1, 5)

FONT_24 = pg.font.Font("game_res/nanum-gothic/NanumGothic.ttf", 24)
FONT_40 = pg.font.Font("game_res/nanum-gothic/NanumGothic.ttf", 40)

APPLE_SND = pg.mixer.Sound("game_res/snake_eat_apple.wav")
COLLISION_SND = pg.mixer.Sound("game_res/snake_collision.wav")

# 메인 게임 루프
while GAME_RUNNING:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            GAME_RUNNING = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                GAME_RUNNING = False
            
            GAME_INTRO = False
            
            # 방향키를 누르면 게임 시작
            if event.key == pg.K_UP or event.key == pg.K_DOWN or event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                GAME_START = True
            
            if GAME_START == True:
                if event.key == pg.K_UP:
                    x_dir = 0
                    y_dir = -1
                elif event.key == pg.K_DOWN:
                    x_dir = 0
                    y_dir = 1
                elif event.key == pg.K_LEFT:
                    x_dir = -1
                    y_dir = 0
                elif event.key == pg.K_RIGHT:
                    x_dir = 1
                    y_dir = 0
                else:
                    pass
            else:
                pass
        else:
            pass
    
    if ENDING_SCREEN == False:
        if GAME_INTRO == True:
            draw_intro()
        else:
            # 배경 그리기
            draw_board()
            draw_score()
            draw_player_life()

            # 오브젝트 그리기
            draw_snake()
            draw_apple()

            # 오브젝트 계산
            move_snake()

    else:
        draw_ending()
    
    # 화면 업데이트 및 업데이트 간격 설정
    pg.display.update()
    time.sleep(0.15)
    
pg.quit()