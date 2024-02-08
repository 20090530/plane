'''
飞机大战
素材: https://www.cnblogs.com/144823836yj/p/10162920.html
直接下载地址: https://files.cnblogs.com/files/144823836yj/plane.zip
'''
import pygame
import sys
from PlaneSprite import *
from settings import *
from os import system

system('echo 建议:')
system('echo     游戏时不要在屏幕内频繁移动鼠标')

# pygame初始化
pygame.init()

pygame.time.wait(1000)

# 创建屏幕
screen = pygame.display.set_mode(SCREEN_SIZE)
# 设置标题
pygame.display.set_caption('飞机大战')
pygame.display.set_icon(
    pygame.image.load('.\\images\\life.png').convert_alpha()
)
# 创建背景对象组
# 创建两个背景对象作用:制造出背景滚动的画面
BgsGroup = pygame.sprite.Group(
    Backgroud(
        '\\'.join(
            (IMAGES_PATH, IMAGES_NAMES['BG'])
        ),
    ),

    Backgroud(
        '\\'.join(
            (IMAGES_PATH, IMAGES_NAMES['BG'])
        ),
        True
    )
)
# 创建飞机对象
hero = Hero(
    [
        '\\'.join((IMAGES_PATH, ImageName))
        for ImageName in IMAGES_NAMES['HERO']['IMAGE']
    ],
    [
        '\\'.join((IMAGES_PATH, ImageName))
        for ImageName in IMAGES_NAMES['HERO']['DESTROY']
    ],
)


# 创建初始敌机&敌机组&血条组
SmallEnemiesGroup = pygame.sprite.Group()
MidEnemiesGroup = pygame.sprite.Group()
BigEnemiesGroup = pygame.sprite.Group()


def create_new_small_enemies() -> None:
    '''创建小型敌机&避免重叠'''
    for _ in range(EACH_CREATE_SMALL_ENEMY_NUMBER):
        NewSmallEnemy = SmallEnemy(
            '\\'.join((IMAGES_PATH, IMAGES_NAMES['SMALL_ENEMY']['IMAGE'])),
            [
                '\\'.join((IMAGES_PATH, ImageName))
                for ImageName in IMAGES_NAMES['SMALL_ENEMY']['DOWN_IMAGE']
            ],
            SMALL_ENEMY_MOVE_SPEED
        )
        for _SmallEnemy in SmallEnemiesGroup.sprites():
            while NewSmallEnemy.rect.x == _SmallEnemy.rect.x:
                NewSmallEnemy.rect.x = randint(
                    0, WIDTH - NewSmallEnemy.rect.width)
        SmallEnemiesGroup.add(NewSmallEnemy)


def create_new_mid_enemies() -> None:
    '''创建中型敌机&避免重叠'''
    for _ in range(EACH_CREATE_MID_ENEMY_NUMBER):
        NewMidEnemy = MidEnemy(
            [
                '\\'.join((IMAGES_PATH, ImageName))
                for ImageName in IMAGES_NAMES['MID_ENEMY']['IMAGE']
            ],
            [
                '\\'.join((IMAGES_PATH, ImageName))
                for ImageName in IMAGES_NAMES['MID_ENEMY']['DOWN_IMAGE']
            ],
            MID_ENEMY_MOVE_SPEED
        )
        for _MidEnemy in MidEnemiesGroup.sprites():
            while NewMidEnemy.rect.x == _MidEnemy.rect.x:
                NewMidEnemy.rect.x = randint(0, WIDTH - NewMidEnemy.rect.width)
        MidEnemiesGroup.add(NewMidEnemy)


def create_new_big_enemies() -> None:
    '''创建大型敌机&避免重叠'''
    for _ in range(EACH_CREATE_BIG_ENEMY_NUMBER):
        NewBigEnemy = BigEnemy(
            [
                '\\'.join((IMAGES_PATH, ImageName))
                for ImageName in IMAGES_NAMES['BIG_ENEMY']['IMAGE']
            ],
            '\\'.join((IMAGES_PATH, IMAGES_NAMES['BIG_ENEMY']['HIT_IMAGE'])),
            [
                '\\'.join((IMAGES_PATH, ImageName))
                for ImageName in IMAGES_NAMES['BIG_ENEMY']['DOWN_IMAGE']
            ],
            BIG_ENEMY_MOVE_SPEED
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
    BombSuppliesGroup
]


# 设置长按键盘时 首次发送信号延迟&连续发送信号间隔 单位:毫秒
pygame.key.set_repeat(KEYBOARD_DELAY, INTERVAL)

# 设置定时发送移动事件,用于背景和敌机的移动 单位:毫秒
pygame.time.set_timer(UPDATE_EVENT, UPDATE_TIME)

