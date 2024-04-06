<<<<<<< HEAD
"""
飞机大战
"""

import pygame
import sys
from PlaneSprite import *
from settings import *
from os import system


# pygame初始化
pygame.init()

system("echo 建议:")
system("echo     游戏时不要在屏幕内频繁移动鼠标")
# 延时启动, 给玩家阅读建议时间
pygame.time.wait(READING_TIME)

# 创建屏幕
screen = pygame.display.set_mode(SCREEN_SIZE)
# 设置标题
pygame.display.set_caption("飞机大战")
pygame.display.set_icon(pygame.image.load("./images/life.png").convert_alpha())
# 创建背景对象组
# 创建两个背景对象作用:制造出背景滚动的画面
BgsGroup = pygame.sprite.Group(
    Backgroud(
        "/".join((IMAGES_PATH, IMAGES_NAMES["BG"])),
    ),
    Backgroud("/".join((IMAGES_PATH, IMAGES_NAMES["BG"])), True),
)
# 创建飞机对象
hero = Hero(
    ["/".join((IMAGES_PATH, ImageName)) for ImageName in IMAGES_NAMES["HERO"]["IMAGE"]],
    [
        "/".join((IMAGES_PATH, ImageName))
        for ImageName in IMAGES_NAMES["HERO"]["DESTROY"]
    ],
)


# 创建初始敌机&敌机组&血条组
SmallEnemiesGroup = pygame.sprite.Group()
MidEnemiesGroup = pygame.sprite.Group()
BigEnemiesGroup = pygame.sprite.Group()


def create_new_small_enemies() -> None:
    """创建小型敌机&避免重叠"""
    for _ in range(EACH_CREATE_SMALL_ENEMY_NUMBER):
        NewSmallEnemy = SmallEnemy(
            "/".join((IMAGES_PATH, IMAGES_NAMES["SMALL_ENEMY"]["IMAGE"])),
            [
                "/".join((IMAGES_PATH, ImageName))
                for ImageName in IMAGES_NAMES["SMALL_ENEMY"]["DOWN_IMAGE"]
            ],
            SMALL_ENEMY_MOVE_SPEED,
        )
        for _SmallEnemy in SmallEnemiesGroup.sprites():
            while NewSmallEnemy.rect.x == _SmallEnemy.rect.x:
                NewSmallEnemy.rect.x = randint(0, WIDTH - NewSmallEnemy.rect.width)
        SmallEnemiesGroup.add(NewSmallEnemy)


def create_new_mid_enemies() -> None:
    """创建中型敌机&避免重叠"""
    for _ in range(EACH_CREATE_MID_ENEMY_NUMBER):
        NewMidEnemy = MidEnemy(
            [
                "/".join((IMAGES_PATH, ImageName))
                for ImageName in IMAGES_NAMES["MID_ENEMY"]["IMAGE"]
            ],
            [
                "/".join((IMAGES_PATH, ImageName))
                for ImageName in IMAGES_NAMES["MID_ENEMY"]["DOWN_IMAGE"]
            ],
            MID_ENEMY_MOVE_SPEED,
        )
        for _MidEnemy in MidEnemiesGroup.sprites():
            while NewMidEnemy.rect.x == _MidEnemy.rect.x:
                NewMidEnemy.rect.x = randint(0, WIDTH - NewMidEnemy.rect.width)
        MidEnemiesGroup.add(NewMidEnemy)


def create_new_big_enemies() -> None:
    """创建大型敌机&避免重叠"""
    for _ in range(EACH_CREATE_BIG_ENEMY_NUMBER):
        NewBigEnemy = BigEnemy(
            [
                "/".join((IMAGES_PATH, ImageName))
                for ImageName in IMAGES_NAMES["BIG_ENEMY"]["IMAGE"]
            ],
            "/".join((IMAGES_PATH, IMAGES_NAMES["BIG_ENEMY"]["HIT_IMAGE"])),
            [
                "/".join((IMAGES_PATH, ImageName))
                for ImageName in IMAGES_NAMES["BIG_ENEMY"]["DOWN_IMAGE"]
            ],
            BIG_ENEMY_MOVE_SPEED,
        )
        for _BigEnemy in BigEnemiesGroup.sprites():
            while NewBigEnemy.rect.x == _BigEnemy.rect.x:
                NewBigEnemy.rect.x = randint(0, WIDTH - NewBigEnemy.rect.width)
        BigEnemiesGroup.add(NewBigEnemy)


