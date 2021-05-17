from collections import namedtuple
import asyncio
import rx
import rx.operators as ops
from rx.subject import Subject
from rx.scheduler.eventloop import AsyncIOScheduler

EchoItem = namedtuple('EchoItem', ['future', 'data'])


def tcp_server(sink, loop):
    def on_subscribe(observer, scheduler):
        async def handle_echo(reader, writer):
            print("new client connected")
            while True:
                data = await reader.readline()
                data = data.decode("utf-8")
                if not data:
                    break

                future = asyncio.Future()
                observer.on_next(EchoItem(
                    future=future,
                    data=data
                ))
                await future
                writer.write(future.result().encode("utf-8"))

            print("Close the client socket")
            writer.close()

        def on_next(i):
            i.future.set_result(i.data)

        PORT = 8001
        print(f"starting telnet echo server on port={PORT}")
        server = asyncio.start_server(handle_echo, '127.0.0.1', PORT, loop=loop)
        loop.create_task(server)

        sink.subscribe(
            on_next=on_next,
            on_error=observer.on_error,
            on_completed=observer.on_completed)

    return rx.create(on_subscribe)


loop = asyncio.get_event_loop()
proxy = Subject()
source = tcp_server(proxy, loop)
aio_scheduler = AsyncIOScheduler(loop=loop)

source.pipe(
    ops.map(lambda i: i._replace(data="echo: {}".format(i.data))),
    ops.delay(5.0)
).subscribe(proxy, scheduler=aio_scheduler)

loop.run_forever()
print("done")
loop.close()
