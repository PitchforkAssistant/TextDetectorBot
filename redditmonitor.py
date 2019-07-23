import threading

import praw

import imagedownloader
from textdetector import TextDetector


class RedditMonitor:
    __slots__ = ["reddit", "config", "posts_thread", "inbox_thread"]

    def __init__(self, config):
        self.config = config
        self.reddit = praw.Reddit()

    def start_thread(self, target):
        thread = threading.Thread(target=target)
        thread.start()
        return thread

    def start_monitors(self):
        self.posts_thread = self.start_thread(self.posts_monitor_loop)
        if self.config.human_review:
            self.inbox_thread = self.start_thread(self.inbox_monitor_loop)

    def inbox_monitor_loop(self):
        pass

    def posts_monitor_loop(self):
        pass
