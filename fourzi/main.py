import os
from typing import Tuple
from fourzi.phrases_loader import XlsxPhrasesLoader
from fourzi.types import PhraseToScore, WordMatrix
from fourzi.words_generator import RandomWordsFromFourZiPhrasesGenerator


PHRASES_FILE_PATH = os.path.join(
    os.path.dirname(__file__),
    "resources",
    "FourZiData2.xlsx",
)


class GameLoop:
    def __init__(self) -> None:
        self._phrases_loader = XlsxPhrasesLoader(PHRASES_FILE_PATH)

    def run(self) -> None:
        # 1. Generate 36 words
        # 2. Display 36 words in 6x6 matrix
        # 3. Collect user inputs (4 words)
        # 4. Verify + calculate score, or return invalid
        phrase_to_score = self._phrases_loader.load_phrases()

        words = self.generate_selectable_words(phrase_to_score)
        self.render_words_display(words)

    def generate_selectable_words(self, phrase_to_score: PhraseToScore) -> WordMatrix:
        return RandomWordsFromFourZiPhrasesGenerator(phrase_to_score).generate_words()

    def render_words_display(self, word_matrix: WordMatrix) -> None:
        print(word_matrix)

    def ask_for_phrase(self) -> str:
        pass

    def validate_phrase(self, phrase: str) -> bool:
        pass

    def calculate_phrase_score(self, words: str) -> int:
        pass

    def _ask_for_word(self) -> Tuple[int, int] | None:
        row_col_input = input(
            "Enter the coordinates of the first letter (format: <row>,<col>)"
        )
        row, col = ",".split(row_col_input)

        try:
            _row = int(row)
            _col = int(row)
        except ValueError:
            print("Improperly formatted coordinates. Try again!")
            return None


if __name__ == "main":
    GameLoop().run()
