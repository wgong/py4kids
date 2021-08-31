from worker_helper import Helper

class Worker:

    def __init__(self):
        self.helper = Helper('os')

    def work(self):
        path = self.helper.get_path("readme.md")
        print(f'[Worker] "{path}"')
        return path
