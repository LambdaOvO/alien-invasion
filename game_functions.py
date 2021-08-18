"""游戏中的一些函数"""
import sys
import pygame
import json
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets):
    """监听keydown事件"""

    # 飞船开始移动
    # 飞船开始右移
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    # 飞船开始左移
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    # 飞船开始上移
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    # 飞船开始下移
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True

    # 生成子弹，并将其加入到编组bullets中
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)

    # 按q退出游戏
    elif event.key == pygame.K_q:
        # 将最高得分存在这个 'json_files/high_score.json' 文件中
        with open('json_files/high_score.json', 'w') as file_object:
            json.dump(stats.high_score, file_object)

        # 退出游戏
        sys.exit()


    # 按P 若条件成立则(开始/重开)游戏
    elif event.key == pygame.K_p:
        # 查看是否存在play按钮（是否为游戏结束状态）
        if not stats.game_active:
            # 存在play按钮，(开始/重开)游戏
            # 执行一些措施
            start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)
        else:
            # 不存在play按钮，则什么也不做
            pass

    # 按G (开启/关闭)上帝模式
    elif event.key == pygame.K_g:
        god_model(ai_settings, stats)


def check_keyup_events(event, ship):
    """监听keyup事件"""

    # 停止移动飞船
    # 飞船停止右移
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    # 飞船停止左移
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    # 飞船停止上移
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    # 飞船停止下移
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_events(
        ai_settings, screen, stats, sb, play_button, ship, aliens, bullets
):
    """ 监听事件"""
    for event in pygame.event.get():
        # 退出(监听退出事件)
        if event.type == pygame.QUIT:
            # 将高得分存在这个 'json_files/high_score.json' 文件中
            with open('json_files/high_score.json', 'w') as file_object:
                json.dump(stats.high_score, file_object)

            # 退出游戏
            sys.exit()

        # 监听keydown事件
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets)

        # 监听keyup事件
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        # 监听鼠标点击事件
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 获取点击时鼠标的坐标
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # 查看是否存在play按钮（是否为游戏结束状态）
            if not stats.game_active:
                # 存在play按钮，查看玩家是否点击了play按钮
                check_play_button(
                    ai_settings, screen, stats, sb, play_button,
                    ship, aliens, bullets, mouse_x, mouse_y
                )


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """更新屏幕"""
    # 以下是重新绘制屏幕：

    # 绘制一个单色平面（将填充整个屏幕）
    screen.fill(ai_settings.bg_color)

    # 以下是绘制物体，覆盖关系为：可视化统计信息> 按钮 >外星人 > 飞船 > 子弹
    # 绘制所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # 绘制一个飞船
    ship.blitme()

    # 在屏幕上绘制一群外星人
    # 编组调用draw()时，pygame自动绘制编组中的每个元素,
    #                 绘制位置由元素的rect决定(不是调用Alien类中的blitme(),
    #                                        是调用pygame自带的绘制方法)
    aliens.draw(screen)

    # 如果是游戏结束状态，则绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 绘制可视化统计信息
    # 绘制记分牌
    sb.show_score()

    # 让最近绘制的屏幕可见(擦去旧屏幕，显示新屏幕)
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
        更新所有子弹的位置，并删除已经消失的子弹, 检测外星人与子弹的碰撞并采取措施
        当所有外星人都被消灭后再生成一群外星人
    """
    # 更新所有子弹的位置 (编组调用update()方法使得编组中的所有元素都调用各自的update()方法)
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    # 检测碰撞并采取措施
    # 当所有外星人都被消灭后再生成一群外星人，并提高游戏整体速度，提高外星人点数
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def fire_bullet(ai_settings, screen, ship, bullets):
    """生成子弹，并将其加入到编组bullets中"""
    if len(bullets) < ai_settings.bullets_allowed:
        # len(bullets)就是在屏幕中的子弹数量
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def creat_fleet(ai_settings, screen, ship, aliens):
    """给外星人编组(aliens)中添加一群外星人(默认位置)"""

    # 创建一个外星人并不绘制它，只需要它的宽和高
    # 外星人间距为外星人图像宽度
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height

    # 计算最多可以有多少行
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien_height)
    # 计算一行最多可以有多少个外星人
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)

    # 减少一行，降低难度
    number_rows -= 1

    # 创建一群外星人(number_rows行)
    for row_number in range(number_rows):
        # 创建一行外星人 (一行 number_aliens_x 个)
        for alien_number in range(number_aliens_x):
            # 创建一个外星人并将其放在当前行中
            create_alien(
                ai_settings, screen, aliens,
                alien_width, alien_height,
                alien_number, row_number
            )


def get_number_aliens_x(ai_settings, alien_width):
    """计算一行最多可以有多少个外星人，间距为外星人的图像宽度"""
    # 计算一行的可用空间
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    # 计算一行最多可以有多少个外星人(整数)
    number_aliens_x = int(available_space_x / (2 * alien_width))

    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算最多可以有多少行外星人，行间距为外星人的图像高度"""
    # 可用空间
    available_space_y = ai_settings.screen_height - ship_height - alien_height
    # 计算行数(整数)
    number_aliens_y = int(available_space_y / (2 * alien_height))

    return number_aliens_y


