import threading

from poif.tagged_data.base import BinaryData


class PartialGetWrapper(BinaryData):
    def __init__(self, data: BinaryData, grace_period=1):
        self.data = data

        self.get_lock = threading.Lock()
        self.timer = None
        self.cached_data = None
        self.grace_period = grace_period

    @property
    def size(self) -> int:
        return self.data.size

    def get(self) -> bytes:
        return self.data.get()

    def clear_data(self):
        print('Clearing data')
        with self.get_lock:
            self.cached_data = None

    def get_partial(self, offset: int, length: int) -> bytes:
        print('Accessing data')
        with self.get_lock:
            if self.cached_data is None:
                self.cached_data = self.get()

            needed_data = self.cached_data[offset: offset + length]

            if self.timer is not None:
                self.timer.cancel()
            self.timer = threading.Timer(self.grace_period, self.clear_data)
            self.timer.start()

        return needed_data
