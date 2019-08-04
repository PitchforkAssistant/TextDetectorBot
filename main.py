from config import Config
from redditmonitor import RedditMonitor


def start_bot():
    config = Config()
    config.logger.debug("Config loaded, initializing RedditMonitor!")
    reddit_monitor = RedditMonitor(config)
    config.logger.info("Starting reddit monitors!")
    reddit_monitor.start_monitors()


if __name__ == "__main__":
    start_bot()