def create_alien(
        ai_settings, screen, aliens,
        alien_width, alien_height,
        alien_number, row_number
):
    """创建一个外星人并将其放在当前行中"""
    # 创建一个外星人
    alien = Alien(ai_settings, screen)

    # 依次序设置外星人的初始位置:（左上角）X坐标Y坐标
    alien.x = alien_width + (2 * alien_number * alien_width)
    alien.rect.x = alien.x
    alien.rect.y = alien_height + (2 * row_number * alien_height)

    # 添加到外星人编组中
    aliens.add(alien)


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """
        更新所有外星人的位置,查看外星人与飞船的碰撞 和 外星人是否飞到屏幕边缘下
                            并采取相应的措施
    """
    # 检查外星人(不管是自己的一部分还是全部)是否位于屏幕边缘外，
    #                                   如果是采取相应的措施。
    check_fleet_edges(ai_settings, aliens)

    # 编组调用update()方法,使得编组中的所有元素都调用各自的update()方法
    aliens.update()

    # 检测外星人与飞船的碰撞并采取相应的措施
    # spritecollideany()这个函数当飞船对象与外星人编组中的某个元素发生碰撞时(rect碰撞)
    #                   返回该元素(第一个发生碰撞的元素)  否则返回None
    if pygame.sprite.spritecollideany(ship, aliens):
        # 外星人与飞船发生碰撞
        # 措施
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

    # 查看外星人是否在屏幕边缘下，如果是采取相应的措施
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)


