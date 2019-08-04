import threading
from sys import exit

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
            try:
                self.config.logger.debug("New post: " + post.permalink)
                if post.is_self or post.approved:
                    continue
                image = imagedownloader.DownloadImage(post.url)
                if image is None:
                    self.config.logger.debug("Got no image from: " + post.url)
                    continue
                textdetector = TextDetector(image)
                if not textdetector.has_text():
                    self.config.logger.debug("Text not found in image.")
                    continue
                self.config.logger.debug(
                    "Removing {0}, text found: {1}".format(
                        post.permalink, textdetector.get_text()))
                post.mod.remove()
                reason = str(self.config.removal_reason).format(
                    username=post.author.name,
                    subreddit=post.subreddit.display_name,
                    text=", ".join(textdetector.get_text()))
                reply = post.reply(reason)
                reply.mod.distinguish(sticky=True)
                self.config.logger.debug(post.permalink + " has been removed!")
            except:
                # I'm catching all exceptions and logging them, most likely,
                # something went wrong with processing/downloading the image.
                self.config.logger.exception(
                    "Exception in posts_monitor_loop:")
