from qfluentwidgets import FluentIcon

from ok import TriggerTask, Logger
from src.tasks.BaseEfTask import BaseEfTask

logger = Logger.get_logger(__name__)


class AutoLoginTask(BaseEfTask, TriggerTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_config = {'_enabled': True}
        self.trigger_interval = 5
        self.name = "自动登录"
        self.description = "自动登录领月卡"
        self.icon = FluentIcon.ACCEPT

    def run(self):
        if self._logged_in:
            return
        else:
            return self.wait_login()
