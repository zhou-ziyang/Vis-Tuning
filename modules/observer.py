import os
import time

# from modules.event import Event


class Observer:
    observers = []

    def __init__(self):
        self.observers.append(self)
        self.observables = {}

    def observe(self, event_name, callback):
        self.observables[event_name] = callback
