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
        stream = praw.models.util.stream_generator(self.reddit.inbox.unread)
        for reply in stream:
            self.config.logger.debug("Messaged by {0}!".format(reply.author))
            if not isinstance(reply, praw.models.Comment):
                continue
            # Because reply.is_submitter is not avaiable from inbox.
            if reply.submission.author != reply.author:
                continue
            if not reply.parent().stickied:
                continue
            self.config.logger.debug("Removal disputed, reporting!")
            report = str(self.config.human_review_report).format(reply.author)
            reply.parent().report(report[:100])
            reply.mark_read()
            self.config.logger.debug("Reported.")
        self.config.logger.debug("Inbox monitor loop has ended!")

    def posts_monitor_loop(self):
        pass
