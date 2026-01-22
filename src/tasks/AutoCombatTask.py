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
        self.trigger_interval = 0.2
        self.name = "自动战斗"
        self.description = "自动战斗"
        self.icon = FluentIcon.ACCEPT
        self.scene: WWScene | None = None
        self.skill_sequence = ["2", "2", "1"]

    def run(self):
        bar_count = self.get_skill_bar_count()
        if self.get_skill_bar_count() < 0:
            return
        self.log_info('enter combat {}'.format(bar_count))
        while True:
            skill_count = self.get_skill_bar_count()
            if skill_count < 0:
                self.log_info("自动战斗结束!", notify=self.in_bg())
                self.screenshot('out_of_combat')
                break
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
                            self.send_key(self.skill_sequence[0], after_sleep=0.1)
                        elif self.get_skill_bar_count() < current_count:
                            self.log_debug('use skill success')
                            break
            else:
                self.send_key("0", after_sleep=0.1)
            self.sleep(0.1)

    def in_combat(self):
        return self.get_skill_bar_count() >= 0

    def get_skill_bar_count(self):
        count = 0
        if self.check_is_pure_color_in_4k(1604, 1958, 1796, 1964):
            count += 1
            if self.check_is_pure_color_in_4k(1824, 1958, 2013, 1964):
                count += 1
                if self.check_is_pure_color_in_4k(2043, 1958, 2231, 1964):
                    count += 1
        if count == 0:
            # self.log_debug('count is 0, check left white')
            has_white_left = self.check_is_pure_color_in_4k(1604, 1958, 1614, 1964)
            if not has_white_left:
                count = -1
        return count

    def check_is_pure_color_in_4k(self, x1, y1, x2, y2):
        # 1. Extract the region of interest
        bar = self.frame[self.height_of_screen(y1 / 2160):self.height_of_screen(y2 / 2160),
                    self.width_of_screen(x1 / 3840):self.width_of_screen(x2 / 3840)]

        if bar.size == 0:
            return False

        # 2. Extract the first column (the reference color for each row)
        # Shape: (Height, 1, Channels)
        first_column = bar[:, 0:1]

        # 3. Calculate absolute difference
        # We MUST cast to int16 (or float) first.
        # In uint8: abs(100 - 102) = 2 (Correct)
        # But:      abs(100 - 98)  -> 100 - 98 = 2 (Correct)
        # However, standard subtraction 98 - 100 in uint8 becomes 254.
        # Converting to int16 allows for negative results before taking abs().
        diff = np.abs(bar.astype(np.int16) - first_column.astype(np.int16))

        # 4. Check if difference is within threshold (<= 2)
        # This checks R, G, and B individually.
        # np.all ensures every single pixel in the area meets this requirement.
        is_pure = np.all(diff <= 2)

        return is_pure
        

       
