class IndexViewModel:
    def __init__(self, lists):
        self._lists = lists

    def get_items_with_status(self, status):
        return [item for _list in self._lists if _list.id == status for item in _list.items]

    @property
    def lists(self):
        return self._lists

    @property
    def to_do_items(self):
        return self.get_items_with_status("to-do")

    @property
    def doing(self):
        return self.get_items_with_status("doing")

    @property
    def done_items(self):
        return self.get_items_with_status("done")

