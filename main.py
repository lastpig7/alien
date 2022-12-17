import pygame
import sys
import math
import traceback
import myplane
import enemy
import bullet
import supply
from pygame.locals import *
from random import *
import os
pygame.init()
pygame.mixer.init()  # 混音器初始化

bg_size = width, height = 450, 600
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('alien')

background = pygame.image.load('./images/background.png').convert()

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
# 初始化音效，和设定声音大小
pygame.mixer.music.load("sound/NieR_End.mp3")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)


# 增加小型敌人的函数
def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.Enemy_1(bg_size)
        group1.add(e1)
        group2.add(e1)


# 增加中型敌人的函数
def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.Enemy_2(bg_size)
        group1.add(e2)
        group2.add(e2)


# 增加大型敌人的函数
def add_big_enemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.Enemy_3(bg_size)
        group1.add(e3)
        group2.add(e3)


# 增加移动速度
def inc_speed(target, inc):
    for each in target:
        each.speed += inc


#

def main():
    pygame.mixer.music.play(-1)  # 无限循环背景音乐

    # 生成我方的飞机
    me = myplane.MyPlane(bg_size)

    enemies = pygame.sprite.Group()

    # 初始化敌方小型飞机
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 14)

    # 初始化敌方中型飞机
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 5)

    # 初始化敌方大型飞机
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 12)

    # 敌人小中大型飞机和我方飞机被损坏的索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    # 统计得分score
    score = 0
    # 设置本游戏的界面字体
    score_font = pygame.font.Font("font/font.ttf", 36)

    paused = False  # 表示是否停止该游戏

    pause_nor_image = pygame.image.load("images/pause_nor.png").convert_alpha()
    pause_pressed_image = pygame.image.load("images/pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("images/resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("images/resume_pressed.png").convert_alpha()
    # 初始化停止按钮上的图片
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
    # 设置停止按钮的位置
    paused_image = pause_nor_image

    # 初始化难度级别与得分-难度间隔
    level = 1

    bomb_image = pygame.image.load("images/bomb.png").convert_alpha()  # 设置全屏炸弹的图片
    # 设置显示炸弹数量的位置与字体
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("font/font.ttf", 48)
    bomb_num = 3

    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    # 初始化两个补给包（炸弹补给包和升级补给包的大小）
    SUPPLY_TIME = USEREVENT
    pygame.time.set_timer(SUPPLY_TIME, 10 * 1000)
    # 设置成每十秒发送补给包

    # 子弹补给包定时器
    Upgarde_Packet_time = USEREVENT + 1

    # 表示当前子弹的状态
    status = 0

    # 解除我方无敌状态定时器
    INVINCIBLE_TIME = USEREVENT + 2

    # 表示当前我方飞机生命的数量
    life_image = pygame.image.load("images/life.png").convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3

    # 用于阻止重复打开记录文件
    recorded = False
    # 初始化两个子弹图片
    image1 = "images/bullet1.png"
    image2 = "images/bullet2.png"
    # 生成普通子弹
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 20  # 子弹数量
    normal_bullet_speed = 12  # 一级子弹速度
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Ordinary_Bullet(me.rect.midtop, image=image1, speed=normal_bullet_speed))  #
        # 设置成普通子弹，并设置成速度

    # 生成双倍子弹
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 8
    double_bullet_speed = 20
    for i in range(BULLET2_NUM // 2):
        bullet2.append(bullet.Ordinary_Bullet((me.rect.centerx - 33, me.rect.centery),
                                              image=image1, speed=double_bullet_speed))
        bullet2.append(bullet.Ordinary_Bullet((me.rect.centerx + 33, me.rect.centery),
                                              image=image1, speed=double_bullet_speed))
    # 设置成双倍子弹，并设置速度

    # 生成弹跳子弹
    bullet3 = []
    bullet3_index = 0
    BULLET3_NUM = 12
    treble_bullet_speed = 20
    for i in range(BULLET3_NUM // 3):
        bullet3.append(
            bullet.Bounce_Bullet((me.rect.centerx - 33, me.rect.centery), image=image2, angle=2 * math.pi / 3,
                                 speed=treble_bullet_speed))
        bullet3.append(bullet.Bounce_Bullet((me.rect.centerx, me.rect.centery), image=image2,
                                            speed=treble_bullet_speed, angle=math.pi / 2))
        bullet3.append(
            bullet.Bounce_Bullet((me.rect.centerx + 30, me.rect.centery), image=image2,
                                 speed=treble_bullet_speed, angle=math.pi / 3))
    # 生成弹跳子弹 设置角度，位置，速度

    running = True

    clock = pygame.time.Clock()

    #  表示我方飞机切换图片，形成飞机的尾气效果
    switch_image = True

    # 初始化延迟为100
    delay = 100

    frame_rate = 30
    # 表示游戏运行的帧率

    # 初始化游戏结束界面
    gameover_font = pygame.font.Font('font/font.ttf', 48)  # 设置字体
    again_image = pygame.image.load('images/again.png').convert_alpha()  # 初始化重新开始图片
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load('images/gameover.png').convert_alpha()  # 初始化游戏结束图片
    gameover_rect = gameover_image.get_rect()
    slow_time = 0  # 将减速时间时间设置为0
    while running:
        if slow_time > 0:
            slow_time -= 1
            # 如果当前时间为减速状态，则将其减1
        else:
            slow_time = 0
            frame_rate = 30
            # 重新设置游戏帧率，和减速时间

        # 对于游戏中事件的处理
        for event in pygame.event.get():
            if event.type == QUIT:
                # 如果用户退出，则进程关闭，退出
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                # 表示是否暂停，如果用户暂停，则停止，如果用户继续，则继续游戏p
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    # 检测鼠标左键并且是否在矩形内
                    paused = not paused
                    #
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIME, 10 * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            elif event.type == MOUSEMOTION:  # 有鼠标消息
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False
            elif event.type == SUPPLY_TIME:
                supply_sound.play()
                if choice([True, False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()

            elif event.type == Upgarde_Packet_time:
                status = 0
                pygame.time.set_timer(Upgarde_Packet_time, 0)

            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)

        # 根据用户的得分从而改变难度
        if level == 1 and score > 1000:
            level = 2
            upgrade_sound.play()
            # 增加3架小型敌机、2架中型敌机
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            # 提升小型敌机速度
            inc_speed(small_enemies, 1)
        elif level == 2 and score > 3000:
            pygame.time.set_timer(SUPPLY_TIME, (10 - level) * 1000)
            level = 3
            upgrade_sound.play()
            # 增加5架小型敌机、3架中型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            # 提升敌机速度
            inc_speed(small_enemies, 2)
            inc_speed(mid_enemies, 1)
        elif level == 3 and score > 7000:
            level = 4
            pygame.time.set_timer(SUPPLY_TIME, (10 - level) * 1000)
            upgrade_sound.play()
            # 增加7架小型敌机、4架中型敌机和一架大型机
            add_small_enemies(small_enemies, enemies, 7)
            add_mid_enemies(mid_enemies, enemies, 4)
            add_big_enemies(big_enemies, enemies, 1)
            # 提升小型敌机速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level == 4 and score > 12000:
            level = 5
            pygame.time.set_timer(SUPPLY_TIME, (10 - 4) * 1000)
            upgrade_sound.play()
            # 增加9架小型敌机、4架中型敌机和1架大型机
            add_small_enemies(small_enemies, enemies, 9)
            add_mid_enemies(mid_enemies, enemies, 4)
            add_big_enemies(big_enemies, enemies, 1)
            # 提升小型敌机速度
            inc_speed(small_enemies, 1)
        elif level == 5 and score > 17000:
            level = 6
            pygame.time.set_timer(SUPPLY_TIME, (10 - 4) * 1000)
            upgrade_sound.play()
            # 增加9架小型敌机、4架中型敌机和2架大型机
            add_small_enemies(small_enemies, enemies, 9)
            add_mid_enemies(mid_enemies, enemies, 4)
            add_big_enemies(big_enemies, enemies, 2)
            inc_speed(small_enemies, 2)
        elif level == 6 and score > 25000:
            if status == 0:
                status = 1

        screen.blit(background, (0, 0))
        if not paused and life_num:
            # 检测用户的键盘操作
            key_pressed = pygame.key.get_pressed()
            if key_pressed[K_c] and level >= 2 and slow_time == 0:
                slow_time = 20
                frame_rate = 10
            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()
            # 飞机移动

            # 绘制炸弹补给并检测是否获得
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, me):
                    get_bomb_sound.play()
                    if bomb_num < 5:
                        bomb_num = min(5, bomb_num + 1)  # 炸弹存储数量最大为5
                    else:
                        life_num = min(5, life_num + 1)
                    bomb_supply.active = False

            # 绘制子弹补给并检测是否获得
            bullet_supply_duration = 10
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, me):
                    get_bullet_sound.play()
                    # 发射超级子弹
                    if status == 0:
                        status = 1
                    else:
                        status = 2
                    # 持续bullet_supply_duration秒
                    pygame.time.set_timer(Upgarde_Packet_time, bullet_supply_duration * 1000)
                    bullet_supply.active = False

            # 发射子弹      难度不同，子弹射速不同
            if level < 3:
                bullet_shoot_interval = 10
            else:
                bullet_shoot_interval = max(7, 10 - level)
            if not (delay % bullet_shoot_interval):  # 每bullet_shoot_interval帧就放一次子弹
                bullet_sound.play()
                if status == 2:
                    bullets = bullet3
                    bullets[bullet3_index].reset((me.rect.centerx - 33, me.rect.centery))
                    bullets[bullet3_index + 1].reset((me.rect.centerx, me.rect.centery))
                    bullets[bullet3_index + 2].reset((me.rect.centerx + 30, me.rect.centery))
                    bullet3_index = (bullet3_index + 3) % BULLET3_NUM

                elif status == 0:
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM

                elif status == 1:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx - 33, me.rect.centery))
                    bullets[bullet2_index + 1].reset((me.rect.centerx + 30, me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM

            # 检测子弹是否击中
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.hit = True
                                e.energy -= 1
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False

            # 绘制大型敌机
            for each in big_enemies:
                if each.active:
                    if each.move():
                        life_num -= 1
                    if each.hit:
                        # 绘制被打到的特效
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen, BLACK,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5),
                                     2)
                    # 当生命大于20%显示绿色，否则显示红色
                    energy_remain = each.energy / enemy.Enemy_3.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain,
                                      each.rect.top - 5), 2)

                    # 即将出现，播放音效
                    if each.rect.bottom == -50:
                        enemy3_fly_sound.play(1)
                else:
                    # 毁灭
                    if not (delay % 3):
                        if e3_destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6
                        if e3_destroy_index == 0:
                            enemy3_fly_sound.stop()
                            score += 2500
                            each.reset()
                # 绘制全屏炸弹数量
                bomb_text = bomb_font.render("x %d" % bomb_num, True, WHITE)
                screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
                screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - bomb_rect.height))

            # 绘制中型敌机
            for each in mid_enemies:
                if each.active:
                    if each.move():
                        life_num -= 1
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen, BLACK,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5),
                                     2)
                    # 当生命大于20%显示绿色，否则显示红色
                    energy_remain = each.energy / enemy.Enemy_2.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain,
                                      each.rect.top - 5), 2)
                else:
                    # 毁灭
                    if not (delay % 3):
                        if e2_destroy_index == 0:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 600
                            each.reset()

            # 绘制小型敌机
            for each in small_enemies:
                if each.active:
                    if each.move():
                        life_num -= 1
                    screen.blit(each.image, each.rect)
                else:
                    # 毁灭
                    if not (delay % 3):
                        if e1_destroy_index == 0:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += 200
                            each.reset()

            # 检测我方飞机是否被撞
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.active = False  # 去掉则无敌
                for e in enemies_down:
                    e.active = False

            # 绘制飞机
            if me.active:
                if switch_image:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                # 毁灭
                if not (delay % 3):
                    if me_destroy_index == 0:
                        me_down_sound.play()
                    screen.blit(me.destroy_images[me_destroy_index], me.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        life_num -= 1
                        me.reset()
                        pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)  # 三秒无敌状态

        # 绘制剩余生命数量
        if life_num:
            for i in range(life_num):
                screen.blit(life_image,
                            (width - 10 - (i + 1) * life_rect.width,
                             height - 10 - life_rect.height))
        # 绘制游戏结束画面
        elif life_num == 0:
            # 背景音乐停止
            pygame.mixer.music.stop()

            # 音效停止
            pygame.mixer.stop()

            # 停止发放补给
            pygame.time.set_timer(SUPPLY_TIME, 0)

            if not recorded:
                recorded = True
                # 读取历史最高得分
                with open("record.txt", "r") as f:
                    record_score = int(f.read())

                # 如果玩家得分高于历史得分存档
                if score > record_score:
                    with open("record.txt", 'w') as f:
                        f.write(str(score))
            # 绘制结束界面
            record_score_text = score_font.render("Best : %d" % record_score, True, (255, 255, 255))
            screen.blit(record_score_text, (50, 80))

            gameover_text1 = gameover_font.render("Your Score", True, (255, 255, 255))
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                (width - gameover_text1_rect.width) // 2, height // 3
            screen.blit(gameover_text1, gameover_text1_rect)

            gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                (width - gameover_text2_rect.width) // 2, \
                gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = \
                (width - again_rect.width) // 2, \
                gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = \
                (width - again_rect.width) // 2, \
                again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)
            # 检测用户的鼠标操作
            # 如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                # 获取鼠标坐标
                pos = pygame.mouse.get_pos()
                # 如果用户点击“重新开始”
                if again_rect.left < pos[0] < again_rect.right and \
                        again_rect.top < pos[1] < again_rect.bottom:
                    # 调用main函数，重新开始游戏
                    main()
                    # 如果用户点击“结束游戏”
                elif gameover_rect.left < pos[0] < gameover_rect.right and \
                        gameover_rect.top < pos[1] < gameover_rect.bottom:
                    # 退出游戏
                    pygame.quit()
                    sys.exit()

        # 绘制得分
        score_text = score_font.render("Score : %s " % str(score), True, WHITE)
        # score_text2 = score_font2.render("adapted by biliDXS", True, WHITE)
        screen.blit(score_text, (10, 5))
        # screen.blit(score_text2, (10, 50))

        # 绘制暂停按钮
        screen.blit(paused_image, paused_rect)

        # 切换图片
        if not (delay % 5):
            switch_image = not switch_image

        delay -= 1
        if not delay:
            delay = 100

        pygame.display.flip()
        clock.tick(frame_rate)


if __name__ == "__main__":
    # print("the game began running")
    try:
        main()
        os.system("pause")
    except SystemExit:
        pass
    except:
        traceback.print_ec()
        pygame.quit()
        input()  # 接收用户输入 防止出现错误闪屏

