import pygame as pg
import time
import random

WIDTH = 400
HEIGHT = 400
CS = 20     # 셀 한 칸의 크기
TC = 20     # Total_Count, TC = 20이면 20(행) * 20(열)
A_x = random.randint(0, CS - 1)      # Apple_X, Y // 사과 좌표
A_y = random.randint(0, CS - 1)
P_x = 10     # Player_X, Y
P_y = 10
SL = 5      # 뱀 몸통의 최대 길이(사과를 먹으면 증가함)
SCORE = 0
PLAYER_LIFE = 3
list_snake_pos = []  # 뱀 몸통의 전체좌표가 저장되는 리스트
x_dir = 0
y_dir = 0
count = 0

pg.init()
pg.display.set_caption("스네이크 게임")
GAME_SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
pg.key.set_repeat(1, 5)

FONT_40 = pg.font.Font("nanum-gothic/NanumGothic.ttf", 40)
APPLE_SND = pg.mixer.Sound("game_res/snake_eat_apple.wav")
COLLISION_SND = pg.mixer.Sound("game_res/snake_collision.wav")
GAME_RUNNING = True
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

# 뱀을 움직이는 함수
def move_snake():
    global P_x, P_y, SL, SCORE, PLAYER_LIFE, count, GAME_RUNNING
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
        GAME_RUNNING = False
    else:
        pass

    count += 1

# 뱀의 좌표와 사과의 좌표가 같으면(= 뱀이 사과를 먹으면) 랜덤한 위치에 사과를 생성
def reset_apple():
    global A_x, A_y
    if (P_x, P_y) == (A_x, A_y):
        A_x = random.randint(0, CS - 1)
        A_y = random.randint(0, CS - 1)

# 메인 게임 루프
while GAME_RUNNING:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            GAME_RUNNING = False
        elif event.type == pg.KEYDOWN:
            GAME_START = True
            if event.key == pg.K_q:
                GAME_RUNNING = False
            elif event.key == pg.K_UP:
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
    
    # 배경 그리기
    draw_board()
    draw_score()
    draw_player_life()

    # 오브젝트 그리기
    draw_snake()
    draw_apple()

    # 오브젝트 계산
    move_snake()

    # 화면 업데이트 및 업데이트 간격 설정
    pg.display.update()
    time.sleep(0.15)
pg.quit()