"""
飞机大战精灵组
"""

import pygame
from settings import *
from typing import List, Tuple
from random import randint


class Backgroud(pygame.sprite.Sprite):
    """背景"""

    def __init__(self, ImagePath: str, alt=False) -> None:
        # 继承pygame.sprite.Sprite用于把实例加入pygame.sprite.Group实例
        super().__init__()
        # 导入图片
        self.image = pygame.image.load(ImagePath).convert_alpha()
        # 获取图片的Rect对象
        self.rect = self.image.get_rect()
        # 设置图片纵坐标
        # 若alt==True,则该背景是第二张,须在第一张上方,即提高一张背景图片的高度
        # 作用:制造出背景滚动的画面
        if alt:
            self.rect.y = -HEIGHT
        else:
            self.rect.y = 0
        # 设置背景滚动速度
        self.speed = BG_MOVE_SPEED

    def update(self) -> None:
        """移动背景"""
        # 当背景纵坐标>屏幕高度时,代表图片已离开屏幕,此时可以移至屏幕上方
        if self.rect.y >= HEIGHT:
            self.rect.y = -HEIGHT
        # 否则继续向下移动
        else:
            self.rect.y += self.speed


class Hero(pygame.sprite.Sprite):
    """飞机"""

    def __init__(self, ImagePaths: List[str], DownImagePaths: List[str]) -> None:
        # 继承pygame.sprite.Sprite,碰撞检测
        super().__init__()
        # 导入图片
        self.image = pygame.image.load(ImagePaths[0]).convert_alpha()
        self.OtherImage = pygame.image.load(ImagePaths[1]).convert_alpha()
        # 获取图片的Rect对象
        self.rect = self.image.get_rect()
        # 设置横纵坐标
        self.rect.x = (WIDTH - self.rect.width) >> 1
        self.rect.y = HEIGHT - self.rect.height - STATE_HEIGHT
        # 导入坠毁图片
        self.DestroyImages = []
        for DownImagePath in DownImagePaths:
            self.DestroyImages.append(pygame.image.load(DownImagePath).convert_alpha())
        # 设置速度
        self.speed = HERO_MOVE_SPEED
        # alpha通道,用于碰撞检测
        self.mask = pygame.mask.from_surface(self.image)
        # 命数
        self.LifeNumber = HERO_LIFE_NUMBER
        # 当前血量
        self.life = self.rect.width
        # 复活时的无敌帧
        self.protecting = False
        self.ListenKeyboard = True
        self.DrawContinue = False
        self.TwoBullet = False
        self.BombNumber = 0
        self.BombIsCD = False

    def draw(self, screen: pygame.Surface) -> None:
        """绘制"""
        if not self.DrawContinue:
            screen.blit(self.image, self.rect)

    def move_up(self) -> None:
        """飞机向上移动"""
        self.rect.y -= self.speed
        if self.rect.top < 0:
            self.rect.top = 0

    def move_down(self) -> None:
        """飞机向下移动"""
        self.rect.y += self.speed
        if self.rect.bottom > FLY_HEIGHT:
            self.rect.bottom = FLY_HEIGHT

    def move_left(self) -> None:
        """飞机向左移动"""
        self.rect.x -= self.speed
        if self.rect.left < 0:
            self.rect.left = 0

    def move_right(self) -> None:
        """飞机向右移动"""
        self.rect.x += self.speed
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def update(self, draw, DrawLifeLine) -> None:
        """刷新图片"""
        self.image, self.OtherImage = self.OtherImage, self.image
        if self.life <= 0:
            self.protecting = True
            pygame.time.set_timer(OFF_PROTECT_EVENT, OFF_PROTECT_TIME)
            self.ListenKeyboard = False
            pygame.time.set_timer(LISTEN_KEYBOARD_EVENT, LISTEN_KEYBOARD_TIME)
            self.LifeNumber -= 1
            self.destroy(draw, DrawLifeLine)
        if self.protecting:
            self.DrawContinue = not self.DrawContinue
        elif self.DrawContinue:
            self.DrawContinue = False

    def fire(
        self, BulletGroup: pygame.sprite.Group, BulletImagePath: str, Bulletspeed: int
    ) -> None:
        """发射子弹"""
        BulletGroup.add(Bullet(BulletImagePath, self, Bulletspeed))

    def destroy(self, draw, DrawLifeLine) -> None:
        TempImage = self.image
        for DestroyImage in self.DestroyImages:
            self.image = DestroyImage
            draw()
            DrawLifeLine()
            pygame.display.update()
            pygame.time.wait(30)
        else:
            self.life = self.rect.width
        self.image = TempImage
        if self.LifeNumber > 0:
            self.rect.x = (WIDTH - self.rect.width) >> 1
            self.rect.y = HEIGHT - self.rect.height - STATE_HEIGHT