# 定时发送创建小型飞机时间 单位:毫秒
pygame.time.set_timer(
    CREATE_NEW_SMALL_ENEMY_EVENT,
    CREATE_NEW_SMALL_ENEMY_TIME
)
# 定时发送创建中型飞机时间 单位:毫秒
pygame.time.set_timer(
    CREATE_NEW_MID_ENEMY_EVENT,
    CREATE_NEW_MID_ENEMY_TIME
)
# 定时发送创建大型飞机时间 单位:毫秒
pygame.time.set_timer(
    CREATE_NEW_BIG_ENEMY_EVENT,
    CREATE_NEW_BIG_ENEMY_TIME
)
# 飞机&敌机定时发射子弹
pygame.time.set_timer(HERO_FIRE_EVENT, HERO_FIRE_TIME)
pygame.time.set_timer(ENEMY_FIRE_EVENT, ENEMY_FIRE_TIME)

pygame.time.set_timer(FALL_SUPPLY_EVENT, FALL_SUPPLY_TIME)


def draw(screen: pygame.Surface) -> None:
    BgsGroup.draw(screen)
    hero.draw(screen)
    SmallEnemiesGroup.draw(screen)
    MidEnemiesGroup.draw(screen)
    BigEnemiesGroup.draw(screen)
    HeroBulletsGroup.draw(screen)
    EnemiesBulletsGroup.draw(screen)
    BulletSuppliesGroup.draw(screen)
    BombSuppliesGroup.draw(screen)


def draw_life_line(screen: pygame.Surface) -> None:
    '''绘制血条'''
    pygame.draw.rect(
        screen,
        (0, 140, 0),
        pygame.Rect(
            hero.rect.left,
            hero.rect.top - 5,
            hero.life,
            LIFE_LINE_HEIGHT
        ),
        0
    )
    for enemy in [*MidEnemiesGroup.sprites(), *BigEnemiesGroup.sprites()]:
        pygame.draw.rect(
            screen,
            (140, 0, 0),
            pygame.Rect(
                enemy.rect.left,
                enemy.rect.top - 5,
                enemy.life,
                LIFE_LINE_HEIGHT
            ),
            0
        )


def update() -> None:
    BgsGroup.update()
    hero.update(draw, draw_life_line, screen)
    SmallEnemiesGroup.update()
    MidEnemiesGroup.update(draw, draw_life_line, screen)
    BigEnemiesGroup.update(draw, draw_life_line, screen)
    HeroBulletsGroup.update()
    EnemiesBulletsGroup.update()
    BulletSuppliesGroup.update()
    BombSuppliesGroup.update()


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
    if hero.BombIsCD == False and hero.BombNumber > 0 and event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            pygame.time.set_timer(BOMB_CD_EVENT, BOMB_CD_TIME)
            hero.BombNumber -= 1
            for group in AllGroups:
                group.empty()


def hero_fire() -> None:
    if hero.TwoBullet:
        for pos in ['left', 'right']:
            HeroBulletsGroup.add(
                Bullet(
                    '\\'.join(
                        (IMAGES_PATH, IMAGES_NAMES['BULLET']['IMAGE'][1])
                    ),
                    hero,
                    HERO_FIRE_SPEED,
                    pos
                )
            )
    else:
        HeroBulletsGroup.add(
            Bullet(
                '\\'.join((IMAGES_PATH, IMAGES_NAMES['BULLET']['IMAGE'][0])),
                hero,
                HERO_FIRE_SPEED
            )
        )


def work_enemy_distance(_Enemy: Enemy) -> (bool | None):
    if hero.rect.left < _Enemy.rect.midbottom[0] < hero.rect.right:
        if hero.rect.top - _Enemy.rect.bottom <= ENEMY_FIRE_DISTANCE:
            return True


def enemies_fire(EnemyBulletsGroup: pygame.sprite.Group, enemy: Enemy, speed: int) -> None:
    EnemyBulletsGroup.add(
        EnemyBullet(
            '\\'.join((IMAGES_PATH, IMAGES_NAMES['BULLET']['IMAGE'][0])),
            enemy,
            speed
        )
    )


def check_plane_collide() -> None:
    '''飞机碰撞检测'''
    Destroyed = False
    ConllideEnemiesListList = [
        pygame.sprite.spritecollide(
            hero,
            EnemiesGroup,
            False,
            pygame.sprite.collide_mask
        )

        for EnemiesGroup in EnemiesGroups
    ]
    for ConllideEnemiesList in ConllideEnemiesListList:
        if ConllideEnemiesList:
            for ConllideEnemy in ConllideEnemiesList:
                ConllideEnemy.down(draw, draw_life_line, screen)
            if not Destroyed:
                Destroyed = True
                hero.protecting = True
                pygame.time.set_timer(OFF_PROTECT_EVENT, OFF_PROTECT_TIME)
                hero.ListenKeyboard = False
                pygame.time.set_timer(
                    LISTEN_KEYBOARD_EVENT, LISTEN_KEYBOARD_TIME)
                hero.LifeNumber -= 1
                hero.destroy(draw, draw_life_line, screen)


