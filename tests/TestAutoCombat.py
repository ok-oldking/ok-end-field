# Test case
import unittest

from src.config import config
from ok.test.TaskTestCase import TaskTestCase

from src.tasks.AutoCombatTask import AutoCombatTask


class TestMyOneTimeTask(TaskTestCase):
    task_class = AutoCombatTask

    config = config

    def test_skill_bars(self):
        self.set_image('tests/images/in_combat_3_bars.png')
        count = self.task.get_skill_bar_count()
        self.assertEqual(count, 3)

        self.set_image('tests/images/in_combat_1_bars.png')
        count = self.task.get_skill_bar_count()
        self.assertEqual(count, 1)

        self.set_image('tests/images/in_combat_3_blink.png')
        count = self.task.get_skill_bar_count()
        self.assertEqual(count, 3)

        self.set_image('tests/images/in_combat_0_bars.png')
        count = self.task.get_skill_bar_count()
        self.assertEqual(count, 0)

        self.set_image('tests/images/skip_quest_confirm.png')
        count = self.task.get_skill_bar_count()
        self.assertEqual(count, -1)

        self.set_image('tests/images/in_combat_low_health.png')
        count = self.task.get_skill_bar_count()
        self.assertEqual(count, 1)




if __name__ == '__main__':
    unittest.main()
