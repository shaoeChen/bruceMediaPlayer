import threading
import concurrent.futures


class Worker(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def __call__(self, proc):
        """

        :param proc: 預期執行的函數
        :return:
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(proc)