create_new_small_enemies()
create_new_mid_enemies()

# 子弹组
HeroBulletsGroup = pygame.sprite.Group()
EnemiesBulletsGroup = pygame.sprite.Group()

BulletSuppliesGroup = pygame.sprite.Group()
BombSuppliesGroup = pygame.sprite.Group()

EnemiesGroups = [SmallEnemiesGroup, MidEnemiesGroup, BigEnemiesGroup]
AllGroups = [
    *EnemiesGroups,
    HeroBulletsGroup,
    EnemiesBulletsGroup,
    BulletSuppliesGroup,
    BombSuppliesGroup,
]

LifeNumberPicsGroup = pygame.sprite.Group()
for number in range(hero.LifeNumber):
    LifeNumberPicsGroup.add(
        LifeNumberPic(
            "/".join((IMAGES_PATH, IMAGES_NAMES["HERO"]["LIFE_IMAGE"])),
            number,
            (
                (WIDTH, FLY_HEIGHT)
                if number == 0
                else LifeNumberPicsGroup.sprites()[-1].rect.topleft
            ),
        )
    )
BombPicsGroup = pygame.sprite.Group()


# 设置长按键盘时 首次发送信号延迟&连续发送信号间隔 单位:毫秒
pygame.key.set_repeat(KEYBOARD_DELAY, INTERVAL)
# 设置定时发送移动事件,用于背景和敌机的移动 单位:毫秒
pygame.time.set_timer(UPDATE_EVENT, UPDATE_TIME)
# 定时发送创建小型飞机时间 单位:毫秒
pygame.time.set_timer(CREATE_NEW_SMALL_ENEMY_EVENT, CREATE_NEW_SMALL_ENEMY_TIME)
# 定时发送创建中型飞机时间 单位:毫秒
pygame.time.set_timer(CREATE_NEW_MID_ENEMY_EVENT, CREATE_NEW_MID_ENEMY_TIME)
# 定时发送创建大型飞机时间 单位:毫秒
pygame.time.set_timer(CREATE_NEW_BIG_ENEMY_EVENT, CREATE_NEW_BIG_ENEMY_TIME)
# 飞机&敌机定时发射子弹
pygame.time.set_timer(HERO_FIRE_EVENT, HERO_FIRE_TIME)
pygame.time.set_timer(ENEMY_FIRE_EVENT, ENEMY_FIRE_TIME)

pygame.time.set_timer(FALL_SUPPLY_EVENT, FALL_SUPPLY_TIME)


def draw() -> None:
    BgsGroup.draw(screen)
    hero.draw(screen)
    SmallEnemiesGroup.draw(screen)
    MidEnemiesGroup.draw(screen)
    BigEnemiesGroup.draw(screen)
    draw_life_line()
    HeroBulletsGroup.draw(screen)
    EnemiesBulletsGroup.draw(screen)
    BulletSuppliesGroup.draw(screen)
    BombSuppliesGroup.draw(screen)
    LifeNumberPicsGroup.draw(screen)
    BombPicsGroup.draw(screen)


def draw_life_line() -> None:
    """绘制血条"""
    pygame.draw.rect(
        screen,
        (0, 140, 0),
        pygame.Rect(hero.rect.left, hero.rect.top - 5, hero.life, LIFE_LINE_HEIGHT),
        0,
    )
    for enemy in [*MidEnemiesGroup.sprites(), *BigEnemiesGroup.sprites()]:
        pygame.draw.rect(
            screen,
            (140, 0, 0),
            pygame.Rect(
                enemy.rect.left, enemy.rect.top - 5, enemy.life, LIFE_LINE_HEIGHT
            ),
            0,
        )


def update() -> None:
    BgsGroup.update()
    hero.update(draw, draw_life_line)
    SmallEnemiesGroup.update()
    MidEnemiesGroup.update(draw, draw_life_line)
    BigEnemiesGroup.update(draw, draw_life_line)
    HeroBulletsGroup.update()
    EnemiesBulletsGroup.update()
    BulletSuppliesGroup.update()
    BombSuppliesGroup.update()
    LifeNumberPicsGroup.update(hero.LifeNumber)
    BombPicsGroup.update()


