import string
from enum import IntEnum

# automatic language detection
AUTO_CHOICE = 'auto'


class Language(IntEnum):
    """
    Language enum.
    Dictionaries https://developers.lingvolive.com/ru-ru/Dictionaries
    """
    EN = 1033
    RU = 1049

    @classmethod
    def from_str(cls, lang: str) -> 'Language':
        return cls[lang.upper()]

    @classmethod
    def find_src(cls, word: str, n: int = 3) -> 'Language':
        """Returns source language for word by first N letters."""
        if not word:
            raise ValueError('word is empty')

        is_en = any(letter in string.ascii_lowercase for letter in word[:n].lower())
        return cls.EN if is_en else cls.RU

    @classmethod
    def parse(cls, choice: str, word: str) -> tuple['Language', 'Language']:
        if choice == AUTO_CHOICE:
            src = cls.find_src(word)
            dst = cls.RU if src == cls.EN else cls.EN
            return src, dst

        src, dst = choice.split('-')
        return cls.from_str(src), cls.from_str(dst)


# possible language choices
LANGUAGE_CHOICES = [
    AUTO_CHOICE,
    '{}-{}'.format(Language.EN.name.lower(), Language.RU.name.lower()),
    '{}-{}'.format(Language.RU.name.lower(), Language.EN.name.lower()),
]
