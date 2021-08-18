"""游戏设置模块"""


class Settings():
    """存储该游戏的所有设置的类"""

    def __init__(self):
        """初始化游戏设置"""
        # *****静态设置*******

        # 屏幕大小
        self.screen_width = 1200
        self.screen_height = 800
        # 背景颜色
        self.bg_color = (230, 230, 230)

        # 飞船的设置
        # 游戏初始化时可用飞船数量（生命数：self.ship_limit + 1）(定值)
        self.ship_limit = 3

        # 子弹设置

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        # 限制屏幕中的子弹数量(这里设置最多3个)
        self.bullets_allowed = 3

        # 外星人设置
        # 外星人群下移的距离(速度)
        self.fleet_drop_factor = 10

        # 游戏节奏的提高速度(倍数)
        self.speedup_scale = 1.1

        # 外星人点数的提高速度(倍数)
        self.score_scale = 1.5

        # ****动态设置*****

        # 初始化游戏动态设置
        self.initialize_dynamic_settings()

        # god
        self.god = False

    def initialize_dynamic_settings(self):
        """(初始化/重置)游戏动态设置"""
        # 飞船的速度(可以为浮点数)
        self.ship_speed_factor = 0.5
        # 子弹的速度(可以为浮点数)
        self.bullet_speed_factor = 1
        # 外星人左右移动的速度(可以为浮点数)
        self.alien_speed_factor = 0.2

        # (外星人群)self.fleet_direction 1为外星人群向右移 -1为外星人群向左移
        # 游戏一开始时为右移
        self.fleet_direction = 1

        # 外星人点数(一开始为50分)
        self.alien_points = 50

    def increase_speed(self):
        """提高游戏整体速度,提高外星人点数"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        # 外星人点数是个整数
        self.alien_points = int(self.alien_points * self.score_scale)




