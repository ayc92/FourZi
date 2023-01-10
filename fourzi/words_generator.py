import logging
import random
import numpy as np
from abc import ABC, abstractmethod
from itertools import chain
from typing import Callable, Iterable, List

from fourzi.types import PhraseToScore, WordMatrix

logger = logging.Logger(__name__)


class WordsGenerator(ABC):
    @abstractmethod
    def generate_words(self) -> WordMatrix:
        ...


class RandomWordsFromFourZiPhrasesGenerator(WordsGenerator):
    NUM_WORDS_PER_PHRASE = 4
    NUM_PHRASES = 9
    MAT_SIDE_SIZE = 6

    _phrases: List[str]
    _shuffle_func: Callable[[Iterable[str]], None]

    def __init__(
        self,
        phrase_to_score: PhraseToScore,
        shuffle_func: Callable[[Iterable[str]], None] = random.shuffle,
    ) -> None:
        self._phrases = list(phrase_to_score.keys())
        self._shuffle_func = shuffle_func

    def generate_words(self) -> WordMatrix:
        random_phrases = self._pick_random_phrases(self.NUM_PHRASES)

        words_from_phrases = self._extract_words_from_phrases(random_phrases)
        shuffled_words = self._shuffle_words_from_phrases(words_from_phrases)

        return self._words_list_to_matrix(shuffled_words)

    def _pick_random_phrases(self, num_phrases: int) -> List[str]:
        num_phrases_left = num_phrases
        remaining_phrases_to_choose_from = list(self._phrases)

        chosen_phrases = []

        while num_phrases_left > 0:
            idx = random.randint(0, len(remaining_phrases_to_choose_from))
            try:
                chosen_phrase = remaining_phrases_to_choose_from.pop(idx)
            except IndexError:
                # If for whatever reason, there are no more phrases left to choose from, exit the loop.
                logger.info(f"Invalid index when picking phrases: {idx}")
                break
            else:
                chosen_phrases.append(chosen_phrase)
                num_phrases_left -= 1

        return chosen_phrases

    def _extract_words_from_phrases(self, phrases: List[str]) -> List[str]:
        phrases_split: List[List[str]] = [
            [word for word in phrase] for phrase in phrases
        ]

        return list(chain.from_iterable(phrases_split))

    def _shuffle_words_from_phrases(self, words_from_phrases: List[str]) -> List[str]:
        words = list(words_from_phrases)
        self._shuffle_func(words)
        return words

    def _words_list_to_matrix(
        self, words: List[str], matrix_side_size: int = MAT_SIDE_SIZE
    ) -> WordMatrix:
        matrix = [
            words[(i * matrix_side_size) : ((i + 1) * matrix_side_size)]
            for i in range(int(len(words) / matrix_side_size))
        ]

        return np.array(matrix)
