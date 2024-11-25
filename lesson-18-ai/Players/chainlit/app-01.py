import chainlit as cl
from chainlit import make_async, run_sync
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


@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here

    msg = f"\n[{ts()}] Starting '{message.content}' ..."

    sleeper_0 = wait_for(3)
    msg += f"\n[{ts()}] sleeper_0 (S): {sleeper_0}"

    # convert to async
    af = make_async(wait_for)

    sleeper_1, sleeper_2, sleeper_4 = await asyncio.gather(await_for(2),await_for(4), af(7))
    msg += f"\n[{ts()}] sleeper_1 (A): {sleeper_1}"
    msg += f"\n[{ts()}] sleeper_2 (A): {sleeper_2}"
    msg += f"\n[{ts()}] sleeper_4 (A): {sleeper_4}"

    # convert to sync
    sleeper_3 = run_sync(await_for(2))
    msg += f"\n[{ts()}] sleeper_3 (S): {sleeper_3}"

    msg += f"\n[{ts()}] Done processing !!!"

    # Send a response back to the user
    await cl.Message(
        content=msg,
    ).send()
