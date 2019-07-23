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

# import praw
# import shutil
# import requests
# from PIL import Image
# import pprint
# import pytesseract as tesseract
# from textdetector import TextDetector

# reddit = praw.Reddit()
# print(reddit.read_only)
# subreddit = reddit.subreddit("aww")
# print(subreddit.fullname)
# print("\n---\n")

# for post in subreddit.stream.submissions(skip_existing=False):
#     if post.is_self:
#         continue
#     link = post.url
#     if link.endswith(".png") or link.endswith(".jpg"):
#         print(f'Post by {post.author}: https://redd.it/{post.id}')
#         response = requests.get(link, stream=True)
#         if response.status_code != 200:
#             continue
#         image = Image.open(response.raw)
#         image = image.convert("RGB")
#         print(f"Image downloaded: {link}")
#         text_detector = TextDetector(image)
#         if text_detector.has_text():
#             print("--- ALERT ---")
#             print(f"Text found: '{text_detector.get_text()}'")
#             print("--- ALERT ---")
#         else:
#             print("No text found!")
#         print(text_detector.get_image_data()["conf"])
#         print(text_detector.get_image_data()["text"])
#         print("\n---\n")