class Enemy(pygame.sprite.Sprite):
    """敌机基类"""

    def __init__(self, ImagePath: str, DownImagePaths: List[str], speed: int) -> None:
        # 继承pygame.sprite.Sprite,碰撞检测
        super().__init__()
        # 导入图片
        self.image = pygame.image.load(ImagePath).convert_alpha()
        # 获取图片的Rect对象
        self.rect = self.image.get_rect()
        # 设置初始位置
        self.rect.bottom = 0
        self.rect.left = randint(0, WIDTH - self.rect.width)
        # 导入坠毁图片
        self.DownImages = []
        for DownImagePath in DownImagePaths:
            self.DownImages.append(pygame.image.load(DownImagePath).convert_alpha())
        # 速度
        self.speed = speed
        # alpha通道,用于碰撞检测
        self.mask = pygame.mask.from_surface(self.image)

    def update(self) -> None:
        """刷新"""
        # 向下移动
        self.rect.y += self.speed
        # 下出上回
        if self.rect.bottom == FLY_HEIGHT:
            self.rect.bottom = 0
            self.rect.x = randint(0, WIDTH - self.rect.width)

    def fire(
        self, BulletGroup: pygame.sprite.Group, BulletImagePath: str, Bulletspeed: int
    ) -> None:
        """发射子弹"""
        BulletGroup.add(Bullet(BulletImagePath, self, Bulletspeed))

    def down(self, draw, DrawLifeLine) -> None:
        """摧毁画面"""
        for DownImage in self.DownImages:
            self.image = DownImage
            draw()
            DrawLifeLine()
            pygame.display.update()
            pygame.time.wait(20)
        self.kill()


class SmallEnemy(Enemy):
    """小型飞机"""

    def __init__(self, ImagePath: str, DownImagePaths: List[str], speed: int) -> None:
        super().__init__(ImagePath, DownImagePaths, speed)


class MidEnemy(Enemy):
    """中型飞机"""

    def __init__(
        self, ImagePaths: List[str], DownImagePaths: List[str], speed: int
    ) -> None:
        super().__init__(ImagePaths[0], DownImagePaths, speed)
        self.HitImage = pygame.image.load(ImagePaths[1]).convert_alpha()
        self.hit = False
        self.life = self.rect.width

    def update(self, draw, DrawLifeLine) -> None:
        super().update()
        if self.life <= self.rect.width * (1 / 3):
            self.image = self.HitImage
        if self.life <= 0:
            self.down(draw, DrawLifeLine)
            self.kill()


class BigEnemy(Enemy):
    """大型飞机"""

    def __init__(
        self,
        ImagePaths: List[str],
        HitImagePath: str,
        DownImagePaths: List[str],
        speed: int,
    ) -> None:
        super().__init__(ImagePaths[0], DownImagePaths, speed)
        self.OtherImage = pygame.image.load(ImagePaths[1]).convert_alpha()
        self.HitImage = pygame.image.load(HitImagePath).convert_alpha()
        self.hit = False
        self.life = self.rect.width

    def update(self, draw, DrawLifeLine) -> None:
        super().update()
        if self.life <= self.rect.width * (1 / 3):
            self.image = self.HitImage
        else:
            self.image, self.OtherImage = self.OtherImage, self.image
        if self.life <= 0:
            self.down(draw, DrawLifeLine)
            self.kill()


class Bullet(pygame.sprite.Sprite):
    """飞机子弹"""

    def __init__(self, ImagePath: str, plane: Hero, speed: int, pos="mid") -> None:
        super().__init__()
        self.image = pygame.image.load(ImagePath).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midbottom = plane.rect.midtop
        if pos == "left":
            self.rect.left = self.rect.left - plane.rect.width * (1 / 6)
        elif pos == "right":
            self.rect.left = self.rect.left + plane.rect.width * (1 / 6)
        self.plane = plane
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)

    def update(self) -> None:
        self.rect.y -= self.speed
        if self.rect.top <= 0:
            self.kill()


class EnemyBullet(Bullet):
    def __init__(self, ImagePath: str, plane: Hero, speed: int) -> None:
        super().__init__(ImagePath, plane, speed, False)
        self.rect.midtop = plane.rect.midbottom

    def update(self) -> None:
        self.rect.y += self.speed
        if self.rect.top >= FLY_HEIGHT or not self.plane.alive():
            self.kill()


class BulletSupply(pygame.sprite.Sprite):
    def __init__(self, ImagePath: str, speed: int) -> None:
        super().__init__()
        self.image = pygame.image.load(ImagePath).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottom = 0
        self.rect.left = randint(0, WIDTH - self.rect.width)
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)

    def update(self) -> None:
        self.rect.bottom += self.speed
        if self.rect.top >= HEIGHT:
            self.kill()


class BombSupply(BulletSupply):
    def __init__(self, ImagePath: str, speed: int) -> None:
        super().__init__(ImagePath, speed)


class LifeNumberPic(pygame.sprite.Sprite):
    def __init__(
        self,
        ImagePath: str,
        number: int,
        pos: Tuple[int],
    ) -> None:
        super().__init__()
        self.image = pygame.image.load(ImagePath).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos[0] - self.rect.width, pos[1]
        self.number = number

    def update(self, HeroLifeNumber: int):
        if self.number > HeroLifeNumber - 1:
            self.kill()


class BombPic(LifeNumberPic):
    def __init__(self, ImagePath: str, number: int, pos: Tuple[int]) -> None:
        super().__init__(ImagePath, number, pos)
        self.rect.topleft = pos

    def update(self):
        return
