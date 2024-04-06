<<<<<<< HEAD
"""
飞机大战游戏设置
"""

import pygame


# 屏幕大小(背景图片大小)
WIDTH, HEIGHT = SCREEN_SIZE = (480, 700)

# 阅读建议时间 单位:毫秒
READING_TIME = 1000

# 背景滚动速度
BG_MOVE_SPEED = 4

# 状态栏高度
STATE_HEIGHT = 60
# 飞行高度
FLY_HEIGHT = HEIGHT - STATE_HEIGHT

# 飞机移动速度
HERO_MOVE_SPEED = 10
# 飞机命数
HERO_LIFE_NUMBER = 3

# 小型敌机移动速度
SMALL_ENEMY_MOVE_SPEED = 3
# 中型敌机移动速度
MID_ENEMY_MOVE_SPEED = 2
# 大型敌机移动速度
BIG_ENEMY_MOVE_SPEED = 1

SUPPLY_FALL_SPEED = 6

# 血条厚度
LIFE_LINE_HEIGHT = 3

# 长按键盘 首次发送信号延迟&连续发送信号间隔 单位:毫秒
KEYBOARD_DELAY = 15
INTERVAL = 15

# 飞机&敌机发射子弹速度
HERO_FIRE_SPEED = 20
SMALL_ENEMY_FIRE_SPEED = 30
MID_ENEMY_FIRE_SPEED = 20
BIG_ENEMY_FIRE_SPEED = 10

# 击中飞机&敌机伤害
FIRED_HERO = 5
FIRED_ENEMY = 10

# 敌机发射子弹距离
ENEMY_FIRE_DISTANCE = 200

# 背景&敌机移动事件&发送间隔时间 单位:毫秒
UPDATE_EVENT = pygame.USEREVENT
UPDATE_TIME = 50

# 单次创建小型敌机数量
EACH_CREATE_SMALL_ENEMY_NUMBER = 3
# 创建新小型敌机事件&时间间隔 单位:毫秒
CREATE_NEW_SMALL_ENEMY_EVENT = pygame.USEREVENT + 1
CREATE_NEW_SMALL_ENEMY_TIME = 3000

# 单次创建中型敌机数量
EACH_CREATE_MID_ENEMY_NUMBER = 2
# 创建新中型敌机事件&时间间隔 单位:毫秒
CREATE_NEW_MID_ENEMY_EVENT = pygame.USEREVENT + 2
CREATE_NEW_MID_ENEMY_TIME = 5000

# 单次创建大型敌机数量
EACH_CREATE_BIG_ENEMY_NUMBER = 1
# 创建新大型敌机事件&时间间隔 单位:毫秒
CREATE_NEW_BIG_ENEMY_EVENT = pygame.USEREVENT + 3
CREATE_NEW_BIG_ENEMY_TIME = 7000

# 取消飞机无敌帧事件&时间间隔 单位:毫秒
OFF_PROTECT_EVENT = pygame.USEREVENT + 4
OFF_PROTECT_TIME = 5000

# 飞机发射子弹事件&时间间隔 单位:毫秒
HERO_FIRE_EVENT = pygame.USEREVENT + 5
HERO_FIRE_TIME = 125

# 敌机发射子弹事件&时间间隔 单位:毫秒
ENEMY_FIRE_EVENT = pygame.USEREVENT + 6
ENEMY_FIRE_TIME = 200

# 恢复监听键盘事件&时间
LISTEN_KEYBOARD_EVENT = pygame.USEREVENT + 7
LISTEN_KEYBOARD_TIME = 700

# 掉落物事件&时间
FALL_SUPPLY_EVENT = pygame.USEREVENT + 8
FALL_SUPPLY_TIME = 10000

# 停止飞机同事发射两发子弹事件&时间
STOP_HERO_FIRE_TWO_EVENT = pygame.USEREVENT + 9
STOP_HERO_FIRE_TWO_TIME = 30000

