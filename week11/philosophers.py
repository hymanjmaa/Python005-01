#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project Name: Python005-01
@Author: 'Hyman MA'
@Email: 'hymanjma@gmail.com'
@Time: 2021/2/1 11:05
"""
import queue
import threading


class DiningPhilosophers2:

    def __init__(self):
        self.l = threading.Lock()

    def wantsToEat(self, philosopher, *actions):
        self.l.acquire()
        [*map(lambda func: func(), actions)]
        self.l.release()


class DiningPhilosopher3:

    def __init__(self):
        self.actions = []

    def wantsToEat(self, philosopher, *actions):
        self.actions += actions
        [*map(lambda _: self.actions.pop(0)(), actions)]


class DiningPhilosophers:
    def __init__(self):
        self.ForkLocks = [threading.Lock() for _ in range(5)]  # 叉子锁

    def wantsToEat(self,
                   philosopher,
                   pickLeftFork,
                   pickRightFork,
                   eat,
                   putLeftFork,
                   putRightFork):
        # 左右叉子的编号
        right_fork = philosopher
        left_fork = (philosopher + 1) % 5

        # 偶数编号的先拿右边叉子
        if philosopher % 2 == 0:
            self.ForkLocks[right_fork].acquire()
            self.ForkLocks[left_fork].acquire()

        # 奇数编号的先拿左边叉子
        else:
            self.ForkLocks[left_fork].acquire()
            self.ForkLocks[right_fork].acquire()
        pickLeftFork()
        pickRightFork()
        eat()
        putLeftFork()
        putRightFork()
        self.ForkLocks[right_fork].release()
        self.ForkLocks[left_fork].release()


class DiningPhilosophers1:
    def __init__(self):
        self.lock = threading.Lock()

    def wantsToEat(self,
                   philosopher,
                   pickLeftFork,
                   pickRightFork,
                   eat,
                   putLeftFork,
                   putRightFork):
        self.lock.acquire()
        pickLeftFork()
        pickRightFork()
        eat()
        putLeftFork()
        putRightFork()
        self.lock.release()


class Pthread(threading.Thread):
    def __init__(self, p_num, q):
        super().__init__()
        self.p_num = p_num
        self.q = q

    def run(self):
        p = DiningPhilosophers()
        p.wantsToEat(self.p_num,
                     self.pickLeftFork,
                     self.pickRightFork,
                     self.eat,
                     self.putLeftFork,
                     self.putRightFork)

    def pickLeftFork(self):
        self.q.put([self.p_num, 1, 1])

    def pickRightFork(self):
        self.q.put([self.p_num, 2, 2])

    def eat(self):
        self.q.put([self.p_num, 0, 3])

    def putLeftFork(self):
        self.q.put([self.p_num, 1, 2])

    def putRightFork(self):
        self.q.put([self.p_num, 2, 2])


if __name__ == '__main__':
    q = queue.Queue()
    n = 3
    thead_list = []
    for x in range(5 * n):
        pt = Pthread(x % 5, q)
        pt.start()
        thead_list.append(pt)

    for t in thead_list:
        t.join()

    queue_list = []
    for i in range(5 * 5 * n):
        queue_list.append(q.get())
    print(queue_list)
