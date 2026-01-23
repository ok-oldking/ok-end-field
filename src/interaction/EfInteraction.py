import re
import traceback
import time
import win32api
import win32con

from ok import PostMessageInteraction, Logger

logger = Logger.get_logger(__name__)

class EfInteraction(PostMessageInteraction):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # def click(self, x=-1, y=-1, move_back=False, name=None, down_time=0.02, move=True, key="left", block=False):
    #     self.operate(lambda: self.do_click(x, y, down_time=down_time, key=key), block=block)

    # def send_key(self, key, down_time=0.02, block=False):
    #     logger.debug(f'EfInteraction send key {key} {down_time}')
    #     self.operate(lambda: self.do_send_key(key, down_time), block=block)

    # def do_click(self, x=-1, y=-1, move_back=False, name=None, down_time=0.02, move=True, key="left"):
    #     click_pos = self.make_mouse_position(x, y)
    #     if key == "left":
    #         btn_down = win32con.WM_LBUTTONDOWN
    #         btn_mk = win32con.MK_LBUTTON
    #         btn_up = win32con.WM_LBUTTONUP
    #     elif key == "middle":
    #         btn_down = win32con.WM_MBUTTONDOWN
    #         btn_mk = win32con.MK_MBUTTON
    #         btn_up = win32con.WM_MBUTTONUP
    #     else:
    #         btn_down = win32con.WM_RBUTTONDOWN
    #         btn_mk = win32con.MK_RBUTTON
    #         btn_up = win32con.WM_RBUTTONUP
    #     self.post(btn_down, btn_mk, click_pos
    #               )
    #     time.sleep(down_time)
    #     self.post(btn_up, 0, click_pos
    #               )

    # def send_key_down(self, key, block=False):
    #     if not self.hwnd_window.is_foreground():
    #         self.activate()
    #     self.post_interaction.send_key_down(key, activate=False)

    # def send_key_up(self, key, block=False):
    #     if not self.hwnd_window.is_foreground():
    #         self.activate()
    #     self.post_interaction.send_key_up(key)
