"""飞船模块"""
import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """"""
    def __init__(self, ai_settings, screen):
        """初始化飞船并设置其初始位置"""
        super().__init__()

        self.screen = screen
        self.ai_settings = ai_settings

        # 创建图片对象(加载飞船图片)
        # 获取图片和屏幕的外接矩形(rect对象/矩形对象)
        self.image = pygame.image.load('images\\ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 设置飞船的位置在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 存储飞船在屏幕底部中央的中心坐标(常数)
        self.down_center_centerx = self.rect.centerx
        self.down_center_centery = self.rect.centery

        # 移动标志(开始为停止状态（False）)
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # 飞船中心X轴坐标(可存浮点数)
        # self.rect.centerx 只能接收整数（只能存整数）
        self.centerx = float(self.rect.centerx)

        # 飞船中心Y轴坐标(原理如上)
        self.centery = float(self.rect.centery)

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        # 向右持续移动
        if self.moving_right and (self.rect.right < self.screen_rect.right):
            self.centerx += self.ai_settings.ship_speed_factor

        # 向左持续移动
        if self.moving_left and (self.rect.left > self.screen_rect.left):
            self.centerx -= self.ai_settings.ship_speed_factor

        # 向上持续移动
        if self.moving_up and (self.rect.top > self.screen_rect.top):
            self.centery -= self.ai_settings.ship_speed_factor

        # 向下持续移动
        if self.moving_down and (self.rect.bottom < self.screen_rect.bottom):
            self.centery += self.ai_settings.ship_speed_factor

        # 更新移动 (这种写法可以将飞船速度设置为浮点数)
        # self.centerx是一个属性可一直保存一个数值(浮点数),如果飞船速度是一个小于1的浮点数
        # 可能前几次循环不足以改变self.rect.centerx的值 通过不断的循环
        # 从而self.centerx就会不断的累加或不断的减少，便可向上或向下突破一个整数
        # 这样就可以改变 self.centerx的值了
        # 因为这种特性使得飞船速度变慢(<1)，符合预期
        # 速度大于1同理
        # 速度2  ：60，62，64，66，68，70   实际速度2
        # 速度1.5：60，61，63，64，66，67   实际速度约为1.5（：1.4）（符合预期）
        # 速度0.5：60，60，61，61，62，62   实际速度约为0.5（：0.4）（符合预期）
        # 这样把飞船速度设置为一个浮点数是没有问题的
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def center_ship(self):
        """把飞船放到底部中央"""
        # 这里代码看起来有点怪，我也没有办法，不这样的话会有bug :(
        self.centerx = self.down_center_centerx
        self.centery = self.down_center_centery
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

