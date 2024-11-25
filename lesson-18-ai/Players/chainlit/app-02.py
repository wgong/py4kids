import time
from datetime import datetime
import asyncio

def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def wait_for(t:float):
    ts_1 = ts()
    time.sleep(t)
    ts_2 = ts()
    return f"\tSYNC slept {t} sec \t[{ts_1}] ==> [{ts_2}]"

async def await_for(t:float):
    ts_1 = ts()
    await asyncio.sleep(t)
    ts_2 = ts()
    return f"\tASYNC slept {t} sec \t[{ts_1}] ==> [{ts_2}]"

async def main():
    msg = f"\n[{ts()}] Starting 'chainlit' ..."
    sleeper_0 = wait_for(5)
    msg += f"\n[{ts()}] sleeper_0 (S): {sleeper_0}"
    sleeper_1, sleeper_2 = await asyncio.gather(await_for(2), await_for(4))
    msg += f"\n[{ts()}] sleeper_1 (A): {sleeper_1}"
    msg += f"\n[{ts()}] sleeper_2 (A): {sleeper_2}"
    print(msg)

asyncio.run(main())
msg = f"\n[{ts()}] Stop!"
print(msg)