def change_fleet_direction(ai_settings, aliens):
    """措施：将整个外星人群下移，并改变它们的方向"""

    # 整个外星人群下移
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_factor

    # 改变方向
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    """
        检查外星人(不管是自己的一部分还是全部)是否位于屏幕边缘外，
        外星人在边缘外时采取相应的措施。
        具体：只要有一个外星人（不管是自己的一部分还是全部）在屏幕边缘外
                则整个外星人群向下移动（直达条件不成立为止），
                并且改变整个外星人群的左右移动方向（左变右，右变左）
    """
    # 检查外星人(不管是自己的一部分还是全部)是否位于屏幕边缘外，
    for alien in aliens.sprites():

        #   True:在边缘外   False：不在边缘外
        if alien.check_edges():
            # 执行措施
            change_fleet_direction(ai_settings, aliens)
            # 游戏主循环中，一次循环最多执行该措施一次，所以用break
            break


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
        检测外星人与子弹的碰撞并采取措施
        当所有外星人都被消灭后再生成一群外星人，并提高游戏整体速度,提高外星人点数,提高玩家等级
    """
    # 检测是否有子弹和外星人碰撞
    # 如果发生碰撞，就删除相应的子弹和外星人,并增加得分
    # groupcollide()是一个检测碰撞并采取措施的函数（返回值为一个dict）
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        # 发生碰撞
        for aliens_s in collisions.values():
            # 加分
            stats.score += ai_settings.alien_points * len(aliens_s)

        # 重新渲染得分图像
        sb.prep_score()
        # 查看是否出现了新的最高得分,并采取措施
        check_high_score(stats, sb)

    # 当所有外星人都被消灭后，删除现有子弹，把飞船放到底部中央，并新建一群外星人，
    # 提高游戏整体速度,提高外星人点数,提高玩家等级
    if len(aliens) == 0:
        # 清空子弹编组
        bullets.empty()

        # 飞船放到底部中央
        ship.center_ship()
        # 新建一群外星人
        creat_fleet(ai_settings, screen, ship, aliens)

        # 提高游戏整体速度, 提高外星人点数
        ai_settings.increase_speed()

        # 提高玩家等级
        stats.level += 1
        # 重新渲染玩家等级图像
        sb.prep_level()

        # 暂停0.1秒，让玩家准备一下
        sleep(0.1)


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """
        外星人与飞船碰撞 或 外星人飞到屏幕边缘下
        所采取的具体措施
        提前检测一下游戏是否可用进入结束状态
    """
    # 检测一下游戏是否可用进入结束状态
    if stats.ships_left > 0:
        #  游戏没有结束，还是进行状态

        # 将可用飞船数量-1
        stats.ships_left -= 1

        # 更新玩家可用飞船数量图像(-1)
        sb.prep_ships()

        # 清空子弹编组和外星人编组
        bullets.empty()
        aliens.empty()

        # 重置飞船的位置（放到底部中央）
        ship.center_ship()
        # 创建新的外星人群，
        creat_fleet(ai_settings, screen, ship, aliens)

        # 暂停0.5秒,让玩家准备一下
        sleep(0.5)

    else:
        # 游戏结束
        stats.game_active = False
        # 并显示光标
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """查看外星人是否在屏幕边缘下，如果是采取相应的措施"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        # 查看
        if alien.rect.bottom > screen_rect.bottom:
            # 措施
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            # 不管是一个还是多个在屏幕边缘下，措施只执行一次
            break


def check_play_button(
        ai_settings, screen, stats, sb, play_button,
        ship, aliens, bullets, mouse_x, mouse_y
):
    """
        查看玩家是否点击了play按钮

        如果点击play按钮，采取一些措施
    """
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        # 点击play按钮

        # 措施
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)


def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
        措施：(开始/重开)游戏 (将游戏状态设置为进行状态)，并重置游戏,隐藏光标
    """
    # 游戏状态设置为游戏进行状态
    stats.game_active = True

    # ***重置游戏***

    # 重置游戏动态设置
    ai_settings.initialize_dynamic_settings()

    # 重置游戏的统计信息
    stats.reset_stats()
    # 重新渲染记分牌的一些图像
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    # 重新设置玩家可用飞船数量图像
    sb.prep_ships()

    # 清空外星人和子弹编组
    aliens.empty()
    bullets.empty()

    # 重置飞船的位置（放到底部中央）
    ship.center_ship()
    # 创建新的外星人群
    creat_fleet(ai_settings, screen, ship, aliens)

    # ***隐藏光标****
    pygame.mouse.set_visible(False)


def god_model(ai_settings, stats):
    """ 开启/关闭 上帝模式 """

    if not ai_settings.god:
        # 开启上帝模式
        # 设置为开启上帝模式
        ai_settings.god = True
        # 子弹速度加快10倍
        ai_settings.bullet_speed_factor *= 5
        # 加大子弹宽度
        ai_settings.bullet_width = 1000
        # 将限制屏幕中的子弹数量乘10（屏幕中的子弹数量最多为30个，相当于无限制）
        ai_settings.bullets_allowed *= 10
    else:
        # 关闭上帝模式
        # 设置为关闭上帝模式
        ai_settings.god = False
        # 一切回归正常
        # 子弹速度
        ai_settings.bullet_speed_factor = ai_settings.speedup_scale ** (stats.level - 1)
        # 子弹宽度
        ai_settings.bullet_width = 3
        # 限制屏幕中的子弹数量
        ai_settings.bullets_allowed = 3


def check_high_score(stats, sb):
    """ 查看是否出现了新的最高得分,并采取措施 """
    if stats.score > stats.high_score:
        # 出现了新的最高分

        # 改值
        stats.high_score = stats.score
        # 重新渲染最高得分图像
        sb.prep_high_score()
