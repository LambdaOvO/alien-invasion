"""游戏统计信息模块"""
import json

class GameStats():
    """游戏统计信息类"""
    def __init__(self, ai_settings):

        self.ai_settings = ai_settings

        # 可用飞船数量（生命数）
        self.ships_left = self.ai_settings.ship_limit

        # 得分
        self.score = 0

        # 最高得分(只要在得分超过历史最高得分时，才会改变数值)
        # 最高得分存在这个 'json_files/high_score.json' 文件中，从中取出
        with open('json_files/high_score.json') as file_object:
            self.high_score = int(json.load(file_object))

        # 玩家等级(游戏开始时为1级)
        self.level = 1

        # 游戏(进行/结束)标志 True:游戏进行状态， False：游戏结束状态 （刚启动时为结束状态）
        # 这个是游戏内容的(进行/结束)标志 ，不是整个程序的(进行/结束)标志
        self.game_active = False

    def reset_stats(self):
        """重置游戏中的某些统计信息"""
        # 重置生命数，得分，玩家等级
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
