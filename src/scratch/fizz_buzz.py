import asyncio
import sys

from async_lru import alru_cache


async def fizzbuzz(n):
    for i in range(1, n + 1):
        fizz_buzz_val = await _fizz_buzz_for(i)
        if isinstance(fizz_buzz_val, str):
            print(fizz_buzz_val, file=sys.stderr)
        else:
            print(fizz_buzz_val)


@alru_cache(maxsize=None)
async def _fizz_buzz_for(n: int) -> int | str:
    await asyncio.sleep(1 / 3)
    if n % 3 == 0 and n % 5 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:
        return n


if __name__ == "__main__":
    asyncio.run(fizzbuzz(20))
    asyncio.run(fizzbuzz(20))
