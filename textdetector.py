import string

import pytesseract


class TextDetector:
    __slots__ = ["_image",
                 "_image_data",
                 "minimum_chars",
                 "minimum_count",
                 "minimum_confidence",
                 "counted_characters"]

    def __init__(self,
                 image,
                 counted_characters=string.ascii_letters+string.digits,
                 minimum_confidence=80,
                 minimum_chars=2,
                 minimum_count=3):
        self.image = image
        self.counted_characters = counted_characters
        self.minimum_confidence = minimum_confidence
        self.minimum_count = minimum_count
        self.minimum_chars = minimum_chars

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, x):
        self._image = x
        self._image_data = None

    def get_image_data(self):
        if not self._image_data:
            self._image_data = pytesseract.image_to_data(
                self.image,
                output_type=pytesseract.Output.DICT
            )
        return self._image_data

    def has_text(self,
                 counted_characters=None,
                 minimum_confidence=None,
                 minimum_chars=None,
                 minimum_count=None):

        if counted_characters is None:
            counted_characters = self.counted_characters
        if minimum_confidence is None:
            minimum_confidence = self.minimum_confidence
        if minimum_chars is None:
            minimum_chars = self.minimum_chars
        if minimum_count is None:
            minimum_count = self.minimum_count

        text = self.get_text(counted_characters=counted_characters,
                             minimum_confidence=minimum_confidence,
                             minimum_chars=minimum_chars)
        return len(text) >= minimum_count

    def get_text(self,
                 counted_characters=None,
                 minimum_confidence=None,
                 minimum_chars=None):

        if counted_characters is None:
            counted_characters = self.counted_characters
        if minimum_confidence is None:
            minimum_confidence = self.minimum_confidence
        if minimum_chars is None:
            minimum_chars = self.minimum_chars

        image_data = self.get_image_data()
        found_text = []
        for index, confidence in enumerate(image_data["conf"]):
            if float(confidence) < minimum_confidence:
                continue
            text = image_data["text"][index]
            if counted_characters:  # Not None or empty
                text = "".join(ch for ch in text if ch in counted_characters)
            if len(text) < minimum_chars:
                continue
            found_text.append(image_data["text"][index])
        return found_text
