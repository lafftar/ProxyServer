from utils.custom_logger import logger
from utils.singleton import Singleton


@Singleton
class Counter:
    def __init__(self):
        self.tasks = 0
        self.failed = 0
        self.success = 0


class Base:
    def __init__(self):
        self.counter: Counter = Counter.instance()
        self.counter.tasks += 1
        self.task_num = self.counter.tasks

    def prnt_frmt(self, text):
        return f'[Task {self.task_num}] ' \
               f': {text}'

    def info(self, text: str = 'Bluuu'):
        logger().info(self.prnt_frmt(text))

    def error(self, text: str = 'Bluuu'):
        logger().error(self.prnt_frmt(text))

    def warn(self, text: str = 'Bluuu'):
        logger().warning(self.prnt_frmt(text))

    def debug(self, text: str = 'Bluuu'):
        logger().debug(self.prnt_frmt(text))

    def exception(self, text: str = 'Bluuu'):
        logger().exception(self.prnt_frmt(text))