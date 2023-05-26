from dataclasses import dataclass


@dataclass(frozen=True)
class MiniCard:
    heading: str
    translation: str
    dictionary: str
    duration: float = 0.0

    @property
    def pretty(self) -> str:
        result = f'{self.heading} - {self.translation}\n{self.dictionary}'
        if self.duration:
            result += f' {self.duration:.2f} ms'

        return result
