import os

class Helper:

    def __init__(self, path):
        self.path = path

    def get_path(self, file):
        print(f"[Helper] {file}")
        base_path = os.getcwd()
        return os.path.join(base_path, file)
