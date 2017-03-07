from multiprocessing import Queue, Process
import numpy as np
from time import time


class Slave(Process):

    def __init__(self, querying_queue, results_queue, idx):

        super().__init__()
        self.querying_queue, self.results_queue = querying_queue, results_queue
        self.idx = idx

    def run(self):

        while True:

            a = self.querying_queue.get()
            if a != "stop":

                print("Slave {} reads: {}".format(self.idx, a))

                self.results_queue.put(self.f(a))

            else:
                break

        print("Slave {} says he is dead.".format(self.idx))

    def f(self, x):

        for i in range(10**7):  # Totally useless, but requires time!
            np.exp(x)
        return np.exp(x)


def main():

    t0 = time()
    n_workers = 4
    queue_list = []

    for i in range(n_workers):

        querying_queue, results_queue = Queue(), Queue()
        queue_list.append([querying_queue, results_queue])
        s = Slave(querying_queue=querying_queue, results_queue=results_queue, idx=i)
        s.start()

    queue_list = np.asarray(queue_list)

    querying = np.random.randint(1, 100, size=n_workers)

    for i, q in enumerate(queue_list[:, 0]):
        q.put(querying[i])

    for i, q in enumerate(queue_list[:, 1]):
        print("For query {}, I get result {}".format(querying[i], q.get()))

    for q in queue_list[:, 0]:
        q.put("stop")

    print("Time needed:", time()-t0)

if __name__ == "__main__":

    main()
