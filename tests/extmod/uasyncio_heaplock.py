# test that basic scheduling of tasks, and asyncio.sleep_ms, does not use the heap

import micropython

# strict stackless builds can't call functions without allocating a frame on the heap
try:
    f = lambda: 0
    micropython.heap_lock()
    f()
    micropython.heap_unlock()
except RuntimeError:
    print("SKIP")
    raise SystemExit

try:
    import asyncio
except ImportError:
    print("SKIP")
    raise SystemExit


async def task(id, n, t):
    for i in range(n):
        print(id, i)
        await asyncio.sleep_ms(t)


async def main():
    t1 = asyncio.create_task(task(1, 4, 100))
    t2 = asyncio.create_task(task(2, 2, 250))

    micropython.heap_lock()

    print("start")
    await asyncio.sleep_ms(5)
    print("sleep")
    await asyncio.sleep_ms(350)
    print("finish")

    micropython.heap_unlock()


asyncio.run(main())