def listen_keyboard(event: pygame.event.Event) -> None:
    # 只有当键盘按下时,event才有key属性
    # 不要设置帧率,否则飞机移动会卡,或者把帧率设置得很大
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            hero.move_up()
        if event.key == pygame.K_DOWN:
            hero.move_down()
        if event.key == pygame.K_LEFT:
            hero.move_left()
        if event.key == pygame.K_RIGHT:
            hero.move_right()
        if not hero.BombIsCD and hero.BombNumber > 0 and event.key == pygame.K_SPACE:
            hero.BombIsCD = True
            pygame.time.set_timer(BOMB_CD_EVENT, BOMB_CD_TIME)
            hero.BombNumber -= 1
            for group in AllGroups:
                group.empty()
            BombPicsGroup.remove(BombPicsGroup.sprites()[-1])


def hero_fire() -> None:
    if hero.TwoBullet:
        for pos in ["left", "right"]:
            HeroBulletsGroup.add(
                Bullet(
                    "/".join((IMAGES_PATH, IMAGES_NAMES["BULLET"]["IMAGE"][1])),
                    hero,
                    HERO_FIRE_SPEED,
                    pos,
                )
            )
    else:
        HeroBulletsGroup.add(
            Bullet(
                "/".join((IMAGES_PATH, IMAGES_NAMES["BULLET"]["IMAGE"][0])),
                hero,
                HERO_FIRE_SPEED,
            )
        )


def work_enemy_distance(_Enemy: Enemy) -> bool:
    if hero.rect.left < _Enemy.rect.midbottom[0] < hero.rect.right:
        if hero.rect.top - _Enemy.rect.bottom <= ENEMY_FIRE_DISTANCE:
            return True


def enemies_fire(
    EnemyBulletsGroup: pygame.sprite.Group, enemy: Enemy, speed: int
) -> None:
    EnemyBulletsGroup.add(
        EnemyBullet(
            "/".join((IMAGES_PATH, IMAGES_NAMES["BULLET"]["IMAGE"][0])), enemy, speed
        )
    )


def check_plane_collide() -> None:
    """飞机碰撞检测"""
    Destroyed = False
    ConllideEnemiesListList = [
        pygame.sprite.spritecollide(
            hero, EnemiesGroup, False, pygame.sprite.collide_mask
        )
        for EnemiesGroup in EnemiesGroups
    ]
    for ConllideEnemiesList in ConllideEnemiesListList:
        if ConllideEnemiesList:
            for ConllideEnemy in ConllideEnemiesList:
                ConllideEnemy.down(draw, draw_life_line)
            if not Destroyed:
                Destroyed = True
                hero.protecting = True
                pygame.time.set_timer(OFF_PROTECT_EVENT, OFF_PROTECT_TIME)
                hero.ListenKeyboard = False
                pygame.time.set_timer(LISTEN_KEYBOARD_EVENT, LISTEN_KEYBOARD_TIME)
                hero.LifeNumber -= 1
                hero.destroy(draw, draw_life_line)


def check_bullet_collide() -> None:
    """飞机子弹&敌机碰撞检测"""
    for EnemiesGroup in EnemiesGroups:
        for ConllideEnemiesList in pygame.sprite.groupcollide(
            HeroBulletsGroup, EnemiesGroup, True, False, pygame.sprite.collide_mask
        ).values():
            for ConllideEnemy in ConllideEnemiesList:
                try:
                    ConllideEnemy.life -= FIRED_ENEMY
                except AttributeError:
                    ConllideEnemy.down(draw, draw_life_line)

    for _ in pygame.sprite.spritecollide(
        hero, EnemiesBulletsGroup, True, pygame.sprite.collide_mask
    ):
        if not hero.protecting:
            hero.life -= FIRED_HERO