# 炸弹CD事件&时间
BOMB_CD_EVENT = pygame.USEREVENT + 10
BOMB_CD_TIME = 3000


# 图片文件夹
IMAGES_PATH = "D:/Program/Files/game/plane/images"
# 游戏元素&图片名
IMAGES_NAMES = {
    "ICON": "life.png",
    "BG": "background.png",
    "HERO": {
        "IMAGE": ["me1.png", "me2.png"],
        "LIFE_IMAGE": "life.png",
        "DESTROY": [
            "me_destroy_1.png",
            "me_destroy_2.png",
            "me_destroy_3.png",
            "me_destroy_4.png",
        ],
    },
    "SMALL_ENEMY": {
        "IMAGE": "enemy1.png",
        "DOWN_IMAGE": [
            "enemy1_down1.png",
            "enemy1_down2.png",
            "enemy1_down3.png",
            "enemy1_down4.png",
        ],
    },
    "MID_ENEMY": {
        "IMAGE": ["enemy2.png", "enemy2_hit.png"],
        "DOWN_IMAGE": [
            "enemy2_down1.png",
            "enemy2_down2.png",
            "enemy2_down3.png",
            "enemy2_down4.png",
        ],
    },
    "BIG_ENEMY": {
        "IMAGE": ["enemy3_n1.png", "enemy3_n2.png"],
        "HIT_IMAGE": "enemy3_hit.png",
        "DOWN_IMAGE": [
            "enemy3_down1.png",
            "enemy3_down2.png",
            "enemy3_down3.png",
            "enemy3_down4.png",
            "enemy3_down5.png",
            "enemy3_down6.png",
        ],
    },
    "BULLET": {
        "IMAGE": ["bullet1.png", "bullet2.png"],
        "SUPPLY_IMAGE": "bullet_supply.png",
    },
    "BOMB": {"SHOW_IMAGE": "bomb.png", "SUPPLY_IMAGE": "bomb_supply.png"},
}
=======
"""
飞机大战游戏设置
"""

import pygame


# 屏幕大小(背景图片大小)
WIDTH, HEIGHT = SCREEN_SIZE = (480, 700)

# 阅读建议时间 单位:毫秒
READING_TIME = 1000

# 背景滚动速度
BG_MOVE_SPEED = 4

# 状态栏高度
STATE_HEIGHT = 60
# 飞行高度
FLY_HEIGHT = HEIGHT - STATE_HEIGHT

# 飞机移动速度
HERO_MOVE_SPEED = 10
# 飞机命数
HERO_LIFE_NUMBER = 3

# 小型敌机移动速度
SMALL_ENEMY_MOVE_SPEED = 3
# 中型敌机移动速度
MID_ENEMY_MOVE_SPEED = 2
# 大型敌机移动速度
BIG_ENEMY_MOVE_SPEED = 1

SUPPLY_FALL_SPEED = 6

# 血条厚度
LIFE_LINE_HEIGHT = 3

# 长按键盘 首次发送信号延迟&连续发送信号间隔 单位:毫秒
KEYBOARD_DELAY = 15
INTERVAL = 15

# 飞机&敌机发射子弹速度
HERO_FIRE_SPEED = 20
SMALL_ENEMY_FIRE_SPEED = 30
MID_ENEMY_FIRE_SPEED = 20
BIG_ENEMY_FIRE_SPEED = 10

# 击中飞机&敌机伤害
FIRED_HERO = 5
FIRED_ENEMY = 10

# 敌机发射子弹距离
ENEMY_FIRE_DISTANCE = 200

# 背景&敌机移动事件&发送间隔时间 单位:毫秒
UPDATE_EVENT = pygame.USEREVENT
UPDATE_TIME = 50

# 单次创建小型敌机数量
EACH_CREATE_SMALL_ENEMY_NUMBER = 3
# 创建新小型敌机事件&时间间隔 单位:毫秒
CREATE_NEW_SMALL_ENEMY_EVENT = pygame.USEREVENT + 1
CREATE_NEW_SMALL_ENEMY_TIME = 3000

