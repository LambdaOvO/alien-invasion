"""
    游戏：飞船射击外星人/外星人入侵（alien invasion）
    交流： qq:2499487471
            邮箱：2499487471@qq.com
    玩法：上下左右键控制飞船，空格发射子弹，每消灭一波外星人将提升游戏难度。
            q:退出游戏   p:开始/重开游戏
"""
from time import sleep
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    """"""
    # 初始化游戏，创建一个设置对象(程序从头到尾只有这一个设置对象(实例))
    # 一个屏幕对象，指定游戏标题
    pygame.init()
    ai_settings = Settings()
    # 该程序没有定义屏幕类，屏幕对象来自于pygame库
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")

    # 创建一个飞船对象(游戏自始至终只有这一个飞船对象，只是通过数值来模拟有多个可用的飞船)
    ship = Ship(ai_settings, screen)

    # 创建一个用于存储子弹的Group(子弹编组)
    bullets = Group()

    # 创建一个用于存储一群外星人的Group(外星人编组)
    aliens = Group()

    # 给外星人编组(aliens)中添加一群外星人
    gf.creat_fleet(ai_settings, screen, ship, aliens)

    # 创建游戏统计信息对象
    stats = GameStats(ai_settings)

    # 创建记分牌对象
    sb = Scoreboard(ai_settings, screen, stats)

    # 创建Play按钮(对象)
    play_button = Button(ai_settings, screen, 'Play')

    # 游戏主循环
    while True:
        # 监听事件
        gf.check_events(
            ai_settings, screen, stats, sb, play_button, ship, aliens, bullets
        )

        # 游戏进行状态：运行这些代码，游戏结束状态：不运行这些代码
        if stats.game_active:
            # 更新飞船位置
            ship.update()

            # 更新所有子弹的位置，并删除已经消失的子弹, 检测外星人与子弹的碰撞并采取措施
            # 当所有外星人都被消灭后再生成一群外星人,并提高游戏整体速度,提高外星人点数
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)

            # 更新所有外星人的位置,查看外星人与飞船的碰撞 和 外星人是否飞到屏幕边缘下
            #                   并采取相应的措施
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)

        # 更新屏幕
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


if __name__ == '__main__':
    run_game()