def check_supply_collide() -> None:
    if pygame.sprite.spritecollide(
        hero, BulletSuppliesGroup, True, pygame.sprite.collide_mask
    ):
        if hero.TwoBullet == False:
            HeroBulletsGroup.empty()
            hero.TwoBullet = True
        pygame.time.set_timer(STOP_HERO_FIRE_TWO_EVENT, STOP_HERO_FIRE_TWO_TIME)
    if pygame.sprite.spritecollide(
        hero, BombSuppliesGroup, True, pygame.sprite.collide_mask
    ):
        if hero.BombNumber < 3:
            hero.BombNumber += 1
            BombPicsGroup.add(
                BombPic(
                    "/".join((IMAGES_PATH, IMAGES_NAMES["BOMB"]["SHOW_IMAGE"])),
                    hero.BombNumber,
                    (
                        (0, FLY_HEIGHT)
                        if hero.BombNumber == 1
                        else BombPicsGroup.sprites()[-1].rect.topright
                    ),
                )
            )


def run() -> None:
    while hero.LifeNumber > 0:
        for event in pygame.event.get():
            # 退出
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            draw()

            if hero.ListenKeyboard:
                listen_keyboard(event)

            if not hero.protecting:
                check_plane_collide()
            check_bullet_collide()

            check_supply_collide()

            update()

            if event.type == HERO_FIRE_EVENT:
                hero_fire()

            if event.type == BOMB_CD_EVENT:
                hero.BombIsCD = False
                pygame.time.set_timer(BOMB_CD_EVENT, 0)

            if event.type == LISTEN_KEYBOARD_EVENT:
                hero.ListenKeyboard = True
                pygame.time.set_timer(LISTEN_KEYBOARD_EVENT, 0)

            if event.type == OFF_PROTECT_EVENT:
                hero.protecting = False
                pygame.time.set_timer(OFF_PROTECT_EVENT, 0)

            if event.type == STOP_HERO_FIRE_TWO_EVENT:
                pygame.time.set_timer(STOP_HERO_FIRE_TWO_EVENT, 0)
                hero.TwoBullet = False
                HeroBulletsGroup.empty()

            if event.type == ENEMY_FIRE_EVENT:
                for EnemyType, EnemiesList in dict(
                    zip(("SMALL", "MID", "BIG"), EnemiesGroups)
                ).items():
                    for enemy in EnemiesList:
                        if work_enemy_distance(enemy):
                            enemies_fire(
                                EnemiesBulletsGroup,
                                enemy,
                                (
                                    SMALL_ENEMY_FIRE_SPEED
                                    if EnemyType == "SMALL"
                                    else (
                                        MID_ENEMY_FIRE_SPEED
                                        if EnemyType == "MID"
                                        else BIG_ENEMY_FIRE_SPEED
                                    )
                                ),
                            )

            if event.type == CREATE_NEW_SMALL_ENEMY_EVENT:
                create_new_small_enemies()
            if event.type == CREATE_NEW_MID_ENEMY_EVENT:
                create_new_mid_enemies()
            if event.type == CREATE_NEW_BIG_ENEMY_EVENT:
                create_new_big_enemies()

            if event.type == FALL_SUPPLY_EVENT:
                BulletSuppliesGroup.add(
                    BulletSupply(
                        "/".join((IMAGES_PATH, IMAGES_NAMES["BULLET"]["SUPPLY_IMAGE"])),
                        SUPPLY_FALL_SPEED,
                    )
                )
                BombSuppliesGroup.add(
                    BombSupply(
                        "/".join((IMAGES_PATH, IMAGES_NAMES["BOMB"]["SUPPLY_IMAGE"])),
                        SUPPLY_FALL_SPEED,
                    )
                )

            # 刷新屏幕
            pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run()
=======
"""
飞机大战
"""

import pygame
import sys
from PlaneSprite import *
from settings import *
from os import system


# pygame初始化
pygame.init()

# 创建屏幕
screen = pygame.display.set_mode(SCREEN_SIZE)
# 设置标题
pygame.display.set_caption("飞机大战")
# 设置图标
pygame.display.set_icon(
    pygame.image.load("/".join((IMAGES_PATH, IMAGES_NAMES["ICON"]))).convert_alpha()
)
# 创建背景对象组
# 创建两个背景对象作用:制造出背景滚动的画面
BgsGroup = pygame.sprite.Group(
    Backgroud(
        "/".join((IMAGES_PATH, IMAGES_NAMES["BG"])),
    ),  # type: ignore
    Backgroud("/".join((IMAGES_PATH, IMAGES_NAMES["BG"])), True),
)
# 创建飞机对象
hero = Hero(
    ["/".join((IMAGES_PATH, ImageName)) for ImageName in IMAGES_NAMES["HERO"]["IMAGE"]],
    [
        "/".join((IMAGES_PATH, ImageName))
        for ImageName in IMAGES_NAMES["HERO"]["DESTROY"]
    ],
)


