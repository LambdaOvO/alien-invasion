"""子弹模块"""
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """"""
    def __init__(self, ai_settings, screen, ship):
        super().__init__()
        self.screen = screen

        # 在(0,0)处创建一个表示子弹的矩形
        # 之后再设置其正确位置(飞船顶部中央)
        self.rect = pygame.Rect(
            0, 0, ai_settings.bullet_width, ai_settings.bullet_height
        )
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # 存储用小数表示子弹的Y轴坐标（这样会更精确）
        self.y = float(self.rect.y)

        # 子弹基本设置
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    # 重写
    def update(self):
        """更新子弹位置（子弹向上移动）"""
        # 以下这种写法可以将子弹速度设置为浮点数
        # 子弹向上移动
        self.y -= self.speed_factor
        # 更新子弹位置
        self.rect.y = self.y

    def draw_bullet(self):
        """绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)
