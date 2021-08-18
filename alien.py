"""外星人模块"""
import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """
        表示外星人的类
        只要有一个外星人（不管是自己的一部分还是全部）在屏幕边缘外
                则整个外星人群向下移动（直达条件不成立为止），
                并且改变整个外星人群的左右移动方向（左变右，右变左）
    """

    def __init__(self, ai_settings, screen):
        """初始化外星人，并设置其初始位置"""
        # 初始化一些属性
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen

        # 加载外星人图像，并获取其rect(矩形)
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # 每个外星人初始位置为左上角附近
        # 左边距为图像宽，上边距为图像高
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人(左上角)X坐标（精确度高），可存浮点数
        self.x = float(self.rect.x)

    # 该程序中这个方法只是用来测试，最终程序里没有调用它
    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)

    # 重写update()
    def update(self):
        """更新外星人的位置(具体来说这个方法实现外星人的左移或右移)"""
        # 以下这种写法可以将外星人速度设置为浮点数
        # self.ai_settings.fleet_direction(1 or -1) ：1为右移 -1为左移
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """
            检查外星人(不管是自己的一部分还是全部)是否位于屏幕边缘外
            在边缘外就返回True，否则返回False
        """
        screen_rect = self.screen.get_rect()
        # 在右边缘外
        if self.rect.right >= screen_rect.right:
            return True

        # 在左边缘外
        if self.rect.left <= 0:
            return True

        # 不在边缘外
        return False