# 创建初始敌机&敌机组&血条组
SmallEnemiesGroup = pygame.sprite.Group()
MidEnemiesGroup = pygame.sprite.Group()
BigEnemiesGroup = pygame.sprite.Group()


# 定义创建敌机的函数
def create_new_small_enemies() -> None:
    """创建小型敌机&避免重叠"""
    for _ in range(EACH_CREATE_SMALL_ENEMY_NUMBER):
        NewSmallEnemy = SmallEnemy(
            "/".join((IMAGES_PATH, IMAGES_NAMES["SMALL_ENEMY"]["IMAGE"])),
            [
                "/".join((IMAGES_PATH, ImageName))
                for ImageName in IMAGES_NAMES["SMALL_ENEMY"]["DOWN_IMAGE"]
            ],
            SMALL_ENEMY_MOVE_SPEED,
        )
        for _SmallEnemy in SmallEnemiesGroup.sprites():
            while NewSmallEnemy.rect.x == _SmallEnemy.rect.x:
                NewSmallEnemy.rect.x = randint(0, WIDTH - NewSmallEnemy.rect.width)
        SmallEnemiesGroup.add(NewSmallEnemy)


def create_new_mid_enemies() -> None:
    """创建中型敌机&避免重叠"""
    for _ in range(EACH_CREATE_MID_ENEMY_NUMBER):
        NewMidEnemy = MidEnemy(
            [
                "/".join((IMAGES_PATH, ImageName))
                for ImageName in IMAGES_NAMES["MID_ENEMY"]["IMAGE"]
            ],
            [
                "/".join((IMAGES_PATH, ImageName))
                for ImageName in IMAGES_NAMES["MID_ENEMY"]["DOWN_IMAGE"]
            ],
            MID_ENEMY_MOVE_SPEED,
        )
        for _MidEnemy in MidEnemiesGroup.sprites():
            while NewMidEnemy.rect.x == _MidEnemy.rect.x:
                NewMidEnemy.rect.x = randint(0, WIDTH - NewMidEnemy.rect.width)
        MidEnemiesGroup.add(NewMidEnemy)


def create_new_big_enemies() -> None:
    """创建大型敌机&避免重叠"""
    for _ in range(EACH_CREATE_BIG_ENEMY_NUMBER):
        NewBigEnemy = BigEnemy(
            [
                "/".join((IMAGES_PATH, ImageName))
                for ImageName in IMAGES_NAMES["BIG_ENEMY"]["IMAGE"]
            ],
            "/".join((IMAGES_PATH, IMAGES_NAMES["BIG_ENEMY"]["HIT_IMAGE"])),
            [
                "/".join((IMAGES_PATH, ImageName))
                for ImageName in IMAGES_NAMES["BIG_ENEMY"]["DOWN_IMAGE"]
            ],
            BIG_ENEMY_MOVE_SPEED,
        )
        for _BigEnemy in BigEnemiesGroup.sprites():
            while NewBigEnemy.rect.x == _BigEnemy.rect.x:
                NewBigEnemy.rect.x = randint(0, WIDTH - NewBigEnemy.rect.width)
        BigEnemiesGroup.add(NewBigEnemy)


create_new_small_enemies()
create_new_mid_enemies()

