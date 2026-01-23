import time

import cv2
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
        self.description = "自动战斗(进入战斗后自动战斗直到结束)"
        self.icon = FluentIcon.ACCEPT
        self.default_config.update({
            "技能释放": "1234",
            # "攻击快捷键": "",
            "后台结束战斗通知": True
        })
        self.config_description.update({
            "技能释放": "满技能时, 开始释放技能, 如1123",
            # "攻击快捷键": "如果设置则使用攻击按键代替鼠标左键",
        })

    def run(self):
        # self.log_debug('AutoCombatTask.run()')
        bar_count = self.get_skill_bar_count()
        if self.get_skill_bar_count() < 0 or not self.in_team():
            return
        self.log_info('enter combat {}'.format(bar_count))
        raw_skill_config = self.config.get("技能释放", "")

        # Parse to local variable
        skill_sequence = self._parse_skill_sequence(raw_skill_config)
        if self.debug:
            self.screenshot('enter_combat')
        self.click(key='middle')
        while True:
            skill_count = self.get_skill_bar_count()
            if skill_count < 0:
                self.log_info("自动战斗结束!", notify=self.config.get("后台结束战斗通知") and self.in_bg())
                if self.debug:
                    self.screenshot('out_of_combat')
                if self.wait_in_combat(click=True):
                    self.log_debug('re-enter combat')
                    self.click(key='middle')
                    continue
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
                    elif self.use_e_skill():
                        continue
                    elif current_count != last_count:
                        i += 1
                        self.log_debug("skill success use next".format(i))
                        if i >= len(skill_sequence):
                            break
                    # use skill
                    start = time.time()
                    last_attack = start
                    while time.time() - start < 6:
                        count = self.get_skill_bar_count()
                        if count == current_count:
                            self.send_key(skill_sequence[i], after_sleep=0.1)
                        elif self.use_e_skill():
                            continue
                        elif count < 0:
                            self.log_debug('skill -1 when using skills {}'.format(count))
                            break
                        elif count < current_count:
                            self.log_debug('use skill success')
                            break
                        elif time.time() - last_attack > 0.5:
                            last_attack = time.time()
                            self.click(after_sleep=0.1)
                        self.next_frame()
            else:
                if key:=self.config.get("攻击快捷键"):
                    self.send_key(key, after_sleep=0.5)
                else:
                    self.click(after_sleep=0.5)
            self.sleep(0.01)

    def _parse_skill_sequence(self, raw_config: str) -> list[str]:
        """
        Parses and validates the skill configuration string.
        """
        if not raw_config:
            return []

        trimmed_config = raw_config.strip()
        sequence = []
        valid_skills = {'1', '2', '3', '4'}

        for char in trimmed_config:
            if char not in valid_skills:
                raise ValueError(f"Invalid skill character '{char}' detected. Skills can only be 1-4.")
            sequence.append(char)

        return sequence

    def use_ult(self):
        ults = ['1', '2', '3', '4']
        for ult in ults:
            if self.find_one("ult_" + ult):
                self.send_key_down(ult)
                self.wait_until(lambda :not self.in_combat())
                self.send_key_up(ult)
                self.wait_in_combat(time_out=6)
                return True

    def wait_in_combat(self, time_out=3, click=False):
        start = time.time()
        while time.time() - start < time_out:
            if self.in_combat():
                return True
            elif click:
                self.click(after_sleep=0.4)
            else:
                self.sleep(0.1)

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

        skill_area = self.frame[self.height_of_screen(1943 / 2160):self.height_of_screen(1983 / 2160),
              self.width_of_screen(1597 / 3840):self.width_of_screen(2259 / 3840)]
        # self.screenshot('skill_area', frame=skill_area)
        if not has_rectangles(skill_area):
            return -1

        count = 0
        y_start = 1958
        y_end = 1970
        if self.check_is_pure_color_in_4k(1604, y_start, 1796, y_end, yellow_skill_color):
            count += 1
            if self.check_is_pure_color_in_4k(1824, y_start, 2013, y_end, yellow_skill_color):
                count += 1
                if self.check_is_pure_color_in_4k(2043, y_start, 2231, y_end, yellow_skill_color):
                    count += 1
        if count == 0:
            # self.log_debug('count is 0, check left white')
            has_white_left = self.check_is_pure_color_in_4k(1604, y_start, 1614, y_end, white_skill_color, threshold=0.1)
            if not has_white_left:
                count = -1
        return count

    def check_is_pure_color_in_4k(self, x1, y1, x2, y2, color_range=None, threshold=0.9):
        bar = self.frame[self.height_of_screen(y1 / 2160):self.height_of_screen(y2 / 2160),
              self.width_of_screen(x1 / 3840):self.width_of_screen(x2 / 3840)]
        # self.screenshot('check_is_pure_color_in_4k', frame=bar)
        if bar.size == 0:
            return False

        height, width, _ = bar.shape
        consecutive_matches = 0

        # Iterate through every horizontal line (row) in the bar
        for i in range(height):
            row_pixels = bar[i]  # Shape is (Width, 3)

            # Find unique colors and their counts for this specific row
            unique_colors, counts = np.unique(row_pixels, axis=0, return_counts=True)

            # Find the most frequent color in this row
            most_frequent_index = np.argmax(counts)
            dominant_count = counts[most_frequent_index]
            dominant_color = unique_colors[most_frequent_index]

            # Determine if this row is valid
            is_valid_row = True

            # 1. Check if the dominant color constitutes at least threshold %
            if (dominant_count / width) < threshold:
                is_valid_row = False

            # 2. If color_range is provided, ensure this row's dominant color fits the range
            if is_valid_row and color_range:
                b, g, r = dominant_color
                if not (color_range['r'][0] <= r <= color_range['r'][1]):
                    is_valid_row = False
                elif not (color_range['g'][0] <= g <= color_range['g'][1]):
                    is_valid_row = False
                elif not (color_range['b'][0] <= b <= color_range['b'][1]):
                    is_valid_row = False

            # Check consecutive streak
            if is_valid_row:
                consecutive_matches += 1
                if consecutive_matches >= 2:
                    return True
            else:
                consecutive_matches = 0

        return False

def has_rectangles(frame):
    """
    Analyzes an OpenCV frame to look for 3 bars and count how many are yellow.

    Args:
        frame: A numpy array representing the image (BGR format).

    Returns:
        int: -1 if the 3-bar structure is not found.
             0-3 indicating the number of fully charged (yellow) bars.
    """

    # 1. PRE-PROCESSING FOR STRUCTURE DETECTION
    if frame is None:
        return -1

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 2. DETECTING THE UI ELEMENTS (BARS)
    # Apply GaussianBlur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    potential_bars = []

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Filter noise: Minimum size check
        if w < 20 or h < 5:
            continue

        # Aspect Ratio Check: The bars are rectangles (wider than tall)
        aspect_ratio = float(w) / h
        if 2.5 < aspect_ratio < 15.0:
            potential_bars.append((x, y, w, h))

    if len(potential_bars) >= 1:
        return True

yellow_skill_color = {
    'r': (230, 255),  # Red range
    'g': (180, 255),  # Green range
    'b': (0, 85)  # Blue range
}

white_skill_color = {
    'r': (190, 255),  # Red range
    'g': (190, 255),  # Green range
    'b': (190, 255)  # Blue range
}


