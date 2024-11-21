import chainlit as cl
from chainlit import make_async, run_sync
import time 
from datetime import datetime

def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def wait_for(t:float):
    ts_1 = ts()
    time.sleep(t)
    ts_2 = ts()
    return f"\tSYNC slept {t} sec \t[{ts_1}] ==> [{ts_2}]"

async def await_for(t:float):
    ts_1 = ts()
    time.sleep(t)
    ts_2 = ts()
    return f"\tASYNC slept {t} sec \t[{ts_1}] ==> [{ts_2}]"


@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here

    msg = f"\n[{ts()}] Starting '{message.content}' ..."

    sleeper_0 = wait_for(5)
    msg += f"\n[{ts()}] sleeper_0 (S): {sleeper_0}"

    sleeper_1 = await await_for(2) 
    msg += f"\n[{ts()}] sleeper_1 (A): {sleeper_1}"

    sleeper_2 = await await_for(4) 
    msg += f"\n[{ts()}] sleeper_2 (A): {sleeper_2}"

    # convert to sync
    sleeper_3 = run_sync(await_for(3))
    msg += f"\n[{ts()}] sleeper_3 (S): {sleeper_3}"

    # convert to async
    af = make_async(wait_for)
    sleeper_4 = await af(7)
    msg += f"\n[{ts()}] sleeper_4 (A): {sleeper_4}"

    msg += f"\n[{ts()}] Done processing !!!"

    # Send a response back to the user
    await cl.Message(
        content=msg,
    ).send()