# 单次创建中型敌机数量
EACH_CREATE_MID_ENEMY_NUMBER = 2
# 创建新中型敌机事件&时间间隔 单位:毫秒
CREATE_NEW_MID_ENEMY_EVENT = pygame.USEREVENT + 2
CREATE_NEW_MID_ENEMY_TIME = 5000

# 单次创建大型敌机数量
EACH_CREATE_BIG_ENEMY_NUMBER = 1
# 创建新大型敌机事件&时间间隔 单位:毫秒
CREATE_NEW_BIG_ENEMY_EVENT = pygame.USEREVENT + 3
CREATE_NEW_BIG_ENEMY_TIME = 7000

# 取消飞机无敌帧事件&时间间隔 单位:毫秒
OFF_PROTECT_EVENT = pygame.USEREVENT + 4
OFF_PROTECT_TIME = 5000

# 飞机发射子弹事件&时间间隔 单位:毫秒
HERO_FIRE_EVENT = pygame.USEREVENT + 5
HERO_FIRE_TIME = 125

# 敌机发射子弹事件&时间间隔 单位:毫秒
ENEMY_FIRE_EVENT = pygame.USEREVENT + 6
ENEMY_FIRE_TIME = 200

# 恢复监听键盘事件&时间
LISTEN_KEYBOARD_EVENT = pygame.USEREVENT + 7
LISTEN_KEYBOARD_TIME = 700

# 掉落物事件&时间
FALL_SUPPLY_EVENT = pygame.USEREVENT + 8
FALL_SUPPLY_TIME = 10000

# 停止飞机同事发射两发子弹事件&时间
STOP_HERO_FIRE_TWO_EVENT = pygame.USEREVENT + 9
STOP_HERO_FIRE_TWO_TIME = 30000

# 炸弹CD事件&时间
BOMB_CD_EVENT = pygame.USEREVENT + 10
BOMB_CD_TIME = 3000


# 图片文件夹
IMAGES_PATH = "./images"
# 游戏元素&图片名
IMAGES_NAMES = {
    "ICON": "icon.ico",
    "BG": "background.png",
    "HERO": {
        "IMAGE": ["me1.png", "me2.png"],
        "LIFE_IMAGE": "life.png",
        "DESTROY": [
            "me_destroy_1.png",
            "me_destroy_2.png",
            "me_destroy_3.png",
            "me_destroy_4.png",
        ],
    },
    "SMALL_ENEMY": {
        "IMAGE": "enemy1.png",
        "DOWN_IMAGE": [
            "enemy1_down1.png",
            "enemy1_down2.png",
            "enemy1_down3.png",
            "enemy1_down4.png",
        ],
    },
    "MID_ENEMY": {
        "IMAGE": ["enemy2.png", "enemy2_hit.png"],
        "DOWN_IMAGE": [
            "enemy2_down1.png",
            "enemy2_down2.png",
            "enemy2_down3.png",
            "enemy2_down4.png",
        ],
    },
    "BIG_ENEMY": {
        "IMAGE": ["enemy3_n1.png", "enemy3_n2.png"],
        "HIT_IMAGE": "enemy3_hit.png",
        "DOWN_IMAGE": [
            "enemy3_down1.png",
            "enemy3_down2.png",
            "enemy3_down3.png",
            "enemy3_down4.png",
            "enemy3_down5.png",
            "enemy3_down6.png",
        ],
    },
    "BULLET": {
        "IMAGE": ["bullet1.png", "bullet2.png"],
        "SUPPLY_IMAGE": "bullet_supply.png",
    },
    "BOMB": {"SHOW_IMAGE": "bomb.png", "SUPPLY_IMAGE": "bomb_supply.png"},
}
>>>>>>> b344d4e (第一次尝试)
