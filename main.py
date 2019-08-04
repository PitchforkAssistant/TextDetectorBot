from sys import exit

from config import Config
from redditmonitor import RedditMonitor


def start_bot():
    config = Config()
    config.logger.debug("Config loaded, initializing RedditMonitor!")
    reddit_monitor = RedditMonitor(config)
    config.logger.info("Starting reddit monitors!")
    try:
        reddit_monitor.start_monitors()
    except Exception as ex:
        # Either a bug or reddit is down, log exception and exit.
        # Bot will be restarted by systemd
        self.config.logger.exception(ex)
        exit()


if __name__ == "__main__":
    start_bot()