# 子弹组
HeroBulletsGroup = pygame.sprite.Group()
EnemiesBulletsGroup = pygame.sprite.Group()
# 掉落物组
BulletSuppliesGroup = pygame.sprite.Group()
BombSuppliesGroup = pygame.sprite.Group()
# 创建所有敌机组&所有游戏元素(除背景)组
# 方便遍历后统一操作
EnemiesGroups = [SmallEnemiesGroup, MidEnemiesGroup, BigEnemiesGroup]
AllGroups = [
    *EnemiesGroups,
    HeroBulletsGroup,
    EnemiesBulletsGroup,
    BulletSuppliesGroup,
    BombSuppliesGroup,
]
# 飞机命数
LifeNumberPicsGroup = pygame.sprite.Group()
for number in range(hero.LifeNumber):
    LifeNumberPicsGroup.add(
        LifeNumberPic(
            "/".join((IMAGES_PATH, IMAGES_NAMES["HERO"]["LIFE_IMAGE"])),
            number,
            (
                (WIDTH, FLY_HEIGHT)
                if number == 0
                else LifeNumberPicsGroup.sprites()[-1].rect.topleft
            ),
        )
    )
# 飞机拥有的炸弹
BombPicsGroup = pygame.sprite.Group()


# 设置长按键盘时 首次发送信号延迟&连续发送信号间隔 单位:毫秒
pygame.key.set_repeat(KEYBOARD_DELAY, INTERVAL)
# 设置定时发送移动事件,用于背景和敌机的移动 单位:毫秒
pygame.time.set_timer(UPDATE_EVENT, UPDATE_TIME)
# 定时发送创建小型飞机时间 单位:毫秒
pygame.time.set_timer(CREATE_NEW_SMALL_ENEMY_EVENT, CREATE_NEW_SMALL_ENEMY_TIME)
# 定时发送创建中型飞机时间 单位:毫秒
pygame.time.set_timer(CREATE_NEW_MID_ENEMY_EVENT, CREATE_NEW_MID_ENEMY_TIME)
# 定时发送创建大型飞机时间 单位:毫秒
pygame.time.set_timer(CREATE_NEW_BIG_ENEMY_EVENT, CREATE_NEW_BIG_ENEMY_TIME)
# 飞机&敌机定时发射子弹
pygame.time.set_timer(HERO_FIRE_EVENT, HERO_FIRE_TIME)
pygame.time.set_timer(ENEMY_FIRE_EVENT, ENEMY_FIRE_TIME)
# 定时掉落物 单位:毫秒
pygame.time.set_timer(FALL_SUPPLY_EVENT, FALL_SUPPLY_TIME)


def draw() -> None:
    """绘制所有游戏元素"""
    BgsGroup.draw(screen)
    hero.draw(screen)
    SmallEnemiesGroup.draw(screen)
    MidEnemiesGroup.draw(screen)
    BigEnemiesGroup.draw(screen)
    draw_life_line()
    HeroBulletsGroup.draw(screen)
    EnemiesBulletsGroup.draw(screen)
    BulletSuppliesGroup.draw(screen)
    BombSuppliesGroup.draw(screen)
    LifeNumberPicsGroup.draw(screen)
    BombPicsGroup.draw(screen)


def draw_life_line() -> None:
    """绘制血条"""
    pygame.draw.rect(
        screen,
        (0, 140, 0),
        pygame.Rect(hero.rect.left, hero.rect.top - 5, hero.life, LIFE_LINE_HEIGHT),
        0,
    )
    for enemy in [*MidEnemiesGroup.sprites(), *BigEnemiesGroup.sprites()]:
        pygame.draw.rect(
            screen,
            (140, 0, 0),
            pygame.Rect(
                enemy.rect.left, enemy.rect.top - 5, enemy.life, LIFE_LINE_HEIGHT
            ),
            0,
        )


def update() -> None:
    """所有游戏元素刷新"""
    BgsGroup.update()
    hero.update(draw, draw_life_line)
    SmallEnemiesGroup.update()
    MidEnemiesGroup.update(draw, draw_life_line)
    BigEnemiesGroup.update(draw, draw_life_line)
    HeroBulletsGroup.update()
    EnemiesBulletsGroup.update()
    BulletSuppliesGroup.update()
    BombSuppliesGroup.update()
    LifeNumberPicsGroup.update(hero.LifeNumber)
    BombPicsGroup.update()


