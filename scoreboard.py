"""记分牌模块"""
import pygame
from pygame.sprite import Group
from ship import Ship


class Scoreboard():
    """记分牌类"""

    def __init__(self, ai_settings, screen, stats):
        """初始化积分牌"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # 设置得分文本
        self.text_color = (30, 30, 30)
        # 默认字体，字号47
        self.font = pygame.font.SysFont(None, 47)

        # 初始化得分图像
        self.prep_score()

        # 初始化最高得分图像
        self.prep_high_score()

        # 初始化玩家等级图像
        self.prep_level()

        # 初始化飞船编组(用来显示玩家还有多少辆飞船可用)
        self.prep_ships()

    def prep_score(self):
        """  将'得分文本'渲染为'得分图像'  """

        # 将得分圆整到最近的10的整倍数
        # 1，2，3，4向下圆整，5，6，7，8，9，向上圆整
        round_score = int(round(self.stats.score, -1))

        # 格式化，千分位(每三位加一个逗号)
        score_str = "{:,}".format(round_score)

        # 创建得分图像
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        # 设置得分图像的位置：为游戏屏幕右上角(右/上边距都为20像素)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """  将'最高得分文本'渲染成'最高得分图像'   """

        # 将最高得分圆整到最近的10的整倍数
        # 1，2，3，4向下圆整，5，6，7，8，9，向上圆整
        high_score = int(round(self.stats.high_score, -1))

        # 格式化，千分位(每三位加一个逗号)
        high_score_str = "{:,}".format(high_score)

        # 创建最高得分图像
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.ai_settings.bg_color
        )

        # 设置最高得分图像的位置：屏幕底端中央(与得分图像水平)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """  将'玩家等级文本'渲染成'玩家等级图像' """

        # 创建玩家等级图像
        self.level_image = self.font.render(
            str(self.stats.level), True, self.text_color, self.ai_settings.bg_color
        )

        # 设置玩家等级图像的位置：在得分图像的下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """ 创建飞船编组,用图像来显示玩家还有多少辆飞船可用(玩家可用飞船数量图像) """

        # 创建飞船编组
        self.ships = Group()

        # 给飞船编组添加飞船并设置其正确位置
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """在屏幕上显示得分和最高得分,以及玩家等级"""

        # 绘制得分图像
        self.screen.blit(self.score_image, self.score_rect)

        # 绘制最高得分图像
        self.screen.blit(self.high_score_image, self.high_score_rect)

        # 绘制玩家等级图像
        self.screen.blit(self.level_image, self.level_rect)

        # 绘制可用飞船
        self.ships.draw(self.screen)
