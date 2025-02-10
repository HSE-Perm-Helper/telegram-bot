class CannotResentEmailByDelayException(Exception):
    def __init__(self, delay: int):
        self.delay = delay