# Copyright (c) [2025] [Yifu Ding]
class SingletonMeta(type):
    def __init__(self, *args, **kwargs):
        self._instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = super().__call__(*args, **kwargs)
        return self._instance
