import re
import time
from typing import Any

import win32con

from ok import BaseTask


class BaseEfTask(BaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logged_in = False

    def in_bg(self):
        return not self.hwnd.is_foreground()

    def find_confirm(self):
        return self.find_one('skip_dialog_confirm', horizontal_variance=0.05, vertical_variance=0.05)

    def in_world(self):
        return self.find_one('top_left_tab')

    def find_f(self):
        return self.find_one('pick_f', vertical_variance=0.05)

    def wait_login(self):
        if not self._logged_in:
            if self.in_world():
                self._logged_in = True
                return True
            elif self.find_one('monthly_card') or self.find_one('logout') or self.find_one(
                    'reward_ok') or self.find_one(
                'one_click_claim'):
                self.click(after_sleep=1)
                return False
            elif close := self.find_one('check_in_close', threshold=0.75):
                self.click(close, after_sleep=1)
                return False