def listen_keyboard(event: pygame.event.Event) -> None:
    """监听键盘"""
    # 注意:
    # 只有当键盘按下时,event才有key属性
    # 不要设置帧率,否则飞机移动会卡,或者把帧率设置得很大
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            hero.move_up()
        if event.key == pygame.K_DOWN:
            hero.move_down()
        if event.key == pygame.K_LEFT:
            hero.move_left()
        if event.key == pygame.K_RIGHT:
            hero.move_right()
        # 飞机发射炸弹
        # 须检测发射CD & 拥有炸弹数量 & 是否按下空格
        if not hero.BombIsCD and hero.BombNumber > 0 and event.key == pygame.K_SPACE:
            # 设置飞机发射炸弹进入CD
            hero.BombIsCD = True
            # 设置CD结束事件
            pygame.time.set_timer(BOMB_CD_EVENT, BOMB_CD_TIME)
            # 拥有炸弹数量减1
            hero.BombNumber -= 1
            # 将除背景&飞机外的元素清除
            for group in AllGroups:
                group.empty()
            # 将显示的炸弹数量减1
            BombPicsGroup.remove(BombPicsGroup.sprites()[-1])


def hero_fire() -> None:
    """飞机发射子弹"""
    # 检测飞机是否同时发射两枚子弹
    if hero.TwoBullet:
        for pos in ["left", "right"]:
            HeroBulletsGroup.add(
                Bullet(
                    "/".join((IMAGES_PATH, IMAGES_NAMES["BULLET"]["IMAGE"][1])),
                    hero,
                    HERO_FIRE_SPEED,
                    pos,
                )
            )
    else:
        HeroBulletsGroup.add(
            Bullet(
                "/".join((IMAGES_PATH, IMAGES_NAMES["BULLET"]["IMAGE"][0])),
                hero,
                HERO_FIRE_SPEED,
            )
        )


def work_planes_distance(_Enemy: Enemy) -> bool:
    """计算飞机&敌机的距离"""
    # 作用: 判断敌机是否发射子弹
    if hero.rect.left < _Enemy.rect.midbottom[0] < hero.rect.right:
        if hero.rect.top - _Enemy.rect.bottom <= ENEMY_FIRE_DISTANCE:
            return True


def enemies_fire(
    EnemyBulletsGroup: pygame.sprite.Group, enemy: Enemy, speed: int
) -> None:
    """敌机发射子弹"""
    EnemyBulletsGroup.add(
        EnemyBullet(
            "/".join((IMAGES_PATH, IMAGES_NAMES["BULLET"]["IMAGE"][0])), enemy, speed
        )
    )


def check_plane_collide() -> None:
    """飞机碰撞检测"""
    # 设置飞机被摧毁的标志变量, 用于保证飞机只被摧毁1次
    Destroyed = False
    # 创建一个由碰撞的敌机的列表组成的列表
    ConllideEnemiesListList = [
        pygame.sprite.spritecollide(
            hero, EnemiesGroup, False, pygame.sprite.collide_mask
        )
        for EnemiesGroup in EnemiesGroups
    ]
    # 取出每个列表
    for ConllideEnemiesList in ConllideEnemiesListList:
        # 如果非空, 则有碰撞
        if ConllideEnemiesList:
            # 摧毁列表里每个敌机
            for ConllideEnemy in ConllideEnemiesList:
                ConllideEnemy.down(draw, draw_life_line)
            # 如果飞机没被摧毁过, 则摧毁
            if not Destroyed:
                # 把飞机被摧毁标志变量设为被摧毁
                Destroyed = True
                # 飞机开启无敌帧
                hero.protecting = True
                # 设置关闭无敌帧事件
                pygame.time.set_timer(OFF_PROTECT_EVENT, OFF_PROTECT_TIME)
                # 停止监听键盘
                hero.ListenKeyboard = False
                # 设置重新监听键盘事件
                pygame.time.set_timer(LISTEN_KEYBOARD_EVENT, LISTEN_KEYBOARD_TIME)
                # 飞机命数减1
                hero.LifeNumber -= 1
                # 摧毁飞机
                hero.destroy(draw, draw_life_line)


def check_bullet_collide() -> None:
    """飞机子弹&敌机碰撞检测"""
    for EnemiesGroup in EnemiesGroups:
        for ConllideEnemiesList in pygame.sprite.groupcollide(
            HeroBulletsGroup, EnemiesGroup, True, False, pygame.sprite.collide_mask
        ).values():
            for ConllideEnemy in ConllideEnemiesList:
                try:
                    ConllideEnemy.life -= FIRED_ENEMY
                except AttributeError:
                    ConllideEnemy.down(draw, draw_life_line)

    for _ in pygame.sprite.spritecollide(
        hero, EnemiesBulletsGroup, True, pygame.sprite.collide_mask
    ):
        if not hero.protecting:
            hero.life -= FIRED_HERO


