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
        self.config.logger.debug("Starting monitors!")
        if self.config.remove:
            self.posts_thread = self.start_thread(self.posts_monitor_loop)
        if self.config.human_review:
            self.inbox_thread = self.start_thread(self.inbox_monitor_loop)
        self.config.logger.debug("Monitors started!")

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
            report = str(self.config.human_review_report).format(
                username=reply.author.name)
            reply.parent().report(report[:100])
            reply.mark_read()
            self.config.logger.debug("Reported.")
        self.config.logger.debug("Inbox monitor loop has ended!")

    def posts_monitor_loop(self):
        subreddit = self.reddit.subreddit("mod")
        for post in subreddit.stream.submissions():
            if post.is_self:
                continue
            image = imagedownloader.DownloadImage(post.url)
            if image is None:
                self.config.logger.debug("No image returned for " + post.url)
                continue
            textdetector = TextDetector(image)
            if not textdetector.has_text():
                continue
            post.mod.remove()
            reason = str(self.config.removal_reason).format(
                username=post.author.name,
                subreddit=post.subreddit.display_name,
                text=textdetector.get_text())
            reason.mod.distinguish(sticky=True)
