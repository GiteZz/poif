import concurrent.futures
from poif.tagged_data.base import BinaryData, StringBinaryData
from poif.file_system.partial import PartialGetWrapper
import random
import time


class MockBinary(StringBinaryData):
    def __init__(self, size=50):
        super().__init__(''.join(['data'] * size))
        self.count = 0

    def get(self) -> bytes:
        self.count += 1
        return super().get()


class TestPartial(PartialGetWrapper):
    def __init__(self, size=50, grace_period: float = 1.0):
        self.data = MockBinary(size)
        super().__init__(grace_period=grace_period, data=self.data)


def test_partial():
    size = 50
    data_object = TestPartial(size=size, grace_period=5)

    for _ in range(1000):
        random_index = random.randint(0, size - 1)

        assert data_object.get_partial(random_index * 4, 4).decode('utf-8') == 'data'

    assert data_object.data.count == 1


size = 50
grace_period = 0.0001
thread_count = 10
data_object = TestPartial(size=size, grace_period=.0001)


def random_access(index):
    # random_index = random.randint(0, size - 1)
    result = data_object.get_partial(index * 4, 4).decode('utf-8')
    time.sleep(grace_period * thread_count * 2)
    assert result == 'data'


def test_deletion():
    # size = 50
    # data_object =
    # args = [(data_object, random.randint(0, size - 1)) for _ in range(10)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(random_access, [random.randint(0, size - 1) for _ in range(1000)])

    print(data_object.data.count)
    assert data_object.data.count >= 1


