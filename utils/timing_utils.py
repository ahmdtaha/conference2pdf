import time
from tqdm import tqdm

class BlockTimer:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.interval = self.end - self.start
        print('Block took {:.03f} sec.'.format(self.interval))


class LoopBar:
    def __init__(self,bar_len):
        self.bar_len = bar_len
        # self.bar_progress = 0

    def step(self):
        # self.bar_progress+=1
        self.pbar.update(1)

    def update(self,value):
        # self.bar_progress = value
        self.pbar.update(value)


    def __enter__(self):
        self.pbar = tqdm(total=self.bar_len)
        return self

    def __exit__(self, *args):
        self.pbar.close()