def check_bullet_collide() -> None:
    '''飞机子弹&敌机碰撞检测'''
    for EnemiesGroup in [SmallEnemiesGroup, MidEnemiesGroup, BigEnemiesGroup]:
        for ConllideEnemiesList in pygame.sprite.groupcollide(
            HeroBulletsGroup,
            EnemiesGroup,
            True,
            False,
            pygame.sprite.collide_mask
        ).values():
            for ConllideEnemy in ConllideEnemiesList:
                try:
                    ConllideEnemy.life -= FIRE_ENEMY
                except AttributeError:
                    ConllideEnemy.down(draw, draw_life_line, screen)
    for EnemyBulletGroup in EnemiesGroups:
        for _ in pygame.sprite.spritecollide(
            hero,
            EnemyBulletGroup,
            True,
            pygame.sprite.collide_mask
        ):
            if not hero.protecting:
                hero.life -= FIRE_HERO


def check_supply_collide() -> None:
    if pygame.sprite.spritecollide(
        hero,
        BulletSuppliesGroup,
        True,
        pygame.sprite.collide_mask
    ):
        if hero.TwoBullet == False:
            HeroBulletsGroup.empty()
            hero.TwoBullet = True
        pygame.time.set_timer(
            STOP_HERO_FIRE_TWO_EVENT,
            STOP_HERO_FIRE_TWO_TIME
        )
    if pygame.sprite.spritecollide(
        hero,
        BombSuppliesGroup,
        True,
        pygame.sprite.collide_mask
    ):
        if hero.BombNumber < 3:
            hero.BombNumber += 1


def run() -> None:
    while hero.LifeNumber > 0:
        for event in pygame.event.get():
            # 退出
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            draw(screen)
            draw_life_line(screen)

            if hero.ListenKeyboard:
                listen_keyboard(event)

            if event.type == BOMB_CD_EVENT:
                pygame.time.set_timer(BOMB_CD_EVENT, 0)

            if event.type == HERO_FIRE_EVENT:
                hero_fire()
            if event.type == ENEMY_FIRE_EVENT:
                for EnemyType, EnemiesList in {
                    'SMALL': SmallEnemiesGroup.sprites(),
                    'MID': MidEnemiesGroup.sprites(),
                    'BIG': BigEnemiesGroup.sprites()
                }.items():
                    for enemy in EnemiesList:
                        if work_enemy_distance(enemy):
                            enemies_fire(
                                EnemiesBulletsGroup,
                                enemy,
                                SMALL_ENEMY_FIRE_SPEED if EnemyType == 'SMALL'else MID_ENEMY_FIRE_SPEED if EnemyType == 'MID' else BIG_ENEMY_FIRE_SPEED
                            )

            if not hero.protecting:
                check_plane_collide()

            if event.type == OFF_PROTECT_EVENT:
                hero.protecting = False
                pygame.time.set_timer(OFF_PROTECT_EVENT, 0)

            if event.type == LISTEN_KEYBOARD_EVENT:
                hero.ListenKeyboard = True
                pygame.time.set_timer(LISTEN_KEYBOARD_EVENT, 0)

            check_bullet_collide()

            update()

            if event.type == CREATE_NEW_SMALL_ENEMY_EVENT:
                create_new_small_enemies()
            if event.type == CREATE_NEW_MID_ENEMY_EVENT:
                create_new_mid_enemies()
            if event.type == CREATE_NEW_BIG_ENEMY_EVENT:
                create_new_big_enemies()

            if event.type == FALL_SUPPLY_EVENT:
                BulletSuppliesGroup.add(
                    BulletSupply(
                        '\\'.join(
                            (IMAGES_PATH,
                             IMAGES_NAMES['BULLET']['SUPPLY_IMAGE'])
                        ),
                        SUPPLY_FALL_SPEED
                    )
                )
                BombSuppliesGroup.add(
                    BombSupply(
                        '\\'.join(
                            (IMAGES_PATH, IMAGES_NAMES['BOMB']['SUPPLY_IMAGE'])
                        ),
                        SUPPLY_FALL_SPEED
                    )
                )

            check_supply_collide()

            if event.type == STOP_HERO_FIRE_TWO_EVENT:
                pygame.time.set_timer(STOP_HERO_FIRE_TWO_EVENT, 0)
                hero.TwoBullet = False
                HeroBulletsGroup.empty()

            # 刷新屏幕
            pygame.display.update()
            print(hero.BombNumber)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    run()
