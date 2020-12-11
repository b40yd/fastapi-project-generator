#
# Copyright (C) {{cookiecutter.copyright}}
#
# Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
#

class Queue:
    def __init__(self, data: list):
        self.data = data
        self.front = 0
        self.tail = 0
        self.size = len(data)

    def __str__(self):
        return str(self.data)

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def get_size(self):
        return self.size

    def get_capaticty(self):
        return self.__len__() - 1

    def is_full(self):
        return (self.tail+1) % len(self.data) == self.front

    def is_empty(self):
        return self.size == 0

    def get_front(self):
        return self.data[self.front]

    def enqueue(self, e):
        if self.is_full():
            self.resize(self.get_capaticty() * 2)
        self.data[self.tail] = e
        self.tail = (self.tail+1) % len(self.data)
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            return None

        result = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front+1) % len(self.data)
        if self.size < self.get_capaticty() // 4 and self.get_capaticty() > 1:
            self.resize(self.get_capaticty() // 2)
        return result

    def resize(self, new_capacity):
        new_arr = [None] * (new_capacity+1)
        for i in range(self.size):
            new_arr[i] = self.data[(i+self.front) % len(self.data)]

        self.data = new_arr
        self.front = 0
        self.tail = self.size
