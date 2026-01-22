import time

import numpy as np
from qfluentwidgets import FluentIcon

from ok import TriggerTask, Logger
from src.tasks.BaseEfTask import BaseEfTask

logger = Logger.get_logger(__name__)


class AutoCombatTask(BaseEfTask, TriggerTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_config = {'_enabled': True}
        self.name = "自动战斗"
        self.description = "自动战斗"
        self.icon = FluentIcon.ACCEPT
        self.skill_sequence = ["1", "2", "4"]

    def run(self):
        bar_count = self.get_skill_bar_count()
        if self.get_skill_bar_count() < 0 or not self.in_team():
            return
        self.log_info('enter combat {}'.format(bar_count))
        self.screenshot('enter_combat')
        while True:
            skill_count = self.get_skill_bar_count()
            if skill_count < 0:
                self.log_info("自动战斗结束!", notify=self.in_bg())
                self.screenshot('out_of_combat')
                break
            elif self.use_e_skill():
                continue
            elif self.use_ult():
                continue
            elif skill_count == 3:
                last_count = skill_count
                i = 0
                while True:
                    current_count = self.get_skill_bar_count()
                    if current_count <= 0:
                        self.log_debug("skill count less than 0 while using skills {}".format(current_count))
                        break
                    if current_count != last_count:
                        i += 1
                        self.log_debug("skill success use next".format(i))
                        if i >= len(self.skill_sequence):
                            break
                    # use skill
                    start = time.time()
                    while time.time() - start < 3:
                        if self.get_skill_bar_count() == current_count:
                            self.send_key(self.skill_sequence[i], after_sleep=0.1)
                        elif self.get_skill_bar_count() < current_count:
                            self.log_debug('use skill success')
                            break
            else:
                self.send_key("9",  after_sleep=0.1)
            self.sleep(0.1)

    def use_ult(self):
        ults = ['1', '2', '3', '4']
        for ult in ults:
            if self.find_one("ult_" + ult):
                self.send_key_down(ult)
                self.wait_until(lambda :not self.in_combat())
                self.send_key_up(ult)
                self.wait_until(self.in_combat)
                return True

    def use_e_skill(self):
        if skill_e := self.find_one('skill_e', threshold=0.7):
            self.log_debug('found skill e {}'.format(skill_e))
            self.send_key('e', after_sleep=0.1)
            return True

    def in_combat(self):
        return self.get_skill_bar_count() >= 0 and self.in_team()

    def in_team(self):
        return self.find_one('skill_1') and self.find_one('skill_2') and self.find_one('skill_3') and self.find_one('skill_4')

    def get_skill_bar_count(self):
        count = 0
        if self.check_is_pure_color_in_4k(1604, 1958, 1796, 1964, yellow_skill_color):
            count += 1
            if self.check_is_pure_color_in_4k(1824, 1958, 2013, 1964, yellow_skill_color):
                count += 1
                if self.check_is_pure_color_in_4k(2043, 1958, 2231, 1964, yellow_skill_color):
                    count += 1
        if count == 0:
            # self.log_debug('count is 0, check left white')
            has_white_left = self.check_is_pure_color_in_4k(1604, 1958, 1614, 1964, white_skill_color)
            if not has_white_left:
                count = -1
        return count

    def check_is_pure_color_in_4k(self, x1, y1, x2, y2, color_range=None):
        bar = self.frame[self.height_of_screen(y1 / 2160):self.height_of_screen(y2 / 2160),
                    self.width_of_screen(x1 / 3840):self.width_of_screen(x2 / 3840)]

        if bar.size == 0:
            return False

        first_column = bar[:, 0:1]
        diff = np.abs(bar.astype(np.int16) - first_column.astype(np.int16))
        is_pure = np.all(diff <= 2)

        if not is_pure:
            return False

        if color_range:
            b, g, r = bar[0, 0]
            if not (color_range['r'][0] <= r <= color_range['r'][1]): return False
            if not (color_range['g'][0] <= g <= color_range['g'][1]): return False
            if not (color_range['b'][0] <= b <= color_range['b'][1]): return False

        return True
        

yellow_skill_color = {
    'r': (230, 255),  # Red range
    'g': (200, 255),  # Green range
    'b': (0, 85)  # Blue range
}

white_skill_color = {
    'r': (205, 255),  # Red range
    'g': (205, 255),  # Green range
    'b': (205, 255)  # Blue range
}