def check_supply_collide() -> None:
    if pygame.sprite.spritecollide(
        hero, BulletSuppliesGroup, True, pygame.sprite.collide_mask
    ):
        if hero.TwoBullet == False:
            HeroBulletsGroup.empty()
            hero.TwoBullet = True
        pygame.time.set_timer(STOP_HERO_FIRE_TWO_EVENT, STOP_HERO_FIRE_TWO_TIME)
    if pygame.sprite.spritecollide(
        hero, BombSuppliesGroup, True, pygame.sprite.collide_mask
    ):
        if hero.BombNumber < 3:
            hero.BombNumber += 1
            BombPicsGroup.add(
                BombPic(
                    "/".join((IMAGES_PATH, IMAGES_NAMES["BOMB"]["SHOW_IMAGE"])),
                    hero.BombNumber,
                    (
                        (0, FLY_HEIGHT)
                        if hero.BombNumber == 1
                        else BombPicsGroup.sprites()[-1].rect.topright
                    ),
                )
            )


def run() -> None:
    while hero.LifeNumber > 0:
        for event in pygame.event.get(exclude=pygame.MOUSEMOTION):
            # 退出
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            draw()

            if hero.ListenKeyboard:
                listen_keyboard(event)

            if not hero.protecting:
                check_plane_collide()
            check_bullet_collide()

            check_supply_collide()

            update()

            if event.type == HERO_FIRE_EVENT:
                hero_fire()

            if event.type == BOMB_CD_EVENT:
                hero.BombIsCD = False
                pygame.time.set_timer(BOMB_CD_EVENT, 0)

            if event.type == LISTEN_KEYBOARD_EVENT:
                hero.ListenKeyboard = True
                pygame.time.set_timer(LISTEN_KEYBOARD_EVENT, 0)

            if event.type == OFF_PROTECT_EVENT:
                hero.protecting = False
                pygame.time.set_timer(OFF_PROTECT_EVENT, 0)

            if event.type == STOP_HERO_FIRE_TWO_EVENT:
                pygame.time.set_timer(STOP_HERO_FIRE_TWO_EVENT, 0)
                hero.TwoBullet = False
                HeroBulletsGroup.empty()

            if not hero.protecting and event.type == ENEMY_FIRE_EVENT:
                for EnemyType, EnemiesList in dict(
                    zip(("SMALL", "MID", "BIG"), EnemiesGroups)
                ).items():
                    for enemy in EnemiesList:
                        if work_planes_distance(enemy) and not hero.protecting:
                            enemies_fire(
                                EnemiesBulletsGroup,
                                enemy,
                                (
                                    SMALL_ENEMY_FIRE_SPEED
                                    if EnemyType == "SMALL"
                                    else (
                                        MID_ENEMY_FIRE_SPEED
                                        if EnemyType == "MID"
                                        else BIG_ENEMY_FIRE_SPEED
                                    )
                                ),
                            )

            if event.type == CREATE_NEW_SMALL_ENEMY_EVENT:
                create_new_small_enemies()
            if event.type == CREATE_NEW_MID_ENEMY_EVENT:
                create_new_mid_enemies()
            if event.type == CREATE_NEW_BIG_ENEMY_EVENT:
                create_new_big_enemies()

            if event.type == FALL_SUPPLY_EVENT:
                BulletSuppliesGroup.add(
                    BulletSupply(
                        "/".join((IMAGES_PATH, IMAGES_NAMES["BULLET"]["SUPPLY_IMAGE"])),
                        SUPPLY_FALL_SPEED,
                    )
                )
                BombSuppliesGroup.add(
                    BombSupply(
                        "/".join((IMAGES_PATH, IMAGES_NAMES["BOMB"]["SUPPLY_IMAGE"])),
                        SUPPLY_FALL_SPEED,
                    )
                )

            # 刷新屏幕
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("down")

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    try:
        run()
    except BaseException as e:
        print(e)
>>>>>>> b344d4e (第一次尝试)
