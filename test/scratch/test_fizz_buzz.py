from time import perf_counter_ns
from unittest import IsolatedAsyncioTestCase

from scratch.fizz_buzz import fizzbuzz


class FizzBuzzTest(IsolatedAsyncioTestCase):
    async def test_fizzbuzz(self):
        start_time_1 = perf_counter_ns()
        await fizzbuzz(20)
        end_time_1 = perf_counter_ns()
        await fizzbuzz(20)
        end_time_2 = perf_counter_ns()

        time_1_ms = (end_time_1 - start_time_1) / 1e6
        time_2_ms = (end_time_2 - end_time_1) / 1e6
        print(f"Time 1: {time_1_ms} ms")
        print(f"Time 2: {time_2_ms} ms")

        self.assertLess(time_2_ms, time_1_ms)
