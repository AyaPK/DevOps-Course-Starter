class IndexViewModel:
    def __init__(self, lists):
        self._lists = lists

    @property
    def lists(self):
        return self._lists
