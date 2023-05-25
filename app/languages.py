from enum import IntEnum


class Language(IntEnum):
    # https://developers.lingvolive.com/ru-ru/Dictionaries
    EN = 1033
    RU = 1049

    @classmethod
    def from_str(cls, lang: str) -> 'Language':
        return cls[lang.upper()]
